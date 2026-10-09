# Evidence snapshot VH-2026-10-09

This is a retrospective audit supporting the 9 October 2026 revision. It does not reconstruct an undocumented original search procedure or claim exhaustive coverage through that date.

The 164-record catalogue is a selected, maintained reading resource, not a complete index of the bibliography. Its frozen copy accompanies the snapshot. Later updates must not silently alter this snapshot.

## Two levels of extraction

- **57 inherited system records:** the comparison cohort from the submitted route tables. Original LaTeX cells and source metadata are preserved in `cohort`. They are explicitly marked as inherited, not fully rechecked. Missing pointers are not evidence that a paper omitted a measurement.
- **22 checked configuration or architecture records for 12 systems:** the focused primary-source audit in `configurations`. Each has an edition, PDF hash, source location, boundary, field statuses, and applicable mechanism annotations. The new quantitative analyses use these records. Architecture-only records retain unaudited quantitative fields rather than turning them into NR.

`configurations-2026-10-09.csv` contains one row per checked configuration. `cohort-2026-10-09.csv` preserves the inherited inventory. `evidence-2026-10-09.json` contains both. This separation exposes remaining audit work instead of presenting the bibliography as newly verified.

## Status and interpretation

Reported values retain their units and source boundary. Other states are `not-reported` in the checked source (NR), `unavailable` source (U), unresolved `conflict` (C), `not-applicable` (NA), and `not-audited`. Missing quantities are never zero. An unavailable PDF is not a source that reports NR.

Mechanism tags mean A documented architecture; Q qualitative example; T quantitative observations at stated times or durations; B component ablation; H proposed transfer. T need not cover every instant; B need not be longitudinal. Filters include documented implementations (A), not hypotheses alone. L4-G uses generated histories; L4-C corrupts ground-truth histories. A retrieval bank or codec history does not alone establish bounded multiscale L2 memory.

## Editions and corrections

Keep archival papers, preprint revisions, supplements, and official documentation distinguishable. Hashes identify the checked PDFs. Retain conflicting reports as separate configurations until resolved. Do not silently substitute training hardware for inference hardware.

- Live Avatar v6 specifies H100 hardware; the submitted draft used an earlier H800 label. Its Table 3 reports 1.21 s TTFF for the optimized configuration, whereas Table 10 reports 0.94 s for the default three-latent-frame chunk. The source does not resolve this difference, so the record retains a conflict flag and both locations.
- StyleAvatar is rendering-primary because geometric UV appearance satisfies the same first rule used for source-volume warping. GAN components remain documented. Primary counts change from GAN 22/rendering 53 to GAN 21/rendering 54; the total stays 123.
- Eight AR browsing results still mean five primary records plus three cross-listed baselines. Charts count each source record once.
- ART-V is a baseline in MMVID. Its cited CVPR proceedings and source locations are exposed; its numerical tables must not be combined with different arXiv results.
- EARTalking v1 provides positive short-horizon ablations, but no numeric inference speed or minute-scale time-binned measurements.
- REA-Listener's primary paper was unavailable in this audit. Its inherited timing cells remain traceable in the cohort, explicitly marked unavailable, and are excluded from the revision's quantitative findings.

The proposed evaluation protocol and enrollment example are proposals/calculations, not new model experiments. Source failure panels retain attribution; missing timestamps are disclosed.
