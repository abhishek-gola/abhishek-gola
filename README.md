## Abhishek Gola

**Computer Vision Engineer · OpenCV Maintainer**

I build **3D perception systems** and make **inference engines faster**. My work spans SLAM, reconstruction, camera–IMU calibration, ONNX operator coverage, and CPU/CUDA optimization.

### Selected impact

- **OpenCV:** Maintainer working on the DNN engine, graph architecture, ONNX coverage, and CPU/CUDA performance.
- **3D perception:** Built a multi-room reconstruction and localization system with under **1° rotation error** and **1.5 cm position error** across a full home.
- **Inference:** Improved ResNet50 from **14 ms to 7.6 ms**, BERT from **26.3 ms to 9.15 ms**, and CRNN LSTM from **17.5 ms to 2.8 ms**.
- **ONNX:** Helped raise OpenCV's conformance pass rate from **37% to 87%**.
- **Calibration:** Created [calibsense](https://github.com/calibsense/calibsense), which translates calibration uncertainty into task-space error in millimetres.

Across both areas, I work the same way: measure the result, publish it, and state clearly when the evidence does not support a claim.

<!--STATS:start-->
So far that's **135 merged pull requests** across the OpenCV organisation and **174** more reviewed.
<!--STATS:end-->

---

## 3D perception

### Reconstruction, localization and sensor calibration

**Indoor reconstruction and localization.** I architected a room-by-room system that registers independently reconstructed sub-maps into one metric world frame by solving inter-room SE(3) extrinsics. ArUco ground truth and multi-view fusion keep drift measurable at every merge step.

**Visual-inertial tracking.** I fuse monocular video with IMU streams for scale-consistent, gravity-aligned tracking, including camera-to-IMU extrinsics and time synchronization. I also use VGGT and Pi-Long in low-texture scenes where feature-based tracking fails.

**Sensor and calibration feasibility.** Before implementation, I evaluate whether a proposed camera and IMU configuration can meet the required accuracy, then validate its calibration against reprojection error and fiducial ground truth.

**Video to simulation.** I turn road footage into metric, navigable simulations using recovered camera geometry, 3D Gaussian splats, collision meshes, physics, and generated assets.

Hands-on stack: ORB-SLAM3, COLMAP, MASt3R, VGGT, Pi-Long, LightGlue, Open3D, ElasticFusion, ACE Zero, Depth Pro, and Kalibr—built, modified, and evaluated on EuRoC and proprietary captures.

### calibsense

[Source](https://github.com/calibsense/calibsense) · [PyPI](https://pypi.org/project/calibsense/) · [Documentation](https://calibsense.github.io/calibsense/)

A reprojection error does not tell you whether a system can measure a part to half a millimetre. **calibsense** retains the full factored parameter covariance, identifies unconstrained directions through null-space analysis, and propagates uncertainty into task space. A 100 mm feature at 800 mm, for example, may read 0.199 mm expected error and ±0.485 mm at 95% confidence. When the evidence is insufficient, it reports that no defensible forecast can be made.

It supports hand-eye calibration, ChArUco, checkerboard and circle-grid input, and JSON, PDF, and self-contained HTML reports.

### OpenCV 3D work

- Added the [DISK learned feature extractor](https://github.com/opencv/opencv/pull/29073), including regression tests and [test data](https://github.com/opencv/opencv_extra/pull/1368).
- Review and merge work across point clouds, SLAM, visual odometry, loop closure, bundle adjustment, surface reconstruction, and 3D visualization.
- GSoC 2026 mentor for Modular SLAM, a lightweight 3D viewer, and a learned feature extraction and LightGlue matching pipeline.

---

## Inference engine and performance

### Architecture

- [#29286](https://github.com/opencv/opencv/pull/29286): Split graph nodes from executors, added per-operator backend dispatch, and brought CUDA into the new engine with on-device residency. ResNet50 runs end to end at **1.17 ms FP16**.
- [#29341](https://github.com/opencv/opencv/pull/29341): Removed the legacy DNN engine and made the new graph engine the default.
- [#30081](https://github.com/opencv/opencv/pull/30081): Added a unified N-dimensional data-movement engine in `core`.
- Also added [custom-layer support](https://github.com/opencv/opencv/pull/28963) and [ONNX Runtime](https://github.com/opencv/opencv/pull/28444) as an optional execution engine.

### Performance

| Work | Result |
|---|---|
| [Convolution block layout](https://github.com/opencv/opencv/pull/28691) | ResNet50: **14 → 7.6 ms** |
| [INT8 block layout](https://github.com/opencv/opencv/pull/28741) | ResNet50-QDQ: **11.5 → 6.6 ms** |
| [Attention fusion and thin GEMM](https://github.com/opencv/opencv/pull/28859) | BERT: **26.3 → 9.15 ms** |
| [FlashAttention graph fusion](https://github.com/opencv/opencv/pull/29126) | OWL-v2: **1078 ms**, versus ONNX Runtime at 1411 ms |
| [LSTM optimization](https://github.com/opencv/opencv/pull/29673) | CRNN: **17.5 → 2.8 ms** |
| [`reserveKVCache()`](https://github.com/opencv/opencv/pull/29642) | Qwen2.5-0.5B: **4.25 → 21.03 tok/s** at 512 tokens |

CPU results were measured on an i9-14900KS with threads pinned to P-cores. Each result is reproducible from its linked pull request.

### ONNX coverage

<!--ONNX:start-->
OpenCV currently passes **87%** of the 1792-test ONNX conformance suite (1552 of 1792),
<!--ONNX:end-->
up from 37% in September 2025, when I imported the complete suite and exposed the cases the earlier test set had skipped.

The work included control flow ([If](https://github.com/opencv/opencv/pull/27508), [Loop](https://github.com/opencv/opencv/pull/28121), [Scan](https://github.com/opencv/opencv/pull/29577)), [attention](https://github.com/opencv/opencv/pull/29104), and [low-bit numeric formats](https://github.com/opencv/opencv/pull/29360).

---

## Writing and talks

- **[VGGT vs VGGT-Ω: A Complete Guide to Feed-Forward 3D Reconstruction](https://learnopencv.com/vggt-vs-vggt-%CF%89-vggt-omega-a-complete-guide-to-feed-forward-3d-reconstruction/)** — LearnOpenCV, August 2026. Both models evaluated on the same 4K sequence and RTX 5090.
- **[Accelerating OpenCV on Graviton: the COOL Framework](https://web.archive.org/web/20260630020243/https://aws.amazon.com/blogs/physical-ai/accelerating-opencv-on-graviton-the-cool-framework/)** — AWS Physical AI Blog, April 2026.
- Four OpenCV webinars and the OpenCV 5 launch preview.

I publish negative results as well as wins: failed optimizations, benchmark regressions, and cases where the available data cannot support a reliable claim.

:mailbox: abhishekg5422@gmail.com
