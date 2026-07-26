# Dashcam Distance-Estimation Benchmark Protocol

**Camera:** DDPAI Mini 5
**Depth model:** Depth Anything V2 (small)
**Goal:** Establish a ground-truth benchmark, in a parking area, for measuring the distance from the front bonnet of the ego vehicle to a lead vehicle in dashcam footage. The benchmark produces (a) a calibrated camera model, (b) ground-plane parameters, and (c) an error table you can use to trust — or distrust — every subsequent on-road distance estimate.

---

## 1. Background and why this benchmark is necessary

### 1.1 Camera parameters (given)

| Parameter | Value |
|---|---|
| Field of view (diagonal) | 140° |
| Aperture | f/1.8 |
| Lens architecture | 7-layer spherical (2G4P — 2 glass + 4 plastic) |
| Image sensor | Sony IMX415, 1/2.8″ |
| Sensor active area | 5.57 mm (H) × 3.13 mm (V) |
| Physical focal length | ~2.5–2.8 mm |
| Pixel pitch (at 4K) | ~1.45 µm |

### 1.2 The lens is NOT a pinhole camera

For a rectilinear (pinhole) lens, a 140° diagonal FOV on a 6.39 mm-diagonal sensor requires a focal length of about **1.16 mm**. The stated 2.5–2.8 mm is only consistent with a **fisheye (equidistant) projection**, where `r = f · θ`. At f = 2.65 mm, the half-diagonal angle is ~69°, i.e., ~138° diagonal — matching the spec.

**Consequences:**
- Simple pinhole distance formulas are only valid near the image center.
- Objects near the frame edges are compressed and distorted.
- All geometry math must be preceded by **fisheye undistortion**.
- The lead vehicle directly ahead sits near the optical center, where pinhole assumptions are approximately valid — this is the friendly case.

### 1.3 Focal length in pixels (starting estimate)

At native 4K recording:

```
f_px ≈ 2.65 mm / 1.45 µm ≈ 1830 pixels
```

Scale proportionally for other resolutions: multiply by 0.5 for 1080p (1920-wide), by 0.75 for 1440p, etc. This is only an **estimate** — the true value must come from Phase 1 calibration.

### 1.4 The Depth Anything V2 (small) scale problem

The standard DA-V2 small checkpoint outputs **relative inverse depth** — an arbitrary affine transform of true disparity. It reveals ordering (A is closer than B) but not absolute distance (A is 12.4 m away). To convert its output to meters, you need **metric anchors** derived from geometry — and that is precisely what this benchmark provides.

### 1.5 Three complementary distance-estimation routes

The benchmark simultaneously validates all three, because each is strongest in different conditions:

**Route 1 — Ground-plane geometry.** For a pixel at row `v` where a tire touches the road, camera height `h`, horizon row `v₀`, focal length `f_px`:

```
Z = f_px · h / (v − v₀)
```

Strong on flat ground with a visible contact point. Fails on hills, dips, and when contact points are occluded.

**Route 2 — Known object width.** For a detected lead vehicle (bounding-box width `w_px`), assuming typical car width `W ≈ 1.8 m`:

**Car Specs** (_on which dashcam is installed_)
Car is a i20 Asta (2017) model. 

Length *Width *Height
3985 mm * 1734 mm * 1505 mm

Height of camera from ground: 1300mm

Bonnet lenth: 1000m 

```
Z = f_px · W / w_px
```

Works on non-flat ground. ±10–15% error because real car widths vary 1.6–2.1 m.

**Route 3 — Metric scaling of the DA-V2 depth map.** Per frame, fit `d_DA ≈ a · (1/Z) + b` using anchors from Routes 1–2, then invert:

```
Z(pixel) = 1 / ((d_DA − b) / a)
```

Produces dense, per-pixel metric depth over the whole frame. Must be refit per frame (or per short window) because DA-V2's scale/shift drifts.

**Final adjustment for all routes:**

```
gap_to_lead = Z − camera_to_bumper_offset
```

The camera sits 1.6–2.0 m behind the front bumper on most cars; measure yours precisely once.

---

## 2. Equipment checklist

- Tape measure (30 m preferred) or laser distance measurer
- Masking tape or chalk for ground marks
- Printed checkerboard: **9 × 6 inner corners**, square size ≥ 30 mm, mounted rigid and flat (foam board, clipboard, or plywood — a floppy sheet ruins calibration)
- Second vehicle whose width you have physically measured, OR a large box of known width + a person for scale
- Spirit level (or a phone app) to verify the parking area is flat
- Plumb line: any weighted string
- Your car in normal-driving trim (tire pressure, typical passenger load)
- Notebook or phone for logging measurements — do not trust memory
- ~45–60 minutes and, ideally, one helper

---

## 3. Phase 0 — Fix the setup before anything else

Every downstream parameter is void if the camera moves after this phase. Do these once, carefully.

### 3.1 Mount the camera in its final driving position

Mount the DDPAI Mini 5 in the exact position you use on trips. Never adjust it again during or after calibration. If you must remount later, the entire calibration is invalidated and Phase 1 + Phase 2 must be re-run.

### 3.2 Lock the recording resolution

Set the recording resolution to what you actually use on trips. Calibration done at 4K does not transfer to 1080p without careful rescaling. It is far safer to just calibrate at your real driving resolution.

### 3.3 Fixed measurements (record once, keep forever)

With the car on level pavement, normal tire pressure, and typical daily load:

| Measurement | How to take it | Expected range |
|---|---|---|
| **Camera height `h`** | Vertical distance from the lens center to the ground | 1.2 – 1.4 m |
| **Camera-to-bumper offset** | Drop a plumb line from the lens, mark the point on the ground, then measure horizontally from that mark to the frontmost point of the bumper | 1.6 – 2.0 m |
| **Lateral offset from centerline** | Distance from lens to the longitudinal centerline of the car | Usually 0 – 0.3 m |

Record these numerically. They enter every distance calculation downstream.

---

## 4. Phase 1 — Intrinsic (lens) calibration

Goal: replace the estimated `f_px ≈ 1830`, principal point, and distortion coefficients with real, measured values using OpenCV's fisheye model.

### 4.1 Capture the checkerboard clip

1. Have a helper hold the checkerboard at distances of ~1–3 m from the camera.
2. Record 2–3 minutes of continuous video while the helper slowly moves and rotates the board so it appears in:
   - The **center** of the frame
   - All **four corners**
   - All **four edges** (top, bottom, left, right)
   - At varied **tilt angles** (yaw, pitch, roll — not just facing straight)
3. **Edge coverage is critical.** Fisheye distortion lives at the edges, and under-sampling there is the most common cause of a bad calibration.
4. Keep the board flat and rigid throughout — any bending introduces errors that mimic distortion.

### 4.2 Extract frames and calibrate

1. Extract ~30–50 sharp frames covering the full spatial distribution above.
2. Use `cv2.findChessboardCorners` to detect corners in each frame.
3. Run `cv2.fisheye.calibrate` to solve for:
   - Focal length in pixels: `f_x`, `f_y` (should be nearly equal)
   - Principal point: `c_x`, `c_y` (should sit near image center)
   - Distortion coefficients: `k1, k2, k3, k4`
4. Sanity checks:
   - **Reprojection error < 0.5 px** (ideally < 0.3 px)
   - Recovered focal length equivalent lands in the 2.5–2.8 mm range
   - Principal point within ~5% of image center

### 4.3 Save the calibration

Serialize the calibration matrix and distortion coefficients (`.npz` or `.yaml`). Every subsequent analysis begins by loading these and undistorting frames with `cv2.fisheye.undistortImage`.

---

## 5. Phase 2 — Ground-truth distance ladder

Goal: create a set of static clips of a target vehicle at precisely known distances, so every distance-estimation method can be scored against tape truth.

### 5.1 Choose the site

Pick a flat, straight stretch of the parking area with at least 30 m of clear space directly ahead of the parked ego vehicle. Confirm flatness:

- Roll a ball gently across the surface — it should not accelerate.
- Or use a spirit level / phone level app at several points.

**Slope is the single biggest silent source of ground-plane error.** A 2° slope over 20 m produces a distance error of ~0.7 m through pitched-camera geometry. Do not skip this check.

### 5.2 Mark the distance ladder

1. Locate the **bumper's ground projection** (the plumb-line point from Phase 0) — this is your zero.
2. From that point, along the car's forward axis, tape or chalk marks at:

   **2 m, 3 m, 5 m, 7 m, 10 m, 15 m, 20 m, 30 m**

   (extend farther if space allows).
3. **Log whether each mark is measured from bumper or from camera.** Convert consistently using the camera-to-bumper offset from Phase 0. Mixing these two references is the classic blunder that quietly biases the whole benchmark.

### 5.3 Static target captures (centered)

1. Measure the **actual width** of the target vehicle. Do not assume 1.8 m — record the real number.
2. Park the target with its **rear bumper exactly on each mark**, facing away from the ego camera, centered on the ego vehicle's forward axis.
3. Record **10–15 seconds of static footage** at each mark. Static footage lets you average across many frames to suppress noise later.
4. If a second car is not available, substitute:
   - A person standing on each mark (gives a clean ground-contact point)
   - A large box of measured width (gives a clean width reference)
   - Cars are best because they are your actual target class, but any object with a crisp contact point and known width works.

### 5.4 Off-axis captures (test distortion effects)

Repeat captures at **5 m, 10 m, 20 m** with the target offset laterally 2–3 m from the ego centerline. These frames test whether accuracy degrades away from the image center — the region where fisheye distortion matters most.

### 5.5 Empty-lane capture (horizon anchor)

Record one clip of the empty marked lane with no target vehicle. The chalk marks themselves become perfect ground-plane anchors: you know each mark's exact distance, so you can read its pixel row `v` directly from the frame and fit the horizon parameter `v₀` precisely.

---

## 6. Phase 3 — Sensitivity and condition checks

These extra ~10 minutes reveal how the benchmark degrades under real-world variation.

### 6.1 Pitch sensitivity (load test)

1. Take the baseline 10 m capture with your normal daily load.
2. Add mass: have your helper(s) sit in the car, load the boot with typical trip cargo.
3. Re-record the 10 m capture.
4. Compare the horizon row `v₀` between the two — it will shift by several pixels. This quantifies how much passenger and cargo load moves the effective horizon, which matters because you calibrate under one condition but drive under another.

### 6.2 Lighting variation

If feasible, repeat captures at **5 m, 10 m, 20 m** at dusk and at night. Depth Anything V2's output quality shifts significantly with lighting; the benchmark should tell you whether the scale-fit degrades and by how much.

### 6.3 Continuous drive-past (temporal stability)

Drive the ego vehicle toward the parked target at **walking pace** from ~30 m to ~5 m. This produces a continuous ground-truth trajectory (distance decreases roughly linearly with constant speed), useful for evaluating:

- **Frame-to-frame jitter** in estimated distance (as important as absolute accuracy for driving-skill inference)
- **Temporal smoothness** of the DA-V2 scale fit
- Whether the pipeline produces sudden jumps that would falsely trigger event detection

---

## 7. Phase 4 — Processing and scoring

### 7.1 Undistort everything

Load the Phase 1 calibration. Run `cv2.fisheye.undistortImage` on every frame from Phase 2 and Phase 3 before any downstream step. All subsequent pixel measurements refer to undistorted frames.

### 7.2 Fit the horizon row `v₀`

Using the empty-lane clip:

1. Read the pixel row `v_i` at which each chalk mark `i` appears.
2. You know the true distance `Z_i` for each mark.
3. Solve `Z_i = f_px · h / (v_i − v₀)` for `v₀` via least squares over all marks.

This is far more accurate than eyeballing the horizon or estimating it from the vanishing point of lane lines in a single frame.

### 7.3 Run the three methods on every static clip

For each Phase 2 static clip:

1. Detect the target vehicle (YOLO or similar) to get its bounding box.
2. Extract the tire ground-contact point (bottom-center of the box, with a small refinement to the actual contact pixel).
3. Compute:
   - `Z_ground` from Route 1 (ground-plane)
   - `Z_width` from Route 2 (known width), using the **measured** target width
   - `Z_da` from Route 3 (DA-V2 scale-fit), using the chalk marks + contact points as anchors
4. Subtract the camera-to-bumper offset from each to get **gap to lead**.

### 7.4 Build the error table

Produce a table like this (one row per capture):

| True distance | Position | Lighting | Z_ground | err % | Z_width | err % | Z_da | err % |
|---|---|---|---|---|---|---|---|---|
| 5 m | center | day | ... | ... | ... | ... | ... | ... |
| 5 m | offset | day | ... | ... | ... | ... | ... | ... |
| 10 m | center | day | ... | ... | ... | ... | ... | ... |
| 10 m | center | dusk | ... | ... | ... | ... | ... | ... |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

**Report error as percentage, not absolute meters.** A 0.5 m error at 5 m is bad (10%); the same error at 30 m is excellent (1.7%).

### 7.5 Target accuracy (rules of thumb)

| Method | Expected accuracy | Fails when |
|---|---|---|
| Ground-plane | ~5% out to 20 m on flat ground | Slopes, dips, occluded contact point |
| Known-width | ~10% at all distances | Non-standard vehicle widths, partial occlusion |
| DA-V2 scale-fit | Between the two, degrades toward edges | Poor lighting, texture-poor scenes |

Use the table to pick, per regime, which method to trust — and consider **fusing** all three at inference time (weighted average or a Kalman filter across frames).

### 7.6 Freeze the benchmark

Save into version control or a labeled folder:

- The intrinsic calibration file (`.npz` / `.yaml`)
- Phase 0 physical measurements
- The horizon-fit parameter `v₀` (baseline + loaded)
- Raw captures for Phase 2 and Phase 3
- Per-frame annotations (bounding boxes, contact points)
- The final error table

**Re-run the benchmark any time you:**
- Remount or bump the camera
- Change recording resolution
- Change vehicles
- Swap the depth model or update its version
- Suspect drift in on-road distance estimates

---

## 8. Code skeleton

```python
import numpy as np
import cv2

# ---------- Constants from Phase 0 + Phase 1 ----------
F_PX = 1830              # Replace with calibrated value from Phase 1
CAM_H = 1.30             # Camera height in meters (Phase 0)
V0 = 1080                # Horizon row in undistorted frame (Phase 4.2)
BUMPER_OFFSET = 1.80     # Camera-to-bumper offset in meters (Phase 0)

# Fisheye intrinsics loaded from Phase 1
K = np.load("calib_K.npy")
D = np.load("calib_D.npy")

def undistort(frame):
    return cv2.fisheye.undistortImage(frame, K, D=D, Knew=K)

# ---------- Route 1: Ground plane ----------
def ground_plane_z(v_contact):
    """Distance from camera to ground point at pixel row v_contact."""
    return F_PX * CAM_H / (v_contact - V0)

# ---------- Route 2: Known object width ----------
def width_z(bbox_w_px, real_w=1.8):
    """Distance based on bounding-box width in pixels and real width in meters."""
    return F_PX * real_w / bbox_w_px

# ---------- Route 3: DA-V2 scale fit ----------
def fit_scale(da_map, anchors):
    """
    anchors : list of (u, v, Z_metric)
    Returns dense metric depth map in meters.
    """
    d = np.array([da_map[v, u] for u, v, _ in anchors])
    inv_z = np.array([1.0 / z for _, _, z in anchors])
    a, b = np.polyfit(inv_z, d, 1)
    with np.errstate(divide="ignore"):
        return a / (da_map - b)

# ---------- Final gap-to-lead ----------
def gap_to_lead(Z):
    return Z - BUMPER_OFFSET
```

---

## 9. On-road interpretation of benchmark numbers

The parking lot is flat. Real roads are not. Crests and dips violate the ground-plane assumption and can throw Route 1 off by 20–30% momentarily — which is exactly when Route 2 (width) and Route 3 (DA-V2 relative structure) serve as cross-checks.

**Treat the benchmark's error numbers as the best-case error floor.** On-road performance is that floor **plus** terrain effects, weather, motion blur, and lighting variation not present in your parking lot session. This is not a failure of the benchmark — it is the correct interpretation. A pipeline that is 5% accurate in the lot might be 10–15% accurate on the highway, and the benchmark tells you which components (which method, which distance range, which conditions) are the weakest link to attack next.
