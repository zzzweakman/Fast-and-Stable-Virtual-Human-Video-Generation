# Single-H200 runtime and memory results

Measured on 15 October 2026; public release 16 October 2026.

This release contains **44 published implementation results and five blank pending entries**. MuseTalk and VideoReTalking await remeasurement. SoulX-LiveAct, SoulX-FlashTalk, and SoulX-FlashHead await measurement; the FlashHead variant will be specified with its results. All numerical and run-configuration fields for these five entries are `null` in JSON and empty in CSV. They are excluded from the published-result count. No missing value is represented by zero.

The published results cover nine GAN, ten diffusion, 24 appearance-reuse/render implementations, and one UniLS motion visualization. The visualization does not measure a photorealistic generator. No native visual-AR implementation is measured. These runs are a tested subset of the survey, not an exhaustive benchmark.

## Environment and procedure

Each run uses one NVIDIA H200 (140.40 GiB reported device memory) on an eight-H200 host with two Intel Xeon Platinum 8558 CPUs. Up to eight workers execute on different GPUs with disjoint sets of 20 logical CPUs; numerical-library thread counts are four. Host memory and storage remain shared, NUMA locality varies, and no memory binding is recorded. A post-run inventory supplements the records; this is not a continuous hardware trace. The host uses Ubuntu 22.04.4, Linux 5.15, and NVIDIA driver 570.124.06.

Each implementation completes one warm-up run, followed by one measured run in a fresh process. Filesystem and compilation caches may persist; the model does not remain resident. Values are individual observations, with no run-to-run variation estimate. CUDA work is synchronized at stage boundaries. Inputs, generated lengths, resolution, dependencies, precision, attention paths, compilation and offloading differ; the machine is shared but software is not uniform.

## Fields

| Field | Meaning |
|---|---|
| `frames` | Actual completed output frames across all generated chunks. |
| `output_width`, `output_height` | Output region after cropping/paste-back, excluding comparison panels; a composited canvas can exceed the internal synthesis crop. |
| `pre_s`, `generation_s`, `post_s` | Implementation-specific stages, in seconds. Dense-diffusion VAE decoding is generally in Post; appearance-reuse generation includes motion prediction and rendering. |
| `load_s` | Model initialization and loading. |
| `process_s` | Complete measured process, including loading and other overhead; not TTFF or the sum of stages. |
| `nvml_peak_gib` | Peak process-tree memory sampled every 100 ms across the whole process, in GiB. Includes loading and auxiliary stages; can miss brief allocations. Not a minimum device-capacity requirement. |
| `torch_allocated_peak_gib`, `torch_reserved_peak_gib` | Separate framework counters. Some exceed sampled NVML peaks; neither counter is substituted for the other. |
| `stage_union_s`, `stage_overlap_s` | Union and overlap of timed phase intervals; overlapping stages must not be added as elapsed time. |
| `evaluation_s` | Additional evaluation outside the three inference stages. |
| `duration_s`, `video_fps` | Encoded media duration and playback frame rate, not inference performance. |
| `encoded_width`, `encoded_height` | Encoded canvas, including any comparison panels. |
| `input_configuration`, `stage_definition` | Supplied demo configuration, prerequisites, and stage boundaries. |
| `code_commit`, `torch_version`, `attention_backend` | Recorded implementation revision and software observations; the commit does not capture all local instrumentation. |

## Configuration exceptions

Ditto and TalkLikeYou have overlapping threaded stages and exclude queue waits from operator times. SyncTalk's process and memory include an additional evaluation pass outside the three inference phases. Wan-Animate-2 times the active worker, excluding its waiting launcher, and crops native frames for output. StyleAvatar uses two output frames and full tracking, with a PyTorch allocator ceiling and separate Jittor allocation. LeapTalk uses one chunk; TaoMate uses one window; Avatar-Forever uses a short output. Supplied trained assets, landmarks, tracks, and audio features are excluded where accepted as demo prerequisites. LAM and StyleAvatar instead include fresh tracking; GUAVA retains internal reconstruction/render warm-ups.

Moore-AnimateAnyone and face-vid2vid-unofficial are third-party implementations. RAD-NeRF uses the repository's PyTorch reimplementation. SplattingAvatar uses the Python evaluation path, not its separately reported optimized Unity implementation. UniLS predicts motion; FLAME decoding, rendering, smoothing and export are in Post. Per-run descriptions in the downloads retain the remaining distinctions.

## Interpretation

The results identify where time is spent within a recorded configuration. They do not support a controlled method ranking, a reproduction ratio against author-reported rates, or conclusions about visual quality or long-session drift. Streaming TTFF, delivery jitter, resident-service throughput and matched quality were not measured. Runtime and memory summaries alone do not establish temporal stability. Original author-reported values remain in the literature catalogue under their own conditions.

Web tables show two decimal places; downloads retain the supplied precision. This public release was prepared from supplied measurement summaries; no additional inference was run during publication.
