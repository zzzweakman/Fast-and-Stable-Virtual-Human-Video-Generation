# AR supplement review

This records the first CSV supplement. See the subsequent [AR paper collection review](ar-collection-review.md) for the current catalogue totals and SpeakerVid-5M baseline cross-listing.

Reviewed 9 October 2026 against the user-supplied `virtual-human-survey/data.csv`, the manuscript's AR section, and original papers. The user confirmed retaining the manuscript's **strict native visual-AR definition**.

The CSV contains **28 AR-labelled rows representing 20 distinct works**. Four were already in the native visual-AR category, eight were already assigned to another visual route, and eight were absent from the catalogue. Of the absent works, **FluentAvatar qualifies for native visual AR**. The other seven generate compact facial or body motion rather than visual frame state. After this supplement the website contains **five native visual-AR papers and 149 papers overall**.

## Added: FluentAvatar

CSV paper ID **338**; citation key `deng2026fluentavatarflickerfreetalkingheadanimation`.

[FluentAvatar: Flicker-Free Talking-Head Animation via Phoneme-Guided Autoregressive Modeling](https://arxiv.org/abs/2509.12052), by Yuchen Deng, Xiuyang Wu, Hai-Tao Zheng, Suiyang Zhang, Yi He, and Yuxing Han.

[Sections 3.1–3.3 of v3](https://arxiv.org/html/2509.12052v3) describe autoregressive visual-token keyframes, phoneme-conditioned causal attention, and timestamp-aware interpolation. Open-MAGVIT2 image tokenization and RGB reconstruction establish that the predicted state is visual, satisfying the manuscript's inclusion rule. The website uses Figure 4 as the preview and a two-sentence mechanism summary; it makes no real-time latency claim.

The CSV's year column says **2025**, matching the first arXiv submission. Its BibTeX and the manuscript bibliography say **2026**, matching the revised v3 edition. The catalogue retains **2026** under its existing bibliography-year policy, with the discrepancy recorded in `provenance`.

## All 20 distinct AR-labelled works

CSV IDs below identify source rows; duplicated works count once. Existing classifications follow the manuscript's visual-owner test: a reusable subject renderer takes precedence over its motion controller; a dense iterative video generator stays diffusion-based; native visual AR predicts evolving dense or discrete frame state from history, optionally with a local refinement head.

| Work | CSV paper IDs | Result |
| --- | --- | --- |
| MIDAS | 33 | Already native visual AR; compressed next-frame visual state. |
| Body of Her | 34 | Already native visual AR; continuous visual tokens. |
| UniMo | 337 | Already native visual AR; interleaved video and human-motion tokens. |
| EARTalking | 339 | Already native visual AR; framewise 3D-VAE visual representations. |
| FluentAvatar | 338 | **Added**; phoneme-aligned visual-token keyframes. |
| X-Streamer | 35 | Already diffusion-based; its Actor denoises dense LTX-VAE video chunks. |
| ARIG | 41, 334 | Already render-based; AR head-motion controls drive portrait warping. |
| Teller | 49, 331 | Already render-based; motion tokens drive an implicit-keypoint warper. |
| DyStream | 76 | Already render-based; identity-agnostic motion drives a reference appearance volume and warp. |
| UniTalker | 97, 335 | Already render-based; speech and facial-landmark tokens feed an emotion-guided renderer. |
| OmniResponse | 98, 336 | Already render-based; conversational facial coefficients feed a pretrained renderer. |
| Talker-T2AV | 341 | Already render-based; 40-dimensional LIA-X motion codes feed a frozen identity-conditioned decoder. |
| Video = World + Event Stream | 343 | Already diffusion-based, displayed as Wan-Streamer v0.3; conditional flow matching generates continuous audio/video latents. |
| StreamingTalker | 77, 332 | Outside the strict supplement; generated state is facial mesh motion. |
| EchoAvatar | 93, 333 | Outside the strict supplement; generated state is full-body 3D motion. |
| VoxFace | 96, 340 | Outside the strict supplement; generated state is facial-expression tokens and 3D motion. |
| ARTalk | 177, 330 | Outside the strict supplement; generated state is FLAME expression and pose. |
| FacePlex | 202 | Outside the strict supplement; generated state is FLAME facial motion. |
| MindFlow | 205 | Outside the strict supplement; generated state is ARKit blendshapes and head angles. |
| ARDY | 272 | Outside the strict supplement; generated state is root and skeletal body motion. |

## Original-paper evidence for the seven excluded additions

These are relevant to broader AR motion/controller research. Exclusion here is a scope decision, not a judgment of quality or relevance to the wider survey.

| Work and verified source | Representation evidence | Metadata clarification |
| --- | --- | --- |
| [StreamingTalker](https://arxiv.org/html/2511.14223v3) | The method's facial-motion latent section encodes mesh vertex motion with a VQ-VAE; generated latents decode into facial meshes. | AAAI **2026**; first preprint **2025**. CSV duplicate years differ. |
| [EchoAvatar](https://arxiv.org/html/2605.28272v1) | §3.1 represents root velocity, height, and joint rotations, then tokenizes motion for causal generation. | SIGGRAPH **2026**; the CSV duplicate marked 2025 is incorrect. |
| [VoxFace](https://openaccess.thecvf.com/content/CVPR2026F/papers/Xiong_VoxFace_Streaming_Audio-Visual_Synthesis_via_Relay-Style_Multi-Token_Prediction_for_Interactive_CVPRF_2026_paper.pdf) | Fig. 1 renders generated 3D motion onto target identities; §3.2 predicts FSQ facial-expression tokens; §4.3 measures first-face-mesh latency. | **CVPR Findings 2026**, pp. 3543–3552. No arXiv identifier was established. |
| [ARTalk](https://arxiv.org/html/2502.20323v5) | A multiscale codebook represents FLAME expression and pose; §7 discusses downstream avatar integration. | **SIGGRAPH Asia 2025**, corroborated by the [author project](https://xg-chu.site/project_artalk/). |
| [FacePlex](https://arxiv.org/html/2606.30145v2) | §3.3 and Appendix D.1 define FLAME motion; §§3.5 and 4.1 use a separate FlexAvatar renderer. | v2 changes the title to **FacePlex: Toward Natural Full-Duplex Conversational Avatars**. The CSV contains the older title. |
| [MindFlow](https://arxiv.org/html/2606.27779v1) | §3.4 combines AR with a flow-matching motion head; §4.1 specifies 51 ARKit coefficients and three head angles. | ECCV **2026**; arXiv **2606.27779**. |
| [ARDY](https://arxiv.org/html/2607.08741v1) | §§3.1–3.2 use explicit root position/heading and a body-motion latent; §3.4 denoises motion tokens. | TOG **45(4), article 86, 2026**; DOI **10.1145/3811284**, corroborated by the [official project](https://research.nvidia.com/labs/sil/projects/ardy/). |

Talker-T2AV was also rechecked because its abstract calls the output video latents. [Appendix A of v2](https://arxiv.org/html/2604.23586v2) specifies **40-dimensional LIA-X motion codes** and a frozen decoder conditioned on a source identity image. Its existing render-based assignment is therefore retained.

The other CSV rows mentioning autoregression, causal generation, or forcing were screened as well. They concern general-video foundations, motion generation, or iterative video diffusion already covered by the manuscript's separate routes. They were not imported into the native visual-AR category.

Only scholarly metadata, source links, and classification decisions are published. The raw CSV, creator fields, and internal comments are not included. Manuscript sources and the supplied draft PDF were not modified.
