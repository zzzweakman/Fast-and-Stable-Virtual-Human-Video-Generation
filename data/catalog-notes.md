# Literature catalogue provenance

Prepared on 9 October 2026 from the manuscript rooted at `virtual-human-survey/1008_overleaf/main.tex`, its `sec_new` sections, and ten bibliography files. No manuscript source was edited.

The catalogue contains **164 distinct bibliography records** with original-paper or author-hosted links, including **122 arXiv links**. Every named method in the comparison tables of all four route sections is represented. The collection also includes selected methods discussed in the surrounding text, verified additions from the supplied CSV and two AR collections, ten dataset papers, six evaluation references, eighteen foundations, three related surveys, and four related-method records. It is a curated view of this draft and its supplied literature, not a complete census of the field or an exhaustive export of its bibliography.

| Category | Records |
| --- | ---: |
| GAN-based | 22 |
| Diffusion-based | 43 |
| Temporal visual autoregressive (including regional DualLip) | 5 |
| Render-based | 53 |
| Foundations and general-video context | 18 |
| Datasets | 10 |
| Evaluation | 6 |
| Related surveys | 3 |
| Related methods and AR scope context | 4 |

## Classification and summaries

Category follows the manuscript's **visual ownership** test, rather than the filename of a bibliography or the presence of an autoregressive/diffusion controller. For example, MuseTalk is a one-call adversarial latent generator; MIDAS has a native visual-AR backbone with a local diffusion head; and Teller, ARIG, DyStream, UniTalker, and OmniResponse use compact controls followed by a renderer. MIDAS, Body of Her, UniMo, EARTalking, and DualLip's without-duration lip-region branch are primary temporal visual AR. The user explicitly confirmed the strict temporal definition. FluentAvatar's earlier inclusion was corrected after a method re-audit; it remains related context with temporal dependence unresolved. See [the second-pass review](ar-second-pass-review.md).

The 123 records assigned to the four routes include general-video bridges, historical regional methods, and contextual controller systems described by the survey. The remaining 41 supporting references are counted separately. MotionStream is general motion-controlled video, UniMo bridges general human video and motion, and the Wan-Streamer records are successive versions of one series. Counts measure records in this catalogue, not independent architectures, full-avatar systems, research quality, performance, or adoption.

Three verified visual-AR baselines are cross-listed: SpeakerVid-5M stays under datasets, while ART-V and TransformerT2L retain the MMVID and ParaLip source papers under Related methods. Thus AR navigation contains eight papers, while the exclusive chart records five primary AR papers. MMVID and ParaLip's main methods are not classified as AR. NOVA, VideoPoet, and VideoGPT remain supporting general-video foundations; FluentAvatar and Taming Transformer have a separate spatial/unresolved-AR context link. See the [15-paper collection review](ar-collection-review.md) and [second-pass review](ar-second-pass-review.md) for evidence and decisions.

Summaries mainly paraphrase the manuscript's mechanism descriptions in one or two sentences. For Vidu S1, Rolling Forcing, Forcing-KV, and FlowCache, the original arXiv abstracts supplement the manuscript's brief contextual mentions. FluentAvatar and both AR collections use verified original method sections, with uncertainties recorded explicitly. Cross-listed baselines have separate source-backed titles, summaries, and optional tags for their route view. Tags describe mechanisms or tasks and are editorial annotations. `featured` marks eight examples for navigation, not a ranking.

## Metadata and links

`id` preserves the manuscript citation key or supplied collection identifier. Manuscript-derived `bibtex` retains its original raw entry; supplemental citations use official publication exports or verified arXiv metadata. An official BibTeX key can differ from the collection ID and is recorded in `source.citationKey`. Titles and author display names receive light capitalization, spacing, and TeX-accent cleanup. `year` follows the cited bibliography edition, which may differ from the first arXiv submission or paginated journal issue. Original manuscript author lists are preserved; new records use verified primary-source author lists.

Missing links were resolved through exact title matching in official CVF proceedings and searches of original arXiv records, publisher records, or author project pages. Every record has a nonempty HTTPS article/project link; **no link remains unresolved**. A direct publisher or author link is retained when no arXiv identifier was established. This is source resolution, not a promise that every external server will remain available or allow automated access.

`source` records the bibliography and manuscript citation locations. `section` names an actual section in which the work is cited; it can differ from the assigned category. Supplemental entries instead identify their CSV or collection paper ID and use an explicit supplement label, without claiming a manuscript citation. `provenance` records the metadata/year policy, link source, and known ambiguities. The original Feishu URL was unavailable; its subsequently supplied local `data.csv`, `AR_Paper_Collection`, and `AR_Second_Pass_Supplement` informed the additions. Private CSV comments and creator fields are not published.

## Preserved evidence boundaries

- The two GaussianTalker papers have separate records and explicit author-qualified display names.
- Wav2Lip + GAN shares a citation with the base Wav2Lip model; the category refers to the GAN variant.
- SqueezeMe's early arXiv title and author order differ from the later SIGGRAPH version. The catalogue retains the manuscript's published-version metadata, corroborated by the [author project page](https://forresti.github.io/squeezeme/).
- OmniTalker's linked preprint title differs from the later title used by the manuscript. GaussianHand has a 2024 early-online year and a 2025 paginated volume. These differences are documented per record.
- Live Avatar and SoulX-FlashHead have timing/hardware ambiguities described in the manuscript. No cross-paper speed ranking is derived from them.
- HDTF, TalkVerse, and NeRSemble each also introduce a method, but are counted once under datasets according to their role in this catalogue.
- Demonstration duration, claimed horizon, media frame rate, measured throughput, and end-to-end latency are different quantities. The site should not infer a stability or speed leaderboard from architecture labels or these brief summaries.

All 164 catalogue papers now have source previews. The supplied `Missing_Paper_Images` collection added 92 verified figures to the previous 72, with English captions and preserved attribution. The new images were checked against original PDFs or author-hosted images and optimized to 7.4 MB in total. See the [image-supplement review](image-supplement-review.md) and its file-level audit for validation details, source edition notes, and the SyncTalk++ filename adjustment. Paper counts and classification were not changed by the image update.

The asset manifest also contains previews for seven additional bibliography records that were not selected for this catalogue: MaineCoon, Towards Interactive Intelligence for Digital Humans, EchoAvatar, Avatar Forcing, IF-MDM, ViSA, and SadTalker. Asset availability alone does not determine inclusion or route assignment.

## External availability check

Bounded HTTP checks of the original 148 links and 16 supplemental links returned **156 HTTP 200 responses**, three HTTP 403 responses from ACM, and five HTTP 202 responses from IEEE. There were no HTTP 404 responses or request timeouts. The eight publisher responses below do not establish that an article is unavailable in a browser; its DOI and paper identity were resolved independently. Full results are retained in `link-audit.json`.

| Automated-access response | Records |
| --- | --- |
| ACM HTTP 403 | VPGC; GaussianTalker by Yu et al.; NeRSemble |
| IEEE HTTP 202 | RC-SMPL; GaussianHand; HDTF; VFHQ; SSIM |

## Validation

Validation covers JSON structure; unique record and citation keys; required nonempty metadata; valid category names; numeric bibliography years; 164 direct links; 122 arXiv identifiers; eight featured entries; manuscript or explicit supplement provenance; cross-listing evidence; and full named-method coverage of all four route comparison tables. Regression checks cover baseline discovery without duplicate counts, regional scope, and exclusion of spatial/unresolved cases from strict temporal-AR statistics. Publication links added beyond the bibliography were checked against original source records or official proceedings indexes. The underlying research results were not independently reproduced.
