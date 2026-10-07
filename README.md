## Abhishek Gola

Maintainer at [OpenCV](https://github.com/opencv/opencv). I work mostly inside the
DNN module's inference engine: the graph execution model, ONNX operator coverage,
and CPU/CUDA performance.

<!--STATS:start-->
So far that's **135 merged pull requests** across the OpenCV organisation and **174** more reviewed.
<!--STATS:end-->

I mentor OpenCV's Google Summer of Code projects
([2026](https://github.com/opencv/opencv/wiki/GSoC_2026): deep-learning feature
extraction and LightGlue matching, VLM inference via ONNX Runtime GenAI, validation
and sample generation for modern DNNs, Modular SLAM, image augmentation, and a
lightweight 3D viewer for SLAM debugging).

### Engine architecture

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
| [#28821](https://github.com/opencv/opencv/pull/28821) | Chunk-level parallelism replacing tensor-level `parallel_for_`. |
| [#28934](https://github.com/opencv/opencv/pull/28934) | MLAS integrated into the GEMM path. |

Measured on an i9-14900KS with threads pinned to P-cores. Every number is reproducible
from the linked pull request.

### ONNX coverage

<!--ONNX:start-->
OpenCV currently passes **87%** of the 1792-test ONNX conformance suite (1552 of 1792),
<!--ONNX:end-->
up from 37% in September 2025, when the complete conformance suite was first imported
and the gaps it exposed became visible.

Getting there meant implementing around fifty operators, including the control-flow
ones ([If](https://github.com/opencv/opencv/pull/27508),
[Loop](https://github.com/opencv/opencv/pull/28121),
[Scan](https://github.com/opencv/opencv/pull/29577)), the attention family
([SDPA](https://github.com/opencv/opencv/pull/29104),
[linear and flex attention](https://github.com/opencv/opencv/pull/29624)), and the
exotic numeric casts
([FP8, FP4, INT4, UINT4, E8M0](https://github.com/opencv/opencv/pull/29360), plus
[FP8 model support](https://github.com/opencv/opencv/pull/29834) end to end).

### Writing and talks

- **Accelerating OpenCV on Graviton: the COOL Framework**, AWS Physical AI Blog, April 2026.
  Co-author with Satya Mallick, Frantz Lohier, Gursimar Singh and Phil Nelson.
  *(AWS moved the blog and the original link is currently broken;
  [archived copy](https://web.archive.org/web/20260630020243/https://aws.amazon.com/blogs/physical-ai/accelerating-opencv-on-graviton-the-cool-framework/).)*
- **[VGGT vs VGGT-&Omega;: A Complete Guide to Feed-Forward 3D Reconstruction](https://learnopencv.com/vggt-vs-vggt-%CF%89-vggt-omega-a-complete-guide-to-feed-forward-3d-reconstruction/)**,
  LearnOpenCV, August 2026. Co-author with Yashpreet Singh.
- Four OpenCV webinars, including one on building an automated code review system.
- Co-presented the OpenCV 5 launch preview on behalf of OpenCV.org.

### Elsewhere

Before OpenCV I worked on 3D vision and reconstruction, and on medical imaging. I still
work that side through GSoC, mentoring the Modular SLAM and 3D viewer projects, and
through the [DISK learned feature extractor](https://github.com/opencv/opencv/pull/29073)
in OpenCV's `features` module.

I care a lot about measurement. Most of what I publish comes with a before and after on
pinned cores, and I keep the optimizations that did not work written down next to the
ones that did.

:mailbox: abhishekg5422@gmail.com
