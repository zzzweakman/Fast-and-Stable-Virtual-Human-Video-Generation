# Evidence for the illustrated manuscript

The current files are `evidence-2026-10-09-final.json` and
`configurations-2026-10-09-final.csv`. They extend the earlier audit with three
OmniResponse configurations: the full model, without Chrono-Text Markup, and
without TempoVoice. Source editions, page locations, and SHA256 hashes identify
the checked material. The NeurIPS main paper and supplementary Appendix.pdf are
recorded separately; the latter is distributed inside the official supplement ZIP.

## Coverage and selection

This is a selective narrative survey based on documented source collections and
a retrospective audit dated 9 October 2026. It does not claim a systematic search
or exhaustive coverage through that date.

- 57 inherited system records preserve the submitted comparison cohort. Their
  fields have not all been checked again.
- 25 checked configuration or architecture records cover 13 systems. These are
  distinct from the inherited cohort; quantitative analyses use checked sources.
- The companion catalogue contains 164 source papers. It is a reading resource,
  not a complete export of the manuscript bibliography.

The machine-readable archive identifier is `VH-2026-10-09-final`, with parent
`VH-2026-10-09`. Earlier evidence files and the website's earlier frozen release
are preserved. The lean Overleaf package includes the current evidence and the
unchanged inherited-cohort CSV.

## Interpreting records

Reported values retain their units, configuration, and measurement boundary.
Other states are `not-reported` in a checked source (NR), `unavailable` source (U),
unresolved `conflict` (C), `not-applicable` (NA), and `not-audited`. Missing values
are never zero. Missing pointers do not prove that a paper omitted a measurement.

Mechanism annotations mean A documented architecture, Q qualitative example,
T quantitative temporal observations, B component ablation, and H proposed
transfer. T need not cover every instant; B need not be longitudinal. L4-G uses
generated history; L4-C corrupts ground-truth history. A codec cache or ordinary
causal context alone does not establish bounded multiscale L2 memory.

## OmniResponse

The official publication is NeurIPS 2025. The manuscript citation is
`luo2025omniresponse`; the website retains the stable record ID
`luo2026omniresponse` to preserve existing links and preview provenance.

The AR model predicts facial coefficients and text. A pretrained portrait renderer
supplies RGB appearance. It is discussed prominently in the AR section and
cross-listed as an AR controller, while retaining rendering-primary ownership.
AR browsing therefore has five visual-AR papers, three cross-listed baselines,
and one controller. Exclusive route counts remain GAN 21, diffusion 43, AR 5,
and rendering 54; supporting references number 41.

Supplementary B.5/Table 2 reports 15.62 FPS on one A100 80 GB and a stated 64 ms
latency. Timing endpoints, renderer inclusion, timed output resolution, and
precision are unspecified. The latency is not identified as TTFF. Main Table 3
reports LSE-D 9.56 for the full model, 11.51 without Chrono-Text Markup, and 11.91
without TempoVoice. These are synchronization ablations, not longitudinal drift
measurements. Chrono-Text markers are not the survey's L3 cache re-indexing.

ResponseNet's 696 pairs, 161 identities, 14.2 aggregate hours, 1024×1024 streams,
27.13–863.13 s clip range, and 417/139/140 split are documented in the main paper
and supplement. Participant-pair disjointness does not establish individual-
identity disjointness. Data duration is not a generated-session stability result.

## Retained source limitations

Live Avatar v6's Table 3/Table 10 TTFF discrepancy remains an unresolved conflict.
Unavailable REA-Listener primary-source timings are excluded from quantitative
synthesis. EARTalking's short-horizon ablations do not establish minute-scale
time-binned performance. A verified example of an anchor blocking an intended
change remains unavailable. No new model experiments or common-hardware rankings
are claimed. Source failure images retain their original attribution.
