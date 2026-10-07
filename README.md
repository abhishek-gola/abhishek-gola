## Abhishek Gola

I work on two things.

**3D perception.** Reconstruction, localization, visual-inertial fusion and sensor
calibration. A room-by-room indoor system that registers per-room sub-maps into a
single metric world frame, under 1 degree and 1.5 cm localization error across a full
multi-room home. Monocular video fused with IMU for scale-consistent, gravity-aligned
tracking. Road footage turned into a navigable physics simulation. And
[calibsense](https://github.com/calibsense/calibsense), which computes what a camera
calibration is actually worth in millimetres instead of reporting a reprojection
error that cannot answer the question.

**Inference performance.** I'm a maintainer at
[OpenCV](https://github.com/opencv/opencv), working inside the DNN engine on graph
architecture, ONNX operator coverage, and CPU and CUDA speed. I also review the
point cloud and SLAM module.

The habit that runs through both is worth more than either: measure it, publish the
number that came back, and say so when the data does not support the claim.

<!--STATS:start-->
So far that's **135 merged pull requests** across the OpenCV organisation and **174** more reviewed.
<!--STATS:end-->

---

## 3D perception

### Reconstruction, localization and sensor calibration

**Indoor reconstruction and localization.** Architected a room-by-room system: each
room reconstructed as its own sub-map, then registered into a single metric world
frame by solving the inter-room SE(3) extrinsics against a defined global origin.
**Under 1 degree rotation and 1.5 cm position error across a full multi-room home.**
ArUco fiducials supply known-geometry ground truth, chunk-wise 3D-3D correspondence
and multi-view fusion bring partial scans into one coordinate frame (Open3D), and
drift is measured at every merge step rather than assumed.

**Visual-inertial.** Monocular video fused with accelerometer and gyroscope streams
for scale-consistent, drift-corrected tracking: camera-to-IMU extrinsics,
cross-sensor time synchronisation, gravity-aligned world frames. Extended with
feed-forward DNN SLAM (VGGT, Pi-Long) for the low-texture indoor scenes where
feature-based tracking gives up.

**Sensor and calibration feasibility.** I own the question that comes before the
build: which camera and IMU configuration can actually hit a stated accuracy target.
Then the calibration itself, intrinsics, lens distortion models, multi-camera rig
extrinsics, multi-sensor alignment, with drift and noise characterised against both
reprojection error and fiducial ground truth, and reprojection-error thresholds set
as the acceptance gate for everything downstream.

**Video to simulation.** Road capture footage in, navigable simulation out: recover
intrinsics and per-frame extrinsics, reconstruct the scene as 3D Gaussian splats,
extract a collision mesh from it, apply physics, then place generative assets
(TRELLIS, served over an MCP server) and navigating agents at correct metric scale
for point-to-point traversal.

**The stack, hands on.** ORB-SLAM3, COLMAP, MASt3R, VGGT, Pi-Long, LightGlue,
Open3D, ElasticFusion, ACE Zero, Depth Pro, Kalibr. Built, modified and run against
EuRoC and my own captures, not just imported.

### calibsense

[source](https://github.com/calibsense/calibsense) ·
[PyPI](https://pypi.org/project/calibsense/) ·
[docs](https://calibsense.github.io/calibsense/)

A calibration reporting 0.2 px reprojection error tells you nothing about whether you
can measure a part to half a millimetre. Two calibrations with identical reprojection
error can differ by thousands of pixels in focal length, because the capture geometry
never constrained it.

calibsense keeps the **full factored parameter covariance** rather than the marginal
standard deviations `calibrateCamera` returns, so correlations survive. It finds the
directions the capture left unconstrained by **null-space analysis**, instead of
letting a pseudo-inverse quietly assign them zero variance. It cross-checks a
**view-clustered covariance** against the classical residual-based one, which catches
spatially correlated detection noise that otherwise inflates confidence. Then it
**propagates into task space**: a 100 mm feature at 800 mm reads 0.199 mm expected
error, ±0.485 mm at 95%, with the variance split between calibration and
measurement-time pixel noise.

It names what the capture is missing, coverage gaps, insufficient depth variation,
frontoparallel dominance, and prescribes the fix. It refuses to print figures it
cannot stand behind.

Hand-eye calibration with board-tolerance and robot-repeatability terms folded into
the covariance. ChArUco, checkerboard and circle-grid ingest, including circle-grid
centroid bias and half-turn checkerboard detection. JSON, PDF and self-contained HTML
reports. Written, tested and maintained solo.

### In OpenCV

- **[DISK learned feature extractor](https://github.com/opencv/opencv/pull/29073)** in
  the `features` module, with regression tests and
  [test data](https://github.com/opencv/opencv_extra/pull/1368).
- I review and merge OpenCV's **point cloud and SLAM** work: visual odometry, loop
  closure, bundle adjustment, surface reconstruction, 3D visualisation. Roughly a
  quarter of my review comments are on `ptcloud`, `geometry` and `features`.
- GSoC 2026 mentor for **Modular SLAM**, a **lightweight 3D viewer with PLY and point
  cloud I/O**, and an **end-to-end learned feature extraction and LightGlue matching
  pipeline**.

### Writing

**[VGGT vs VGGT-Ω: A Complete Guide to Feed-Forward 3D Reconstruction](https://learnopencv.com/vggt-vs-vggt-%CF%89-vggt-omega-a-complete-guide-to-feed-forward-3d-reconstruction/)**,
LearnOpenCV, August 2026. Both models on the same 4K sequence and the same RTX 5090,
timed with `torch.cuda.synchronize()`: speed, GPU memory, frame-count scaling, depth
quality. Co-author with Yashpreet Singh.

---

## Inference engine and performance

### Architecture

| | |
|---|---|
| [#29286](https://github.com/opencv/opencv/pull/29286) | Split the layer abstraction into graph node and executor, added per-operator backend dispatch, and brought CUDA into the new engine with on-device residency. ResNet50 runs end to end on CUDA at 1.17 ms FP16. |
| [#29341](https://github.com/opencv/opencv/pull/29341) | Removed the legacy DNN engine and made the new graph engine the default. |
| [#30081](https://github.com/opencv/opencv/pull/30081) | A unified N-dimensional data-movement engine in `core`, so `dnn` and the rest of the library stop carrying separate copies of the same machinery. |
| [#28963](https://github.com/opencv/opencv/pull/28963) | Custom layer support in the new engine. |
| [#28444](https://github.com/opencv/opencv/pull/28444) | ONNX Runtime as an optional execution engine. |

### Performance

| | |
|---|---|
| [#28691](https://github.com/opencv/opencv/pull/28691) | Block layout for 1x1 and 3x3 convolution. ResNet50 14 ms &rarr; 7.6 ms. |
| [#28741](https://github.com/opencv/opencv/pull/28741) | Int8 block layout. ResNet50-QDQ 11.5 ms &rarr; 6.6 ms. |
| [#28859](https://github.com/opencv/opencv/pull/28859) | Attention fusion and thin GEMM. BERT 26.3 ms &rarr; 9.15 ms, against ONNX Runtime's 9.13 ms. |
| [#29126](https://github.com/opencv/opencv/pull/29126) | Attention graph fusion with FlashAttention. OWL-v2 at 1078 ms, against ONNX Runtime's 1411 ms. |
| [#29673](https://github.com/opencv/opencv/pull/29673) | LSTM: batched input projection, weight pre-packing, parallel directions. CRNN 17.5 ms &rarr; 2.8 ms. |
| [#29642](https://github.com/opencv/opencv/pull/29642) | `reserveKVCache()` for LLM decode. Qwen2.5-0.5B at 512 tokens: 4.25 &rarr; 21.03 tok/s. |

Measured on an i9-14900KS with threads pinned to P-cores, best of several runs, `min`
from the test XML. Every number is reproducible from the linked pull request. Also
[chunk-level parallelism](https://github.com/opencv/opencv/pull/28821) replacing
tensor-level `parallel_for_`, and
[MLAS in the GEMM path](https://github.com/opencv/opencv/pull/28934).

### ONNX coverage

<!--ONNX:start-->
OpenCV currently passes **87%** of the 1792-test ONNX conformance suite (1552 of 1792),
<!--ONNX:end-->
up from 37% in September 2025, when I imported the complete conformance suite and the
gaps it had been hiding became visible.

Getting there meant implementing around fifty operators: the control-flow ones
([If](https://github.com/opencv/opencv/pull/27508),
[Loop](https://github.com/opencv/opencv/pull/28121),
[Scan](https://github.com/opencv/opencv/pull/29577)), the attention family
([SDPA](https://github.com/opencv/opencv/pull/29104),
[linear and flex attention](https://github.com/opencv/opencv/pull/29624)), and the
exotic numeric casts
([FP8, FP4, INT4, UINT4, E8M0](https://github.com/opencv/opencv/pull/29360), plus
[FP8 models](https://github.com/opencv/opencv/pull/29834) end to end).

---

## Elsewhere

- **Accelerating OpenCV on Graviton: the COOL Framework**, AWS Physical AI Blog,
  April 2026. Co-author with Satya Mallick, Frantz Lohier, Gursimar Singh and Phil
  Nelson. *(AWS moved the blog and the original link is currently broken;
  [archived copy](https://web.archive.org/web/20260630020243/https://aws.amazon.com/blogs/physical-ai/accelerating-opencv-on-graviton-the-cool-framework/).)*
- Four OpenCV webinars, including one on building an automated code review system.
- Co-presented the OpenCV 5 launch preview on behalf of OpenCV.org.

A note on how I work. I publish the losses. The ONNX pass rate dropped from 72% to
37% the day I imported the full suite, because the old number was measuring a test
set that skipped the failures. My OpenCV-versus-ONNX-Runtime benchmark rig currently
reports OpenCV behind on four models out of six. calibsense will tell you it cannot
make the forecast you asked for. I keep the optimizations that did not work written
down next to the ones that did.

:mailbox: abhishekg5422@gmail.com
