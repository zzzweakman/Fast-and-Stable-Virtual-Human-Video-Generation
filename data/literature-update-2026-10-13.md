# Literature update — 13 October 2026

The revised survey adds 26 references selected from the supplied 188-entry recommendation list. Selection targets missing mechanisms and evaluation questions, rather than incorporating every recommended paper. The selected primary manuscripts were inspected beyond their abstracts; the complete 188-paper pool has not been independently re-reviewed in this update.

The bibliography increases from 237 to 263 cited references. The public catalogue adds 21 records and revises five already present, reaching 185 unique papers. Every record has an attributed original-paper preview.

## What changed and why

- Added motion-preserving distillation, explicit memory-update policies, and the distinction between within-chunk feature reuse and bounded temporal memory.
- Added compact motion controllers, Gaussian deformation, and reference-texture reuse while preserving classification by dense visual appearance ownership.
- Added interaction-context datasets, temporal metric alignment, oral-identity evaluation, and human-centered quality assessment.
- Revised the open questions to recognize existing adaptive memory methods and focus on recovery under corrupted history and changing references.
- Extended the duration table with task- and protocol-specific examples; no common-hardware speed ranking was constructed.

## Source identity and interpretation

- `2512.11423` is now titled **JoyStreamer-Flash** in arXiv v3 (31 March 2026). Its original title was JoyAvatar. It is distinct from `2602.00702`, the text–audio-conditioned JoyAvatar paper. The existing citation ID is preserved.
- Cui et al.’s **AvatarForcing** (`2603.14331`) denoises dense video in a sliding window. Ki et al.’s **Avatar Forcing** (`2601.00664`) predicts motion for reused appearance.
- The **OmniHuman dataset / OHBench** (`2604.18326`) is distinct from the **OmniHuman-1** generation method.
- **Motar** retains a visual diffusion decoder despite using an AR motion controller; **EfficientSync**, **VibeAvatar**, and **Talk Like You** reuse appearance through geometric transport. **TT-SAC** is a conditioning procedure applicable across generator families.
- **ForeverCache** resets between chunks. **LiveAnimate** includes a clean-cache update, and its reported block timing excludes VAE decoding. **AvatarForcing** updates each block multiple times despite one update per window advance.

## Integrated papers

| Paper | Primary edition | Placement |
|---|---|---|
| EmbedTalk | [arXiv 2603.07604v1](https://arxiv.org/abs/2603.07604v1) | render based methods |
| Face-to-Face | [arXiv 2603.14794v1](https://arxiv.org/abs/2603.14794v1) | datasets and evaluation |
| AvatarForcing · sliding-window video | [arXiv 2603.14331v1](https://arxiv.org/abs/2603.14331v1) | diffusion based methods |
| Gloria | [arXiv 2603.29931v1](https://arxiv.org/abs/2603.29931v1) | diffusion based methods |
| OmniHuman dataset / OHBench | [arXiv 2604.18326v1](https://arxiv.org/abs/2604.18326v1) | datasets and evaluation |
| SDTalk | [arXiv 2605.09956v1](https://arxiv.org/abs/2605.09956v1) | render based methods |
| EverAnimate | [arXiv 2605.15042v1](https://arxiv.org/abs/2605.15042v1) | diffusion based methods |
| TT-SAC | [arXiv 2605.25488v1](https://arxiv.org/abs/2605.25488v1) | diffusion based methods |
| Temporally-Aligned Evaluation | [arXiv 2606.01031v1](https://arxiv.org/abs/2606.01031v1) | datasets and evaluation |
| Reference-guided deep-compression VAE | [arXiv 2606.01620v1](https://arxiv.org/abs/2606.01620v1) | diffusion based methods |
| InteractiveAvatar | [arXiv 2606.22905v1](https://arxiv.org/abs/2606.22905v1) | diffusion based methods |
| HVEval+ / MoE-Rater | [arXiv 2607.16742v1](https://arxiv.org/abs/2607.16742v1) | datasets and evaluation |
| TaoMate | [arXiv 2607.24359v1](https://arxiv.org/abs/2607.24359v1) | diffusion based methods |
| InteracVid | [arXiv 2608.01157v1](https://arxiv.org/abs/2608.01157v1) | datasets and evaluation |
| LeapTalk | [arXiv 2608.00079v1](https://arxiv.org/abs/2608.00079v1) | diffusion based methods |
| Avatar-Forever | [arXiv 2608.12107v1](https://arxiv.org/abs/2608.12107v1) | diffusion based methods |
| LiveAnimate | [arXiv 2608.11745v1](https://arxiv.org/abs/2608.11745v1) | diffusion based methods |
| DynaForcing | [arXiv 2608.17707v1](https://arxiv.org/abs/2608.17707v1) | diffusion based methods |
| EfficientSync | [arXiv 2608.18832v1](https://arxiv.org/abs/2608.18832v1) | render based methods |
| Motar | [arXiv 2609.10317v1](https://arxiv.org/abs/2609.10317v1) | diffusion based methods |
| Vidu S2 | [arXiv 2609.11638v1](https://arxiv.org/abs/2609.11638v1) | diffusion based methods |
| VibeAvatar | [arXiv 2609.18632v1](https://arxiv.org/abs/2609.18632v1) | render based methods |
| FlowAct-R2 | [arXiv 2609.35728v1](https://arxiv.org/abs/2609.35728v1) | diffusion based methods |
| Routed Forcing | [arXiv 2609.30963v1](https://arxiv.org/abs/2609.30963v1) | diffusion based methods |
| RGOR | [arXiv 2609.38019v1](https://arxiv.org/abs/2609.38019v1) | datasets and evaluation |
| Talk Like You | [arXiv 2610.06658v1](https://arxiv.org/abs/2610.06658v1) | render based methods |

## Measurements and earlier releases

Common-environment results are pending. The measurement template contains only a header, with no values borrowed from the literature. The authors will provide frames per run, resolution, preprocessing/generation/postprocessing time, and peak GPU memory for all open-source methods. Existing original-paper values retain their source configuration and timing boundaries.

The four visual routes and their definitions are preserved. Dated 9 October releases, their PDFs, and their source records remain unchanged. The new release pairs the updated PDF, source package, bibliography, and frozen catalogue.
