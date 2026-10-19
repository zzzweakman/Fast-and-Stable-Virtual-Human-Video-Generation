# Single-H200 repeated measurements — 19 October 2026

This release contains **56 configurations covering 55 methods**: 11 GAN, 20 diffusion, 24 rendering, and one motion visualization. FlashHead Lite and Pro are separate configurations of one method. The original 50-configuration main sheet and six additional configurations are both included. All previously pending entries have completed measurements. Native visual-AR coverage is zero; UniLS is motion prediction with FLAME visualization.

## Repetition and workload

Every configuration executes three complete warm-ups followed by three measured calls in the same interpreter: **168 warm-ups + 168 measured calls = 336 calls**. Warm-ups replay the selected complete demo clip, including its declared preparation, generation and output processing. Each call produces a fresh output and rebuilds clip state.

**15 configurations retain audited model objects or a GPU worker; 41 reload models each call.** Retained objects do not imply every auxiliary object is resident. StyleAvatar retains its style generator and stateless ORT sessions but rebuilds FaceVerse fitting state. Wan retains the actual neural GPU worker, not just its controller. Caches may survive between calls; the first call may use existing disk caches. Three warm-ups do not establish convergence for every input shape.

Each configuration uses one H200. Suites run across three nodes, with four CPU-affinity identifiers and numerical-library thread limits of four. Those identifiers do not prove four independent physical cores. Host memory, storage, cache state, software, precision, offloading and implementation settings differ.

Inputs and sampling schedules are unmatched. Supplied tracking, features, masks and subject-trained assets remain prerequisites when the demo expects them. Full sampling/decoder settings for Follow-Your-Emoji-Faster, Hallo-Live, LightningCP, Lip Forcing, Live Avatar and PersonaLive were not included in the workbook. Their measured results are retained without inventing missing settings.

## Times and statistics

| Field | Meaning |
|---|---|
| pre_s / generation_s / post_s | Mean over three measured calls; each phase uses its own event union and implementation-specific synchronized boundaries. |
| *_sd_s | Sample standard deviation (n−1 denominator), calculated from the three full-precision measured values. |
| load_s | Mean recorded per-call loading interval. Null/NR means no interval is supplied, not zero loading cost. |
| call_s | Mean wall time from inference entry to synchronized return, including per-call loading, native validation and unclassified overhead. Generic output QA follows this window. |
| stage_union_s | Mean union of the three inference phases; overlapping operators are counted once. |
| stage_overlap_s | Sum of phase times minus their union. Retained floating-point residuals may be near zero. |
| evaluation_s | Recorded native extra validation. SyncTalk performs this inside Call but outside Pre/Gen/Post. A zero records no such timed event. |
| suite_process_s | Entire 3+3 process: startup/import, setup, all six calls, QA and shutdown. This is **not a single-call measurement or TTFF**. |
| statistics | Per-stage raw values, mean, median, sample SD, minimum and maximum for measured calls. |
| measured_iterations / warmup_iterations | All three calls of each kind, kept separately. |

The suite process total has a different boundary from the 15 October fresh-process measurement. Do not divide it by six or combine old and new records as equivalent latency observations. Ditto and Talk Like You overlap phases, so adding Pre/Gen/Post does not give elapsed time. Stage synchronization can affect asynchronous production behavior.

The table shows time means and Call ± sample SD. CSV/JSON retain all stage SDs. Small positive times below the display precision are shown as <0.01 s; unavailable values display NR and export as JSON null / empty CSV cells.

## Memory windows

| Field | Meaning |
|---|---|
| measured_nvml_peak_gib | Maximum of the three measured-window NVML peaks. |
| first_warmup_nvml_peak_gib | Peak within the first complete warm-up call. |
| suite_nvml_peak_gib | Peak across setup, all warm-up/measured calls, QA and shutdown. |
| torch_allocated_peak_gib / torch_reserved_peak_gib | Maximum recorded allocator peak across measured calls; individual values remain in the call records. |

NVML samples the memory sum of the suite's own GPU processes and workers approximately every 100 ms; brief allocations may be missed. Torch counters are reset at each call but include resident allocations. They do not cover all Jittor, ORT or other CUDA memory. GiB uses 2^30 bytes.

MuseTalk reaches **137.849609375 GiB** in its first warm-up and **9.4921875 GiB** in each measured call. VideoReTalking reaches **133.6875 GiB** in the first warm-up and **16.01171875 GiB** in each measured call. Both suite peaks equal their first-call peaks. The supplied audit supports a cuDNN autotuning/workspace interpretation but does not supply a complete allocation call stack or establish a unique operator-level cause. Warmed peaks alone do not demonstrate startup feasibility at those capacities.

## Actual output and metadata

Wan's final encoded outputs contain **35 / 33 / 34 frames**, at 528 × 935 and 16 media FPS. The scalar frames field is null because the lengths differ; frames_per_repeat retains all three. Per-repeat durations are derived from decoded frame count / media FPS. No requested shape or mean frame count substitutes for the actual outputs.

Talker-T2AV resets Python/NumPy/Torch/CUDA seed 42 at the generation boundary after initialization; all six calls produce 136 frames. Other configurations retain their own recorded seed/sampling behavior. This is not a claim of byte-identical output.

Output dimensions describe the generated region or paste-back canvas; encoded dimensions include comparison panels where present. Neural face crops can be smaller. Follow-Your-Emoji-Faster counts its main generated output, not an additional comparison panel.

No fresh attention capture accompanies the timed suites. Labels for the original 46 implementations retain historical execution observations from 15 October; ten additional configurations use 19 October source/configuration inspection. SDPA denotes an API path and does not establish actual kernel dispatch. Package versions and repository heads are post-run inventories, not contemporaneous execution captures or complete instrumentation snapshots.

## Provenance and limits

The authors supplied the final workbook and README. All 56 sets of timing means and sample SDs, measured-window memory maxima, frame sequences and phase unions were checked against the **336 workbook call records**. The README references a separate JSON delivery, server-side raw traces/adapters and output videos; these were not included in the supplied directory. No GPU inference, independent kernel capture or visual-quality assessment was performed during this integration.

The reported output checks establish freshness, decodeability and nonconstant samples, not identity, lip-sync or perceptual quality. These short demo repetitions do not measure matched quality, TTFF, delivery jitter, sustained service or long-session drift. The results are configuration observations, with model residency, inputs and prerequisites explicitly retained.

Download the summary CSV, full JSON (including all six calls and statistics per configuration), and 336-call CSV. The release manifest pairs their hashes with the updated manuscript and source package. Earlier dated releases remain available with their original meanings.

