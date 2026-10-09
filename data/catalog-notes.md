# Literature catalogue provenance

Prepared on 9 October 2026 from the manuscript rooted at `virtual-human-survey/1008_overleaf/main.tex`, its `sec_new` sections, and ten bibliography files. No manuscript source was edited.

The catalogue contains **148 distinct bibliography records** with original-paper or author-hosted links, including **106 arXiv links**. Every named method in the comparison tables of all four route sections is represented. The collection also includes selected methods discussed in the surrounding text, ten dataset papers, six evaluation references, fifteen foundational/contextual papers, and three related surveys. It is a curated view of this draft, not a complete census of the field or an exhaustive export of its bibliography.

| Category | Records |
| --- | ---: |
| GAN-based | 22 |
| Diffusion-based | 35 |
| Native visual autoregressive | 4 |
| Render-based | 53 |
| Foundations and general-video context | 15 |
| Datasets | 10 |
| Evaluation | 6 |
| Related surveys | 3 |

## Classification and summaries

Category follows the manuscript's **visual ownership** test, rather than the filename of a bibliography or the presence of an autoregressive/diffusion controller. For example, MuseTalk is a one-call adversarial latent generator; MIDAS has a native visual-AR backbone with a local diffusion head; and Teller, ARIG, DyStream, UniTalker, and OmniResponse use compact controls followed by a renderer. Only MIDAS, Body of Her, UniMo, and EARTalking are counted as native visual AR.

The 114 records assigned to the four routes include general-video bridges and contextual controller systems described by the survey. The remaining 34 supporting references are counted separately. MotionStream is general motion-controlled video, UniMo bridges general human video and motion, and the Wan-Streamer records are successive versions of one series. Counts measure records in this catalogue, not independent architectures, research quality, performance, or adoption.

Summaries paraphrase the manuscript's mechanism descriptions in one or two sentences. For Vidu S1, Rolling Forcing, Forcing-KV, and FlowCache, the original arXiv abstracts supplement the manuscript's brief contextual mentions. Tags describe mechanisms or tasks and are editorial annotations. `featured` marks eight examples for navigation, not a ranking.

## Metadata and links

`id` preserves the manuscript citation key, including punctuation. `bibtex` retains the original raw bibliography entry. Titles and author display names receive light capitalization, spacing, and TeX-accent cleanup. `year` always retains the bibliography year, which may differ from the first arXiv submission or paginated journal issue. Authors are not expanded beyond those listed in the supplied bibliography.

Missing links were resolved through exact title matching in official CVF proceedings and searches of original arXiv records, publisher records, or author project pages. Every record has a nonempty HTTPS article/project link; **no link remains unresolved**. A direct publisher or author link is retained when no arXiv identifier was established. This is source resolution, not a promise that every external server will remain available or allow automated access.

`source` records the bibliography and manuscript citation locations. `section` names an actual section in which the work is cited; it can differ from the assigned category. `provenance` records the metadata/year policy, link source, and known ambiguities. The incomplete Feishu document was not independently incorporated into this catalogue; the local draft and original-paper sources determine this dataset.

## Preserved evidence boundaries

- The two GaussianTalker papers have separate records and explicit author-qualified display names.
- Wav2Lip + GAN shares a citation with the base Wav2Lip model; the category refers to the GAN variant.
- SqueezeMe's early arXiv title and author order differ from the later SIGGRAPH version. The catalogue retains the manuscript's published-version metadata, corroborated by the [author project page](https://forresti.github.io/squeezeme/).
- OmniTalker's linked preprint title differs from the later title used by the manuscript. GaussianHand has a 2024 early-online year and a 2025 paginated volume. These differences are documented per record.
- Live Avatar and SoulX-FlashHead have timing/hardware ambiguities described in the manuscript. No cross-paper speed ranking is derived from them.
- HDTF, TalkVerse, and NeRSemble each also introduce a method, but are counted once under datasets according to their role in this catalogue.
- Demonstration duration, claimed horizon, media frame rate, measured throughput, and end-to-end latency are different quantities. The site should not infer a stability or speed leaderboard from architecture labels or these brief summaries.

The asset manifest may contain previews for seven additional bibliography records that were not selected for this catalogue: MaineCoon, Towards Interactive Intelligence for Digital Humans, EchoAvatar, Avatar Forcing, IF-MDM, ViSA, and SadTalker. Asset availability alone does not determine inclusion or route assignment.

## External availability check

A bounded HTTP check of all 148 links returned **140 HTTP 200 responses**, three HTTP 403 responses from ACM, and five HTTP 202 responses from IEEE. There were no HTTP 404 responses or request timeouts. The eight publisher responses below do not establish that an article is unavailable in a browser; its DOI and paper identity were resolved independently. Full results are retained in `link-audit.json`.

| Automated-access response | Records |
| --- | --- |
| ACM HTTP 403 | VPGC; GaussianTalker by Yu et al.; NeRSemble |
| IEEE HTTP 202 | RC-SMPL; GaussianHand; HDTF; VFHQ; SSIM |

## Validation

Validated JSON structure; unique citation keys; required nonempty metadata; valid category names; numeric bibliography years; 148 direct links; 106 arXiv identifiers; eight featured entries; actual manuscript citation provenance; and full named-method coverage of all four route comparison tables. Publication links added beyond the bibliography were checked against original source records or official proceedings indexes. The underlying research results were not independently reproduced.
