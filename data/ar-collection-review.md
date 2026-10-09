# AR paper collection review

This is the historical 15-paper collection snapshot. The later [second-pass review](ar-second-pass-review.md) adds historical baselines and spatial context, corrects FluentAvatar's strict-AR membership, and gives current catalogue totals.

Reviewed 9 October 2026 from the supplied `AR_Paper_Collection` package, including its 15 paper records, evidence notes, and original-source image manifest. This continues the [earlier CSV review](ar-supplement-notes.md) and retains the user's confirmed native visual-AR definition.

## Catalogue changes

- **SpeakerVid-5M's visual-AR baseline is now discoverable in AR browsing.** Its existing dataset record, citation key, and BibTeX are reused. It remains one paper in the catalogue and one dataset in the statistics.
- **Three general-video foundations are added:** NOVA, VideoPoet, and VideoGPT. A link from the AR view opens this supporting collection. They do not increase the primary virtual-human route counts.
- **Eight diffusion papers are added:** Vidu S2, FlowAct-R2, PixReenact, Routed Forcing, DynaForcing, Avatar-Forever, Wan-Animate-2, and Vorch-Streamer. Streaming or blockwise autoregression does not make their main visual generator a native AR model.
- **Wan-Streamer v0.3 is retained once.** Archon and Taming Transformer are documented below as classification boundary cases and are not added to the strict AR list.

The resulting catalogue has **160 unique papers**, **118 arXiv links**, and **68 source previews**. AR browsing shows **six papers: five primary-route entries plus one cross-listed dataset baseline**. The exclusive statistics remain five AR, 43 diffusion, 22 GAN, 53 rendering, and 37 supporting references. Supporting references comprise 18 foundations, 10 datasets, six evaluation papers, and three surveys. Filter counts can overlap because of cross-listing; chart counts cannot.

## Evidence and decisions

| Paper | Decision | Primary-source evidence |
| --- | --- | --- |
| [SpeakerVid-5M](https://arxiv.org/html/2507.09862v1#S5.SS1) | Cross-list the existing dataset's AR baseline | §§5.1–5.2 maintain dense 3D-VAE patch representations across causal audiovisual chunks. Spatial refinement and a shallow per-patch diffusion head emit visual latents for VAE decoding. This is visual state rather than a compact facial-motion controller. |
| [NOVA](https://arxiv.org/html/2412.14169v2) | Add as a general-video foundation | §§3.2–3.4 combine causal frame prediction, spatial token-set prediction, and a local continuous-token diffusion head. General video evidence is kept separate from avatar-specific deployment evidence. |
| [VideoPoet](https://arxiv.org/html/2312.14125v2) | Add as a general-video foundation | §3 describes a decoder-only language model over discrete video/audio tokens, with codec decoding and subsequent super-resolution. |
| [VideoGPT](https://arxiv.org/pdf/2104.10157) | Add as a general-video foundation | §3 trains a GPT prior over spatiotemporal VQ-VAE codes, then reconstructs video with the decoder. Human-action experiments do not establish a conversational-avatar system. |
| [Wan-Streamer v0.3](https://arxiv.org/html/2607.15038v2#S2.SS2) | Retain the existing diffusion entry | Conditional flow matching generates the continuous audiovisual latents. Its event stream is not a separate native visual-token AR generator. |
| [Vidu S2](https://arxiv.org/html/2609.11638v1#S2.SS2) | Add under diffusion | A joint audiovisual Diffusion Transformer uses block-causal denoising and Self-Replay Forcing. The paper covers avatar, editing, and spatial-video tasks. |
| [FlowAct-R2](https://arxiv.org/html/2609.35728v1#S2.SS1) | Add under diffusion | A reference-to-video DiT and diffusion forcing produce streaming video; a separate agent plans proactive behavior. |
| [PixReenact](https://arxiv.org/html/2610.05233v1) | Add under diffusion | §§3.2–3.4 adapt a dense video-diffusion backbone using causal masks and distillation. Driver conditioning includes one-latent lookahead; the catalogue does not claim zero-lookahead operation. |
| [Routed Forcing](https://arxiv.org/html/2609.30963v1) | Add under diffusion | §§3–4 route training supervision by semantic region and noise level. The causal student still generates dense video latents through iterative denoising. |
| [DynaForcing](https://arxiv.org/html/2608.17707v1) | Add under diffusion | Rollout anchors, dynamics rewards, reference variation, and gradient replay address motion collapse in a video-diffusion student. Reported throughput is not interpreted as a single-GPU result. |
| [Avatar-Forever](https://arxiv.org/html/2608.12107v1) | Add under diffusion | §§3.1–3.3 decouple few-step distillation and robustness training, then reuse history through ForeverCache. The visual generator remains a video-diffusion model. |
| [Wan-Animate-2](https://arxiv.org/abs/2608.06009) | Add one diffusion paper, identifying its Lite variant | The Lite variant uses chunk-causal denoising and self-forcing/distillation. Its streaming mechanism is not attributed to the Base variant, and a public Lite checkpoint is not inferred from other releases. |
| [Vorch-Streamer](https://arxiv.org/abs/2608.05663) | Add under diffusion | A block-causal audiovisual flow model jointly denoises audio and video. Speech-planning tokens do not replace the dense visual generator. |
| [Archon](https://arxiv.org/html/2605.30311v1#S3.SS3) | Retain as a documented AR boundary case | Its semantic masks are dense visual representations; a fully trained WALT video-diffusion backbone owns RGB appearance from semantic, identity, and text conditions. This exceeds a local AR emission head. |
| [Taming Transformer](https://arxiv.org/html/2508.14359v1) | Keep outside the strict AR list pending temporal-state evidence | §§3.2–3.4 and §4.2 establish AR over a single image's 256 spatial codes. §3.5 adds a previous-frame continuity loss, but does not clearly document inference-time causal visual history across frames. |

The last two decisions do not deny the use of autoregression. They preserve the survey's narrower requirement that AR own cross-frame appearance state. Their source links remain available in this review without assigning an unsupported native-AR label.

## Metadata and imagery

New metadata and summaries were checked against original paper records and method sections. NOVA uses its **ICLR 2025** edition and VideoPoet its **ICML 2024** edition, rather than the package's first-preprint dates of 2024 and 2023. SpeakerVid-5M retains the existing **2025** preprint citation; its **ICLR 2026** publication is documented separately. The other new entries use their verified arXiv editions. Each record states its source and year policy.

Avatar-Forever's project citation omits an author present in arXiv; Wan-Animate-2's repository citation has a placeholder identifier and an incomplete author list. Both entries follow the original arXiv metadata. DynaForcing's reported ACM Multimedia 2026 acceptance is recorded as an arXiv-sourced note. Wan-Animate-2 and Vorch-Streamer were checked against their current v2 texts.

Twelve new previews comprise the eleven added papers and SpeakerVid-5M's baseline architecture. Source-file SHA-256 hashes were checked against the supplied manifest. Images were resized and encoded as WebP with transparency preserved; they were not redrawn. Original figure numbers, image URLs, credits, and source hashes are retained in `assets/papers/manifest.json`.

The original collection, manuscript, and draft PDF were not modified. No unverified implementation, checkpoint, latency, or cross-paper speed claim is added to the site.
