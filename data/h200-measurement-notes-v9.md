# Single-H200 measurements: manuscript subset

The current tables report **51 configurations for 51 methods**: 11 GAN, 16 diffusion, 23 rendering, and one UniLS motion visualization. Configurations are included when first-call loading and all displayed timing and memory fields are recorded. Five configurations without an initial loading interval are omitted from the tables. The [original 56-configuration release](h200-results-2026-10-19.json) and [all 336 calls](h200-trials-2026-10-19.csv) remain unchanged.

The current [summary CSV](h200-results-v9.csv), [JSON](h200-results-v9.json), and [306-call CSV](h200-trials-v9.csv) cover the included configurations. Publication years match the cited editions in the manuscript. Native visual-AR coverage is zero; UniLS predicts motion and exports a FLAME visualization.

## First-call loading and warmed execution

Each configuration executes three complete warm-ups followed by three measured calls in the same interpreter: **153 warm-ups and 153 measured calls** for the included subset. Every call repeats its selected clip, rebuilds clip state, and writes fresh output.

**Load₁ is the recorded loading interval in the first invocation, `warmup_01`.** It is one observation per configuration. Disk caches may already be populated, so this is not a cache-cleared cold-start experiment. MuseTalk, LAM, and GUAVA have initial loads of **7.99 s, 23.09 s, and 30.20 s**, respectively.

Pre, Gen, Post, and Call retain the means of the three later measured calls. Load₁ and these means refer to different invocations and cannot be summed into a measured total. Ten included configurations retain audited model objects; 41 reload each call. Retained models still repeat pre-processing and rebuild clip state.

| Field | Definition |
|---|---|
| `publication_year` | Year of the cited publication in the manuscript's measured tables. |
| `first_load_s` | Loading in the first recorded invocation; displayed as Load₁. |
| `pre_s`, `generation_s`, `post_s` | Means over the three measured calls, using implementation-specific synchronized phase boundaries. |
| `call_s`, `call_sd_s` | Mean and sample standard deviation of measured Call; Call spans inference entry to synchronized return, including any loading in that call, native validation, and unclassified overhead. Generic output QA follows Call. |
| Other `*_sd_s` fields | Sample standard deviations with the n−1 denominator over measured calls. |
| `stage_union_s`, `stage_overlap_s` | Mean union of Pre/Gen/Post and the difference between their sum and union. |
| `evaluation_s` | Recorded native validation; SyncTalk includes this inside Call but outside Pre/Gen/Post. |
| `suite_process_s` | The complete 3+3 process: startup, setup, all six calls, output QA, and shutdown. |
| `statistics` | Measured-call values, mean, median, sample SD, minimum, and maximum for each recorded phase. |
| `warmup_iterations`, `measured_iterations` | The three individual calls of each kind. |

The new summary uses `first_load_s` instead of an ambiguous top-level `load_s` column. Within `statistics`, `load_s` still describes the three measured loading intervals; in individual trial records, `load_s` describes that particular call. These underlying records are preserved. EAT and HyperReenact remain included because their initial loads are recorded, even though loading intervals are absent from their later resident calls.

Suite total is not a single-call latency or TTFF and must not be divided by six to estimate warmed latency. Ditto and Talk Like You overlap phases; phase sums do not represent elapsed time. Synchronization may itself affect asynchronous execution. The pipeline-cost figure uses all stages and the Call denominator from the same first invocation, rather than mixing initial loading with warmed phase means.

## Hardware, inputs, and memory

Each configuration uses one H200. Suites run across three nodes, with four CPU-affinity identifiers and numerical-library thread limits of four. Affinity identifiers do not establish four independent physical cores. Host memory, storage, caches, software, precision, offloading, and input settings differ.

Output dimensions describe generated regions or paste-back canvases, excluding comparison panels. Internal neural face crops can be smaller. Supplied tracking, features, masks, and subject-trained assets remain prerequisites where accepted by the implementation; LAM performs fresh tracking. Talker-T2AV resets seed 42 at the generation boundary and produces 136 frames in all six calls. No common seed or bitwise-equivalence claim applies across methods.

Warm peak is `measured_nvml_peak_gib`: the maximum NVML peak across the three measured calls after three complete warm-ups. Each window includes any loading, pre-processing, generation, and output processing. MuseTalk and VideoReTalking retain **9.49 GiB and 16.01 GiB**, respectively. Own-process/worker NVML samples are collected approximately every 100 ms, which can miss brief allocations. Torch counters do not cover all Jittor, ORT, or other CUDA allocations. GiB uses 2^30 bytes. The original first-call, suite, and framework memory observations remain in the downloads.

## Evidence and manuscript

Initial loading, measured means, sample SDs, memory maxima, phase unions, and output frame counts were reconciled with the corresponding records. The 306 included call times match archived iteration records. The first measured primary output of each included configuration was decoded and checked against recorded frame counts and canvas dimensions.

Labels for 44 included implementations describe separate execution observations; seven use source/configuration inspection. No fresh attention capture accompanies the timed suites. Package versions and repository heads are post-run inventories. Archived launch records supplement six configurations; unrecorded sampler and decoder defaults remain unspecified. The [archived output evidence](h200-output-evidence-v1.json) retains these configuration annotations and sources.

The current [54-page survey](../assets/survey/survey-measured-v9.pdf) includes a radial taxonomy, revised schematic portraits and representation diagrams, and a first-call stage-cost figure. The [clean source package](../assets/survey/virtual-human-survey-measured-v9.zip) contains 52 files, including the compiled paper and the ten figures it uses. Cartoon illustrations are not presented as raw measured outputs. Earlier output-crop assets and their provenance remain available in earlier releases.

The archive contains JSON reports, iteration records, phase events, NVML samples, and videos, but excludes adapter source, model weights, and complete environments. No new GPU runs or quantitative visual-quality assessment were performed for this reporting revision. Unmatched workloads and residency policies prevent a controlled method ranking; repeated short calls do not establish TTFF, delivery jitter, sustained service, or long-session drift.

The [release manifest](snapshots/measured-v9/manifest.json) pairs the current data, protocol, paper, and source-package hashes. Earlier snapshots retain their original files and reporting definitions.
