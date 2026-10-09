# AR second-pass review

Reviewed 9 October 2026 against the supplied `AR_Second_Pass_Supplement`, the manuscript's Section 5, and original publications. The website keeps the user's chosen **strict temporal visual-AR definition**: prior generated visual state must condition appearance generation across time. Spatial token order, recurrent feature processing, or an AR controller alone does not establish that property.

**Result:** four new source-paper records, three additional temporal-AR examples for browsing, and a correction to FluentAvatar's classification. The catalogue contains **164 unique papers, 122 arXiv links, and 72 source previews**. AR browsing contains **eight records: five primary-route papers and three cross-listed baselines**. The five primary entries comprise four existing human/video methods and DualLip's regional branch. Baselines retain one citation and one statistical count under their source paper's supporting category.

## Decisions on the five supplied works

| Work | Website decision | Suitability for the survey |
| --- | --- | --- |
| ART-V in **Show Me What and Tell Me How: Video Synthesis via Multimodal Conditioning** (CVPR 2022) | Add the MMVID source paper under Related methods; cross-list its ART-V baseline in AR browsing. | Include as historical full-frame temporal visual AR, explicitly naming the baseline. |
| **DualLip: A System for Joint Lip Reading and Generation** (ACM Multimedia 2020) | Add its without-duration branch to primary AR, with lip-region and historical labels. | Include as regional pixel-space temporal AR; distinguish the branch and its output scope from full-portrait systems. |
| TransformerT2L in **Parallel and High-Fidelity Text-to-Lip Generation** (AAAI 2022) | Add the ParaLip source paper under Related methods; cross-list TransformerT2L in AR browsing. | Include as a historical regional baseline and evidence of output-feedback error accumulation. |
| **Taming Transformer for Emotion-Controllable Talking Face Generation** (2025) | Add under Related methods, reachable through the AR scope-context link. Exclude from strict temporal-AR browsing and counts. | Useful spatial-AR boundary example; cross-frame inference remains unestablished. |
| **Photorealistic Novel View Synthesis of Human Faces using Next-Scale Transformers** (2026) | Retain in these review notes; do not add a catalogue record. | Optional adjacent-task/outlook reference. It generates viewpoints across scales, rather than a temporal avatar sequence. |

## Primary-source evidence and limits

### ART-V and MMVID

The [CVPR paper, §4 and §4.1](https://openaccess.thecvf.com/content/CVPR2022/papers/Han_Show_Me_What_and_Tell_Me_How_Video_Synthesis_via_CVPR_2022_paper.pdf) defines ART-V as a causal DALL-E-style Transformer predicting the concatenated video-token sequence, with VQGAN providing appearance reconstruction. Evaluation includes MUG, Multimodal VoxCeleb, and iPER. The eight-frame, 128 × 128 VoxCeleb setup uses 512 visual tokens, establishing prediction across frames rather than merely within a single image.

MMVID itself uses bidirectional masked-token prediction. ART-V is neither the main method nor a separate paper. MMVID's long-sequence extrapolation demonstrations must not be assigned to ART-V; short human-video experiments do not establish interactive streaming or audio-driven lip synchronization. The published and arXiv Table 3 differ, so the website does not mix their numerical results. The [official publication record](https://openaccess.thecvf.com/content/CVPR2022/html/Han_Show_Me_What_and_Tell_Me_How_Video_Synthesis_via_CVPR_2022_paper.html) supplies CVPR 2022 metadata and pages 3615–3625.

### DualLip

[§3.3.2 of the original paper](https://arxiv.org/pdf/2009.05784) explicitly feeds the previous generated image into the next prediction for the **without-duration** branch. Its decoder generates lip pixels directly; the experiments use 128 × 64 outputs. The full-face extension has a separate lip-to-face module, so full-face appearance ownership is not attributed to this regional AR component.

The original paper's without-duration results use GRID. Its TCD-TIMIT experiments use the with-duration branch; the later ParaLip paper reproduces a without-duration baseline on both datasets. These are distinct sources of evidence. Figure 3(b) depicts the selected branch but does not draw the feedback arrow; the textual method supplies that evidence. [ACM's publication record](https://doi.org/10.1145/3394171.3413623) establishes Multimedia 2020, pages 1985–1993.

### TransformerT2L and ParaLip

[The ParaLip paper, §3.1, Eq. (1), and §5.1](https://arxiv.org/pdf/2107.06831v2) specifies temporal image-history conditioning and identifies TransformerT2L as an implemented AR comparison baseline. GRID and TCD-TIMIT experiments use 160 × 80 lip crops. Figure 3 and its discussion demonstrate how errors propagate through generated-image feedback.

ParaLip's main method is non-autoregressive; its architecture in Figure 2 is not an AR diagram. The website counts the publication once and cites [AAAI 2022, 36(2), 1738–1746](https://ojs.aaai.org/index.php/AAAI/article/view/20066). The first preprint is from 2021; method verification used arXiv v2 because the publisher PDF endpoint was unavailable.

### Taming Transformer

[§§3.4–3.5 and §4.5](https://arxiv.org/html/2508.14359v1#S3.SS4) document autoregression over image-code positions, VQGAN appearance decoding, and a training loss for cross-frame consistency. A generated-frame feedback dependency at inference is not established. This is a spatial visual-AR method, not merely a motion controller; its appearance-owning tokens justify retaining it as relevant context without expanding the strict temporal category.

### Human-face next-scale novel-view synthesis

[§3 and Figure 2](https://arxiv.org/html/2608.23410v1#S3) describe next-scale prediction, with multiple facial viewpoints generated simultaneously at each scale. Optional downstream lifting uses an existing Gaussian reconstruction model. Camera views are not video timesteps, and the paper does not establish an animated or audio-driven avatar generator. Its first preprint is dated [24 August 2026](https://arxiv.org/abs/2608.23410). A brief outlook comparison is appropriate if the survey discusses spatial or multiview extensions; it should not become another row in the temporal-AR evidence table.

## Corrections to earlier interpretation

**FluentAvatar:** the initial CSV review inferred strict membership from appearance-token prediction too readily. [v3 Eq. (4)](https://arxiv.org/html/2509.12052v3#S3.SS1) includes earlier frames, but [§3.3 and Figure 4](https://arxiv.org/html/2509.12052v3#S3.SS3) explicitly mask cross-frame attention during keyframe generation. Interpolation couples adjacent visual keyframes and is described broadly as autoregressive, yet its output-feedback order is unspecified. Appendix C.1 does not resolve this. The current evidence supports **visual-token AR with temporal dependency unresolved**. The record, citation, and preview remain available under Related methods, outside verified temporal-AR counts. This is not evidence that the model lacks temporal modeling. An explicit implementation or factorization would be needed before restoring strict membership.

**Archon:** its semantic masks are dense visual representations. The exclusion criterion is appearance ownership: [§3.3](https://arxiv.org/html/2605.30311v1#S3.SS3) uses a fully fine-tuned WALT diffusion model to synthesize RGB video conditioned on those masks. That differs from a documented local emission head on an appearance-owning AR backbone. The strict-route exclusion remains, with this more precise rationale.

## Recommended survey changes

These are editorial recommendations; the manuscript and its downloadable PDF were not modified.

1. **Section 5, scope and mechanism discussion:** add a short historical paragraph separating temporal pixel/image feedback (DualLip without duration and TransformerT2L) from temporal appearance-token prediction (ART-V). Name each source paper and mark the two baselines explicitly.
2. **Mechanism/interaction map:** if adding rows, give ART-V a full-frame human-video baseline label; mark DualLip and TransformerT2L as lip-region outputs. Regional generation does not imply full-portrait appearance ownership or an end-to-end avatar system.
3. **Speed/stability evidence table:** only add rows with matched output resolution, sequence length, hardware, timing boundary, and benchmark provenance. Do not transfer MMVID's long-horizon behavior to ART-V, combine arXiv and published scores, or compare regional-image throughput directly with full-avatar performance.
4. **Taxonomy boundary paragraph:** use Taming Transformer to distinguish spatial token AR from temporal AR; describe FluentAvatar as unresolved until its temporal factorization is clarified. Explain Archon through its diffusion-owned RGB appearance rather than calling its masks nonvisual.
5. **Optional outlook:** cite next-scale face-view synthesis only when discussing adjacent spatial/multiview tasks. It is not needed to increase the temporal-AR paper count.

## Website implementation and provenance

The new `context` category is displayed as **Related methods** within Supporting references. MMVID and ParaLip preserve their main-method descriptions there. In the AR view, their existing source-paper records display baseline-specific titles, summaries, and tags through `crossListings`; citation exports still contain each paper once. FluentAvatar and Taming Transformer share an **AR scope context** discovery link, separate from general-video foundations.

Exclusive totals are 22 GAN, 43 diffusion, 5 AR, 53 rendering, and 41 supporting references. Supporting references comprise 18 foundations, 10 datasets, 6 evaluation papers, 3 surveys, and 4 related-method records. Four new original-paper links returned HTTP 200 during this review.

All four supplied preview checksums match the package manifest. DualLip, TransformerT2L, and Taming source images match the downloaded originals pixel for pixel. The ART-V crop differs from a fresh render by at most one RGB level in a handful of channels, consistent with rendering rounding. The comparison labels and captions were inspected. ART-V and TransformerT2L previews identify their non-AR comparison rows explicitly; none is presented as a standalone baseline architecture. `assets/papers/manifest.json` records the original source, crop/page when applicable, checksum, and WebP conversion.

## Validation and interface review

Catalogue tests and the static build passed. Browser checks covered the eight-paper AR view, five-paper exclusive AR count, baseline aliases, publication-year filtering, persistent list/grid state, eight unique exported citations, supporting-context and foundation links, and the empty-state recovery. Layouts at 1440, 720, 390, and 320 pixels showed no horizontal overflow. Desktop and mobile AR/context views had no automated WCAG A/AA violations or JavaScript errors in these checks.

Visual review preserved the existing type, route colors, and mineral scope panel. Scope links wrap with 44-pixel targets; baseline/source-paper distinctions remain readable, and original previews load in both AR and supporting views. The update is ready for publication. Automated accessibility checks do not replace a complete manual accessibility audit.
