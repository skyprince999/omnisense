"""Hardened static server for the Cloudflare-tunnelled public viewer.

`serve.py` serves this whole folder, which includes `.env` (live VIDEODB_API_KEY)
and generates a directory listing at `/`. That is fine on localhost and a
credential leak the moment a tunnel points at it. This server serves ONLY the
paths `trip_dist_viewer_v6.html` actually requests:

    trip_dist_viewer_v6.html                (also served at "/")
    stitched/<stem>.mp4                     detections/<stem>.detections.json
    depth/<stem>.depth.mp4                  detections/manifest.json
    tracks/<stem>.tracks.json               slices/<stem>.slices.v5.json
    distances/<stem>.distances.json         nudges/<file>.mp3

Everything else -> 404. No directory listings, no dotfiles, no traversal.
Range requests are answered with 206 so video seeking works (same reason as
serve.py — the stdlib handler ignores Range).

Usage:
    python serve_public.py            # http://localhost:8001
    python serve_public.py 9000       # custom port
"""

import os
import re
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
INDEX = "trip_dist_viewer_v6.html"

# make_web_videos.py writes 720p @ ~1.5 Mbps versions of the 1080p @ 12 Mbps
# sources here. A request for stitched/<stem>.mp4 is served from web/<stem>.mp4
# when one exists, so the viewer needs no change and `stitched/` stays canonical
# for local work. Sources already small enough have no web/ copy and fall back.
WEB_DIR = "web"

# Top-level folders the viewer fetches from, and what may be served out of each.
ALLOWED_DIRS = {
    "stitched": {".mp4"},
    "depth": {".mp4"},
    "detections": {".json"},
    "tracks": {".json"},
    "distances": {".json"},
    "slices": {".json"},
    "nudges": {".mp3", ".wav", ".m4a", ".ogg"},
}
ALLOWED_ROOT_FILES = {INDEX.lower()}

RANGE_RE = re.compile(r"bytes=(\d*)-(\d*)")


def is_allowed(rel: str) -> bool:
    """rel is a '/'-joined path already normalized and known traversal-free."""
    parts = rel.split("/")
    if any(p.startswith(".") for p in parts):
        return False
    if len(parts) == 1:
        return parts[0].lower() in ALLOWED_ROOT_FILES
    exts = ALLOWED_DIRS.get(parts[0])
    return exts is not None and os.path.splitext(parts[-1])[1].lower() in exts


class PublicHandler(SimpleHTTPRequestHandler):
    server_version = "omnisense-viewer"

    def list_directory(self, path):  # never expose a listing
        self.send_error(404, "Not Found")
        return None

    def send_head(self):
        rel = unquote(urlparse(self.path).path).lstrip("/")
        if rel in ("", "index.html"):
            self.send_response(302)
            self.send_header("Location", "/" + INDEX)
            self.end_headers()
            return None

        rel = os.path.normpath(rel).replace("\\", "/")
        if rel.startswith("..") or os.path.isabs(rel) or not is_allowed(rel):
            self.send_error(404, "Not Found")
            return None

        parts = rel.split("/")
        if parts[0] == "stitched" and len(parts) == 2:
            web = os.path.join(ROOT, WEB_DIR, parts[1])
            if os.path.isfile(web):
                return self._send_file(web)

        full = os.path.join(ROOT, *parts)
        if not os.path.isfile(full):
            self.send_error(404, "Not Found")
            return None

        return self._send_file(full)

    def _validators(self, full, size):
        """Cloudflare caches .mp4 by default (4h). Without ETag/Last-Modified it
        cannot revalidate, so a file replaced at the origin keeps serving stale
        from the edge until the TTL lapses — which is exactly what happened when
        web/ replaced the 1080p sources. These let the edge re-check instead."""
        mtime = os.path.getmtime(full)
        return (
            self.date_time_string(int(mtime)),
            f'"{int(mtime):x}-{size:x}"',
        )

    def _send_file(self, full):
        size = os.path.getsize(full)
        ctype = self.guess_type(full)
        last_mod, etag = self._validators(full, size)

        # A matching validator means the edge/browser copy is current.
        if self.headers.get("If-None-Match") == etag:
            self.send_response(304)
            self.send_header("ETag", etag)
            self.end_headers()
            return None

        rng = self.headers.get("Range")
        m = RANGE_RE.match(rng) if rng else None

        if not m:
            f = open(full, "rb")
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Length", str(size))
            self.send_header("Last-Modified", last_mod)
            self.send_header("ETag", etag)
            self.end_headers()
            return f

        start_s, end_s = m.group(1), m.group(2)
        if start_s == "":
            length = min(int(end_s or 0), size)
            start, end = size - length, size - 1
        else:
            start = int(start_s)
            end = int(end_s) if end_s else size - 1
        end = min(end, size - 1)

        if start > end or start >= size:
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{size}")
            self.end_headers()
            return None

        length = end - start + 1
        f = open(full, "rb")
        f.seek(start)
        self.send_response(206)
        self.send_header("Content-Type", ctype)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(length))
        self.send_header("Last-Modified", last_mod)
        self.send_header("ETag", etag)
        self.end_headers()
        return _LimitedReader(f, length)


class _LimitedReader:
    """Stops copyfile() after exactly `remaining` bytes (see serve.py)."""

    def __init__(self, fp, remaining):
        self.fp = fp
        self.remaining = remaining

    def read(self, n=-1):
        if self.remaining <= 0:
            return b""
        if n is None or n < 0 or n > self.remaining:
            n = self.remaining
        data = self.fp.read(n)
        self.remaining -= len(data)
        return data

    def close(self):
        self.fp.close()


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8001
    handler = partial(PublicHandler, directory=ROOT)
    with ThreadingHTTPServer(("127.0.0.1", port), handler) as httpd:
        print(f"Public viewer server on http://127.0.0.1:{port}  (allowlisted paths only)")
        print(f"Local check: http://127.0.0.1:{port}/{INDEX}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped.")


if __name__ == "__main__":
    main()
