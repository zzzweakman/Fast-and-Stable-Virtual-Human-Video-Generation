# Literature catalogue provenance

Prepared on 9 October 2026 from the manuscript rooted at `virtual-human-survey/1008_overleaf/main.tex`, its `sec_new` sections, and ten bibliography files. No manuscript source was edited.

The catalogue contains **149 distinct bibliography records** with original-paper or author-hosted links, including **107 arXiv links**. Every named method in the comparison tables of all four route sections is represented. The collection also includes selected methods discussed in the surrounding text, the verified FluentAvatar addition from the supplied CSV, ten dataset papers, six evaluation references, fifteen foundational/contextual papers, and three related surveys. It is a curated view of this draft and its supplied literature, not a complete census of the field or an exhaustive export of its bibliography.

| Category | Records |
| --- | ---: |
| GAN-based | 22 |
| Diffusion-based | 35 |
| Native visual autoregressive | 5 |
| Render-based | 53 |
| Foundations and general-video context | 15 |
| Datasets | 10 |
| Evaluation | 6 |
| Related surveys | 3 |

## Classification and summaries

Category follows the manuscript's **visual ownership** test, rather than the filename of a bibliography or the presence of an autoregressive/diffusion controller. For example, MuseTalk is a one-call adversarial latent generator; MIDAS has a native visual-AR backbone with a local diffusion head; and Teller, ARIG, DyStream, UniTalker, and OmniResponse use compact controls followed by a renderer. MIDAS, Body of Her, UniMo, EARTalking, and FluentAvatar are counted as native visual AR. The user explicitly confirmed this strict definition for the CSV supplement; see [the AR review](ar-supplement-notes.md).

The 115 records assigned to the four routes include general-video bridges and contextual controller systems described by the survey. The remaining 34 supporting references are counted separately. MotionStream is general motion-controlled video, UniMo bridges general human video and motion, and the Wan-Streamer records are successive versions of one series. Counts measure records in this catalogue, not independent architectures, research quality, performance, or adoption.

Summaries mainly paraphrase the manuscript's mechanism descriptions in one or two sentences. For Vidu S1, Rolling Forcing, Forcing-KV, and FlowCache, the original arXiv abstracts supplement the manuscript's brief contextual mentions. FluentAvatar's summary and route assignment were checked against Sections 3.1–3.3 of the original paper's v3. Tags describe mechanisms or tasks and are editorial annotations. `featured` marks eight examples for navigation, not a ranking.

## Metadata and links

`id` preserves the manuscript citation key, including punctuation. `bibtex` retains the original raw bibliography entry. Titles and author display names receive light capitalization, spacing, and TeX-accent cleanup. `year` always retains the bibliography year, which may differ from the first arXiv submission or paginated journal issue. Authors are not expanded beyond those listed in the supplied bibliography.

Missing links were resolved through exact title matching in official CVF proceedings and searches of original arXiv records, publisher records, or author project pages. Every record has a nonempty HTTPS article/project link; **no link remains unresolved**. A direct publisher or author link is retained when no arXiv identifier was established. This is source resolution, not a promise that every external server will remain available or allow automated access.

`source` records the bibliography and manuscript citation locations. `section` names an actual section in which the work is cited; it can differ from the assigned category. Supplemental entries instead identify their CSV paper ID and use an explicit supplement label, without claiming a manuscript citation. `provenance` records the metadata/year policy, link source, and known ambiguities. The original Feishu URL was unavailable; its subsequently supplied local `data.csv` was reviewed specifically for AR coverage. Private CSV comments and creator fields are not published.

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

A bounded HTTP check of the original 148 links plus the newly added FluentAvatar link returned **141 HTTP 200 responses**, three HTTP 403 responses from ACM, and five HTTP 202 responses from IEEE. There were no HTTP 404 responses or request timeouts. The eight publisher responses below do not establish that an article is unavailable in a browser; its DOI and paper identity were resolved independently. Full results are retained in `link-audit.json`.

| Automated-access response | Records |
| --- | --- |
| ACM HTTP 403 | VPGC; GaussianTalker by Yu et al.; NeRSemble |
| IEEE HTTP 202 | RC-SMPL; GaussianHand; HDTF; VFHQ; SSIM |

## Validation

Validated JSON structure; unique citation keys; required nonempty metadata; valid category names; numeric bibliography years; 149 direct links; 107 arXiv identifiers; eight featured entries; manuscript or explicit CSV provenance; and full named-method coverage of all four route comparison tables. Publication links added beyond the bibliography were checked against original source records or official proceedings indexes. The underlying research results were not independently reproduced.
