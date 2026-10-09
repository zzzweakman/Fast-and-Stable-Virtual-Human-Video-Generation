# OmniResponse: placement and source check

The paper is now a dedicated case study in the survey's AR section, with an
additional ResponseNet entry in the dataset discussion and table. The citation
year is corrected to NeurIPS 2025. Completed figure PDFs are included directly;
illustration placeholders are absent from the final manuscript.

## Why its AR role needs qualification

OmniResponse is autoregressive at the response and facial-behavior level. Its
main Section 3.1 and supplementary B.1 specify that predicted embeddings decode
to facial coefficients, which a pretrained portrait renderer maps to RGB. The
supplement identifies 52 blendshape coefficients and 12 head-pose parameters.
This is a valuable AR example, but calling it a pure visual-AR generator would
contradict the survey's appearance-ownership rule. The website therefore exposes
it in AR browsing as **AR controller**, while preserving its rendering-primary
statistical assignment. It remains one source record.

## Checked sources

- [Official NeurIPS 2025 record](https://proceedings.nips.cc/paper_files/paper/2025/hash/b734c30b9c955c535e333f0301f5e45c-Abstract-Conference.html): publication year and bibliography.
- [Main paper](https://proceedings.nips.cc/paper_files/paper/2025/file/b734c30b9c955c535e333f0301f5e45c-Paper-Conference.pdf): Section 3.1, pp.4–5; Section 4/Table 1/Figure 4, pp.6–7; Tables 2–3, pp.8 and 10.
- [Official supplement ZIP](https://proceedings.nips.cc/paper_files/paper/2025/file/b734c30b9c955c535e333f0301f5e45c-Supplemental-Conference.zip), Appendix.pdf: A/B.1, pp.1–3; B.5/Table 2, p.5; C.2/Tables 3–4, pp.6–7.

The evidence JSON pins each PDF hash. The supplement's runtime is 15.62 FPS on
one A100 80 GB with a stated 64 ms latency. Input/output endpoints, renderer
inclusion, timed resolution, and precision are unspecified, so TTFF and complete
pipeline speed are not inferred. Synchronization ablations retain the source's
configuration boundaries. ResponseNet split claims are limited to participant
pairs; no individual-identity-disjoint protocol is inferred.

## Writing review

Mini-outline: causal response coordination; facial controls and appearance;
within-source alignment evidence; runtime scope; dataset relevance.

Paragraph roles in the new AR subsection:
1. Opening/mechanism: explain the prediction and rendering path.
2. Evidence: connect the synchronization design to its ablations.
3. Limitation: separate reported runtime from TTFF and long-session stability.

Reverse outline: all three paragraphs support the same claim—autoregression
coordinates multimodal responses, and its representation defines which speed
and stability conclusions the source supports. The dataset entry supplies the
corresponding supervision and horizon context.

Claim–evidence map:
- NeurIPS 2025 publication | official proceedings and BibTeX | supported.
- Causal facial coefficients plus portrait rendering | main 3.1; supplement A/B.1 | supported.
- Alignment ablation changes LSE-D 9.56 to 11.51/11.91 | main Table 3 | supported within source.
- Reported runtime 15.62 FPS/A100 80 GB and 64 ms | supplement B.5/Table 2 | supported; timing endpoints unresolved.
- Continuous long-session visual stability | no time-binned protocol in checked sources | not claimed.
- ResponseNet scale, clip range, and pair split | main 4; supplement C.2 | supported; identity disjointness not claimed.

Five-dimension self-review:
- Contribution: pass; explains a distinct AR response interface relevant to the taxonomy.
- Clarity: pass; prediction, rendering, synchronization, and timing have separate roles.
- Empirical strength: bounded; cites the authors' ablations and runtime without rerunning models.
- Evaluation completeness: limitations explicit; TTFF and long-session stability remain unestablished.
- Method soundness: pass; appearance ownership and cross-listing remain consistent, with no duplicate statistical count.
