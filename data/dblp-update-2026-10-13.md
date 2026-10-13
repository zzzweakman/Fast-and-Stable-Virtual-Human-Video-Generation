# Reference update — 13 October 2026

Bibliographic metadata now follows the [DBLP computer science bibliography](https://dblp.org/), retrieved through its [official SPARQL service](https://sparql.dblp.org/). Matching uses titles, authors and source identifiers; identical titles alone are insufficient.

## Coverage

| Scope | Records | Matched in DBLP | No matching record found |
|---|---:|---:|---:|
| Manuscript bibliography files | 274 | 261 | 13 |
| References actually cited in the manuscript | 263 | 252 | 11 |
| Website catalogue | 185 | 180 | 5 |
| Combined citation records | 284 | 270 | 14 |

These sets overlap. Ten website citations are absent from the manuscript bibliography; eleven manuscript bibliography entries are not cited in the PDF. No paper was added or removed in this update. A missing DBLP match does not establish that a paper or standard is invalid.

## Changes

The update aligns titles, author order, venue, year, pages or article identifiers, DOI and citation type. Fifteen preprint citations now use an indexed proceedings version. Venue names use DBLP’s condensed form. Values absent from DBLP are omitted rather than asserted to be incorrect. Full before/after metadata and persistent record links are available in the [reference check file](dblp-reference-check-2026-10-13.json).

Conference citations use DBLP’s event year; journal articles and preprints use their publication year. DBLP separately records the publication year of a proceedings volume, which can differ. For example, EDTalk remains ECCV 2024, and Out of Time remains ACCV Workshops 2016. The annual chart counts each catalogue record once using its citation year. Earlier releases retain their original metadata.

## Version names

- [JoyAvatar](https://dblp.org/rec/journals/corr/abs-2512-11423) is DBLP’s title for arXiv:2512.11423. The catalogue discusses its v3, titled JoyStreamer-Flash; the method name, version-specific source link and measurements remain associated with v3. It is distinct from the JoyAvatar paper at arXiv:2602.00702.
- [AvatarSync](https://dblp.org/rec/journals/corr/abs-2509-12052) is DBLP’s title for arXiv:2509.12052. The reviewed v3 is called FluentAvatar. Both names remain searchable; its unresolved temporal-AR classification is unchanged.
- [MuseTalk](https://dblp.org/rec/journals/corr/abs-2410-10122) uses DBLP’s title and author order. The method description still identifies the reviewed source version.

Bibliographic updates do not reassign mechanisms or transfer measurements between publication versions. The paper-reading links continue to identify the reviewed source; DBLP record links identify the bibliography edition.

## Catalogue entries without a DBLP match

These entries retain their original-source citations and are identified in the citation panel. They are not labelled DBLP-verified.

- [FlowAct-R2: Beyond Talking Avatar via Streaming Multimodal References and Proactive Agent Planning](https://arxiv.org/abs/2609.35728v1) (`huang2026flowactr2`).
- [Where and When to Force: Routed Forcing for Streaming Avatars](https://arxiv.org/abs/2609.30963v1) (`su2026routedforcing`).
- [Beyond Lip Sync: Reference-Grounded Oral Refinement for Audio-Driven Portrait Animation](https://arxiv.org/abs/2609.38019v1) (`tang2026rgor`).
- [Talk Like You: Imitating How You Speak in Real-Time Talking Head Generation](https://arxiv.org/abs/2610.06658v1) (`wang2026talklikeyou`).
- [PixReenact: Pixel-Conditioned Causal Video Diffusion for Streaming Head-Avatar Reenactment](https://arxiv.org/abs/2610.05233) (`habib2026pixreenact`).

Other unmatched manuscript items include technical standards, reports, an unpublished survey and older non-CS material; the full list is in the reference check file.

## Downloads

- [Current survey PDF](../assets/survey/survey-2026-10-13-dblp.pdf).
- [Complete source package](../assets/survey/virtual-human-survey-dblp-2026-10-13.zip).
- [All 185 catalogue citations](references-dblp-2026-10-13.bib), including the five retained original-source citations.
- [Release manifest](snapshots/2026-10-13-dblp/manifest.json).

The manuscript still cites 263 references. The common-environment runtime and GPU-memory measurements remain pending, and the measurement template contains no results.
