# Survey measurements, v10

This release matches the 43-page `1028_astra_v0` manuscript. Runtime values retain the earlier observations. HDTF and StreamEval values are exported directly from the current manuscript tables.

## Runtime and memory

The suite reports 51 configurations covering 51 methods on one H200 each: 11 GAN, 16 diffusion, 23 rendering, and one UniLS motion visualization. Each configuration has three complete warm-ups followed by three measured calls in the same interpreter. The included records contain 306 calls. The original 56-configuration archive and its 336 calls remain available. Five configurations lack a first-call loading interval and are excluded from these tables.

Load₁ is the loading interval in the first invocation, `warmup_01`. Pre, Gen, Post, and Call are means of the three subsequent measured calls. Call also reports sample standard deviation. Initial loading and warmed means have different timing windows and cannot be summed into a measured total. MuseTalk, LAM, and GUAVA have initial loads of 7.99, 23.09, and 30.20 seconds.

Warm peak is the largest own-process/worker NVML sample across the three measured calls. Sampling is approximately every 100 ms and may miss short allocations. These windows include loading, preprocessing, generation, and output processing. Ten configurations retain audited model objects; 41 reload each call. Disk caches may already be populated on the first invocation.

Call spans inference entry to synchronized return. Stage boundaries depend on the implementation, and phases can overlap. The downloadable suite total includes setup, all six calls, output checks, and shutdown. It is neither single-call latency nor time to first frame. Different inputs, model residency, and prerequisites prevent a controlled speed ranking.

Unless stated otherwise, inputs use the demo recommended in the official open-source README. Wav2Lip+GAN uses the EDTalk pair, and FOMM uses the TPS Motion Model pair. Third-party implementations use their supplied demos. RAD-NeRF uses the PyTorch reimplementation. Precomputed tracking, features, masks, and subject-trained assets remain prerequisites where required. LAM performs fresh FLAME tracking. No common random seed is imposed across methods. Talker-T2AV resets seed 42 at the generation boundary and produces 136 frames in each call.

Attn. reports the backend labels used in the manuscript. FA2/FA3 denote FlashAttention 2/3, xF denotes xFormers, and SDPA-m/e/f/c denote math, memory-efficient, flash, and cuDNN paths. S marks seven labels obtained from source/configuration inspection. The other 44 labels come from separate historical execution observations. No new kernel-dispatch capture accompanies the timed runs. Eager means that no fused attention API was reported.

Input settings, stage boundaries, attention evidence, per-call statistics, and memory peaks remain in the JSON and CSV exports. Adapter source, model weights, and complete environments are outside the archive. Repeating short demo clips does not establish sustained service or long-session stability.

## HDTF

The matched-input evaluation covers 23 configurations on 40 fifteen-second cases from the Let Them Talk HDTF split, producing 920 videos. The table reports Sync-C, Sync-D, identity similarity, FID, and FVD in manuscript order. SyncNet uses 25 FPS without offset correction. Identity is raw ArcFace cosine similarity, averaged over 16 temporal-bin midpoint frames per clip. FID and FVD use center-square full-frame clips and 20 real reference clips.

Identity scores depend on preserved source pixels and pose variation. Distribution scores are sensitive to framing and the small reference pool. These measurements do not establish long-session stability.

## StreamEval

Six configurations use a 20% subset of avatar-performance conditions, with supplied portraits, incrementally released speech, and live visual directions. Three repetitions yield 36 sessions per configuration and 216 sessions in total. Durations cover 15, 30, 60, 120, and 300 seconds. Aggregation averages repetitions, then conditions within each duration stratum, then the five strata equally. Failures and unsupported visual controls remain in the denominator.

The columns are Quality, Stability, Following, and Identity, on a 0–100 scale. Local Qwen vision models replace the reference judges, without independent calibration. The subset and judges limit direct comparison with the original leaderboard.

A–V Sync remains unresolved in the local observations. It and the aggregate scores that depend on it are omitted from the paper and website. StreamEval awards five points for support of custom portraits, independently of content quality. All six tested configurations have this capability, so the constant bonus is described in text and omitted from the table.

## Files

- `h200-results-v10.json` and `.csv`: 51 runtime configurations and attention labels.
- `h200-trials-v10.csv`: 153 warm-up and 153 measured calls.
- `benchmark-results-v10.json`: HDTF and StreamEval protocols and values.
- `hdtf-results-v10.csv` and `streameval-results-v10.csv`: benchmark rows.
- `snapshots/measured-v10/manifest.json`: paired paper, source package, catalogue, and data files.

Earlier releases remain archived unchanged. The build validates all numerical runtime values against the original records and the current benchmark exports against the downloadable manuscript tables.
