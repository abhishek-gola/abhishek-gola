# Abhishek Gola

**OpenCV Maintainer · Senior Computer Vision Engineer**

I'm an OpenCV maintainer working on the DNN engine, execution architecture, ONNX operator support, and CPU/CUDA performance. As a Senior Computer Vision Engineer at Bigvision, I also build 3D perception systems for reconstruction, localization, and camera–IMU calibration.

<!--STATS:start-->
So far that's **140 merged pull requests** across the OpenCV organisation and **444** more reviewed.
<!--STATS:end-->

## Selected OpenCV contributions

- **Execution architecture:** Separated graph nodes from executors and added per-operator backend dispatch and CUDA execution. [PR #29286](https://github.com/opencv/opencv/pull/29286)
- **Inference performance:** Optimized convolution layouts, attention fusion, and LSTM execution. Selected results below.
- **Learned features:** Added the DISK feature extractor, with regression tests and accompanying test data. [PR #29073](https://github.com/opencv/opencv/pull/29073)

| Workload | Before → after | Implementation |
| --- | --- | --- |
| ResNet50 | 14 → 7.6 ms | [Convolution block layout](https://github.com/opencv/opencv/pull/28691) |
| BERT | 26.3 → 9.15 ms | [Attention fusion and thin GEMM](https://github.com/opencv/opencv/pull/28859) |
| CRNN LSTM | 17.5 → 2.8 ms | [LSTM optimization](https://github.com/opencv/opencv/pull/29673) |

CPU measurements on an Intel i9-14900KS using default thread settings. These are results for the linked workloads and configurations; see each PR for details.

### ONNX coverage

<!--ONNX:start-->
OpenCV currently passes **89%** of the 1792-test ONNX conformance suite (1589 of 1792),
<!--ONNX:end-->
up from 37% in September 2025, when I imported the complete suite. Subsequent work includes [If](https://github.com/opencv/opencv/pull/27508), [Loop](https://github.com/opencv/opencv/pull/28121), and [Scan](https://github.com/opencv/opencv/pull/29577) operator support.

## 3D perception and calibration

- **Multi-room reconstruction and localization:** Built a system achieving under **1° rotation error** and **1.5 cm position error** across a full home, registering room sub-maps into a metric world frame and evaluating against ArUco ground truth.
- **Visual-inertial tracking:** Fuse monocular video and IMU data, including camera–IMU extrinsics and time synchronization.
- **Public projects:** [hazard-detector](https://github.com/abhishek-gola/hazard-detector) · [spatial_query_engine](https://github.com/abhishek-gola/spatial_query_engine)

I also mentor OpenCV GSoC projects in SLAM, 3D visualization, and learned feature matching.

**[calibsense](https://github.com/calibsense/calibsense)** translates camera-calibration uncertainty into measurement error in millimetres. It diagnoses poorly constrained parameters and flags cases where the available evidence cannot support a reliable forecast.

[Documentation](https://calibsense.github.io/calibsense/) · [PyPI](https://pypi.org/project/calibsense/)

## Selected writing

- **[VGGT vs. VGGT-Ω: A Complete Guide to Feed-Forward 3D Reconstruction](https://learnopencv.com/vggt-vs-vggt-%CF%89-vggt-omega-a-complete-guide-to-feed-forward-3d-reconstruction/)** — LearnOpenCV, August 2026.
- **[Accelerating OpenCV on Graviton: the COOL Framework](https://web.archive.org/web/20260630020243/https://aws.amazon.com/blogs/physical-ai/accelerating-opencv-on-graviton-the-cool-framework/)** (archived) — AWS Physical AI Blog, April 2026.

## Contact

[abhishekg5422@gmail.com](mailto:abhishekg5422@gmail.com)
