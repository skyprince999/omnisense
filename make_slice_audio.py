"""Generate a Sarvam voiceover clip for every amber/red slice's coaching line.

For each slice whose driving_signal is amber or red, this reads the `coaching` key
(the conversational line written by make_slice_coaching.py), synthesizes it with
Sarvam TTS in the "simran" voice, saves the mp3 under nudges/, and records the
filename on a new `coaching_audio` key on that slice. Green slices are skipped.
trip_dist_viewer_v4/v5.html will read `coaching_audio` to play the nudge.

Sarvam's bulbul clips the tail of whatever text is sent last (the real final word
loses its ending). To avoid that, a throwaway sentinel sentence is appended so the
real text is no longer last; the clip then eats the sentinel, which is trimmed back
off at the silence gap before it (via ffmpeg silencedetect). Requires ffmpeg/ffprobe
on PATH. Key comes from .env `SARVAM_API_KEY` / `SARAVAM_API_KEY`, env, or --key.

The run is idempotent/resumable: a slice is skipped if its `coaching_audio` file
already exists (unless --force); files are written atomically (.part -> replace) and
each slices manifest is flushed after every clip so an interrupt never loses work.

Usage:
    python make_slice_audio.py --dry-run          # list what would be generated
    python make_slice_audio.py --limit 3          # smoke test the first 3
    python make_slice_audio.py                     # generate for every amber/red slice
    python make_slice_audio.py --force             # regenerate even existing ones
    python make_slice_audio.py --voice anushka
"""
import argparse
import base64
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLICES_DIR = HERE / "slices"
NUDGES_DIR = HERE / "nudges"

TARGET_SIGNALS = {"amber", "red"}
AUDIO_KEY = "coaching_audio"

# Throwaway sentence appended so bulbul's tail-clip eats it instead of the real last
# word. The leading "..." forces a clear pause we can find and cut on.
SENTINEL = " ... okay."
SILENCE_DB = "-38dB"    # silencedetect noise floor
SILENCE_MIN = "0.12"    # min silence length (s) to count as a gap


def load_key(cli_key):
    if cli_key:
        return cli_key
    for name in ("SARVAM_API_KEY", "SARAVAM_API_KEY", "SARVAM_API_SUBSCRIPTION_KEY"):
        if os.environ.get(name):
            return os.environ[name]
    env = HERE / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            if k.strip() in ("SARVAM_API_KEY", "SARAVAM_API_KEY", "SARVAM_API_SUBSCRIPTION_KEY"):
                return v.strip().strip('"').strip("'")
    return None


def safe_name(stem, idx):
    """Audio filename for a slice: '<stem> s<idx>.mp3'. Stem is already filesystem-safe."""
    return f"{stem} s{idx}.mp3"


def _sarvam_wav(client, text, voice, model, lang, sr):
    """One Sarvam TTS call -> raw WAV bytes, with a single retry."""
    for attempt in range(2):
        try:
            resp = client.text_to_speech.convert(
                text=text,
                target_language_code=lang,
                speaker=voice,
                model=model,
                speech_sample_rate=sr,
                output_audio_codec="wav",
            )
            return b"".join(base64.b64decode(c) for c in resp.audios)
        except Exception:
            if attempt == 0:
                time.sleep(2)
                continue
            raise


def _duration(path):
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path], text=True).strip())


def _trim_point(path, dur):
    """Locate the sentinel as the LAST short speech segment and return the time to cut
    (just inside the silence gap before it). Returns None if there's no clean short
    trailing segment (e.g. the sentinel merged into the last word) -> caller falls back
    to a plain render so nothing leaks."""
    out = subprocess.run(
        ["ffmpeg", "-i", path, "-af",
         f"silencedetect=noise={SILENCE_DB}:d={SILENCE_MIN}", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start:\s*(-?[\d.]+)", out)]
    ends = [float(x) for x in re.findall(r"silence_end:\s*(-?[\d.]+)", out)]
    gaps = [(starts[i], ends[i] if i < len(ends) else dur) for i in range(len(starts))]
    if not gaps:
        return None
    # walk the gaps, recording each speech segment and the gap that precedes it
    segs = []            # (seg_start, seg_end, preceding_gap_start)
    prev, prev_gap_start = 0.0, None
    for gs, ge in gaps:
        if gs > prev + 0.02:
            segs.append((prev, gs, prev_gap_start))
        prev, prev_gap_start = max(prev, ge), gs
    if prev < dur - 0.02:
        segs.append((prev, dur, prev_gap_start))
    if len(segs) < 2:                       # need real content + a separate sentinel
        return None
    seg_start, seg_end, gap_start = segs[-1]
    if gap_start is None or (seg_end - seg_start) > 0.95:  # last seg too long = merged sentinel
        return None
    cut = gap_start + min(0.25, (seg_start - gap_start) * 0.5)   # land inside the gap
    return cut if cut > 0.4 * dur else None


def _encode_mp3(src, dst, sr, cut=None):
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", src]
    if cut is not None:
        cmd += ["-t", f"{cut:.3f}"]
    cmd += ["-ar", str(sr), "-c:a", "libmp3lame", "-q:a", "4", dst]
    subprocess.run(cmd, check=True)


def synth(client, text, voice, model, lang, sample_rate):
    """TTS the coaching line without the bulbul tail-clip: append a sentinel so the
    real text renders fully, then trim the sentinel off at the silence gap. Returns
    mp3 bytes. Falls back to a plain (un-sentinel) render if the gap can't be found."""
    wav = _sarvam_wav(client, text + SENTINEL, voice, model, lang, sample_rate)
    with tempfile.TemporaryDirectory() as td:
        wp = os.path.join(td, "in.wav")
        mp = os.path.join(td, "out.mp3")
        with open(wp, "wb") as fh:
            fh.write(wav)
        dur = _duration(wp)
        cut = _trim_point(wp, dur)
        if cut is not None:
            _encode_mp3(wp, mp, sample_rate, cut=cut)
        else:
            # sentinel didn't separate cleanly: re-render plain so nothing leaks
            wav2 = _sarvam_wav(client, text, voice, model, lang, sample_rate)
            with open(wp, "wb") as fh:
                fh.write(wav2)
            _encode_mp3(wp, mp, sample_rate)
        with open(mp, "rb") as fh:
            return fh.read()


def atomic_bytes(path, data):
    tmp = path.with_suffix(path.suffix + ".part")
    tmp.write_bytes(data)
    tmp.replace(path)


def atomic_json(path, data):
    tmp = path.with_suffix(path.suffix + ".part")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", default="v5", help="slices file version (default v5)")
    ap.add_argument("--voice", default="simran", help="Sarvam speaker (default simran)")
    ap.add_argument("--model", default="bulbul:v3")
    ap.add_argument("--lang", default="en-IN")
    ap.add_argument("--sample-rate", type=int, default=22050)
    ap.add_argument("--force", action="store_true", help="regenerate even if the mp3 exists")
    ap.add_argument("--limit", type=int, default=0, help="generate at most N clips (0 = all)")
    ap.add_argument("--dry-run", action="store_true", help="list targets, synthesize nothing")
    ap.add_argument("--key", default=None)
    args = ap.parse_args()

    suffix = f".slices.{args.version}.json"
    files = sorted(SLICES_DIR.glob(f"*{suffix}"))
    if not files:
        sys.exit(f"No slices/*{suffix} files found.")
    NUDGES_DIR.mkdir(exist_ok=True)

    # enumerate targets (amber/red slices that have coaching text)
    def is_target(s):
        return (s.get("driving_signal") or "").lower() in TARGET_SIGNALS \
            and (s.get("coaching") or "").strip()

    def needs(stem, idx, s):
        if not args.force and (s.get(AUDIO_KEY) or "").strip():
            if (NUDGES_DIR / s[AUDIO_KEY]).exists():
                return False
        return True

    total = 0
    for f in files:
        stem = f.name[: -len(suffix)]
        for i, s in enumerate(json.loads(f.read_text(encoding="utf-8")).get("slices", [])):
            if is_target(s) and needs(stem, i, s):
                total += 1
    print(f"{len(files)} files, {total} amber/red slices to voice"
          + (" (dry run)" if args.dry_run else f" via Sarvam '{args.voice}' / {args.model}"))

    client = None
    if not args.dry_run:
        key = load_key(args.key)
        if not key:
            sys.exit("No Sarvam key. Add SARVAM_API_KEY=... to .env or pass --key.")
        from sarvamai import SarvamAI
        client = SarvamAI(api_subscription_key=key)

    done = errors = 0
    stop = False
    for f in files:
        stem = f.name[: -len(suffix)]
        data = json.loads(f.read_text(encoding="utf-8"))
        changed = False
        for i, s in enumerate(data.get("slices", [])):
            if not is_target(s) or not needs(stem, i, s):
                continue
            name = safe_name(stem, i)
            text = s["coaching"].strip()
            if args.dry_run:
                print(f"  {name}  <-  {text[:70]}")
                done += 1
            else:
                try:
                    audio = synth(client, text, args.voice, args.model, args.lang, args.sample_rate)
                    atomic_bytes(NUDGES_DIR / name, audio)
                    s[AUDIO_KEY] = name
                    changed = True
                    done += 1
                    print(f"[{done}/{total}] {name}  ({len(audio)} bytes)")
                    atomic_json(f, data)  # flush after each so the run is resumable
                except Exception as e:
                    errors += 1
                    print(f"  ! error on {stem} slice {i}: {e}")
            if args.limit and done >= args.limit:
                stop = True
                break
        if changed and not args.dry_run:
            atomic_json(f, data)
        if stop:
            break

    print(f"\nDone: {done} slice audios"
          + (f", {errors} errors" if errors else "")
          + (" (dry run — nothing written)" if args.dry_run else f" -> {NUDGES_DIR.name}/"))


if __name__ == "__main__":
    main()
