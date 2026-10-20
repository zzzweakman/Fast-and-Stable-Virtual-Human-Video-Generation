# Fast and Stable Virtual Human Video Generation: A Survey

A research companion for the survey: searchable papers, source figure previews, source-specific operating conditions, bibliography downloads, and statistics derived from the catalogue.

**Website:** https://zzzweakman.github.io/Fast-and-Stable-Virtual-Human-Video-Generation/

The website is a static HTML/CSS/JavaScript application. It has no production dependencies, external image hosts, analytics, or API keys. GitHub Actions validates and publishes it to GitHub Pages on every push to `main`.

## Run locally

Python 3.10+ and Node.js 18+ are recommended. No package installation is needed.

```sh
npm test
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/build.py
python3 -m http.server 4173 --bind 127.0.0.1 --directory dist
```

Open http://127.0.0.1:4173. Serve over HTTP rather than opening the HTML as a local file, because the catalogue loads as JSON.

The build gives CSS and JavaScript files a shared content-based version, including module imports. Changes to the page, styles, or modules update their published URLs together, preventing cached assets from a previous layout from breaking the catalogue or annual chart.

## Runtime and memory results

**56 measured configurations covering 55 methods are available**, each using one H200. Every configuration executes three complete warm-ups followed by three measured calls in the same interpreter. All **336 calls** are included: 168 warm-ups and 168 measured repetitions. MuseTalk and VideoReTalking have completed remeasurements; SoulX-LiveAct, SoulX-FlashTalk, and both FlashHead Lite/Pro configurations now have results. Six additional diffusion implementations are also included.

- [View the results](https://zzzweakman.github.io/Fast-and-Stable-Virtual-Human-Video-Generation/measurements.html).
- Download the [summary CSV](data/h200-results-2026-10-19.csv), [full JSON](data/h200-results-2026-10-19.json), or [all 336 calls](data/h200-trials-2026-10-19.csv).
- Read the [measurement protocol](data/h200-measurement-notes-v4.md) and [release manifest](data/snapshots/measured-v7/manifest.json).
- Read the [updated survey PDF](assets/survey/survey-measured-v7.pdf) or download its [source package](assets/survey/virtual-human-survey-measured-v7.zip).

The current **55-page survey** uses the ten newly cropped vector figures, with captions and body references updated to match the removed headers, footers and embedded table. The single-H200 stage-cost figure now shows only stage shares; the text points to the main measurement tables for absolute times and output sizes. Long notes below all four measurement tables have been consolidated into the shared protocol, route-specific discussion and short captions. Publication-year columns in **15 tables**, four **Takeaways cards**, two-column appendix text, all measurement values and the cited references are retained. The source package includes the revision and layout reports.

The table reports measured-call means and Call ± sample standard deviation. **Call** spans inference entry to synchronized return; **Suite total** spans setup, all six calls, QA and shutdown. The suite total is not a single-call latency and must not be divided by six to estimate measured latency. Fifteen configurations retain audited model objects or a GPU worker; 41 reload each call. Inputs, supplied assets and software differ.

The main result tables show **Warm peak**, the maximum NVML peak over the three measured calls after warm-up: **9.49 GiB for MuseTalk and 16.01 GiB for VideoReTalking**. The revised manuscript removes calendar dates from its narrative, tables and reference notes while retaining bibliographic publication years. Wan's actual final frame counts remain **35 / 33 / 34**, and unrecorded load intervals remain null/NR.

Coverage is 11 GAN, 20 diffusion, 24 rendering configurations and one UniLS motion visualization. FlashHead Lite/Pro account for the configuration/method count difference. Native visual-AR coverage is zero. These measurements do not establish a matched quality/speed ranking, TTFF or continuous-session stability. Full sampling/decoder settings for the six additional configurations were not supplied; attention labels are historical execution or source/configuration evidence, not fresh kernel captures.

The supplied workbook and README contain the evidence for this integration. All summaries were reconciled with individual workbook calls. Referenced server-side traces, a separate JSON delivery and videos were not supplied for independent inspection. Public exports omit internal machine identifiers and paths.

Regenerate the public files with `scripts/export_measurements.py --input <verified-h200_results.json> --output-dir <new-directory>` and the static page with `scripts/render_measurements.py --output <new-file>`. Run `npm test`, Python unit tests and `scripts/build.py` before publishing. Validation checks means/SDs, memory windows, phase unions, frame sequences and HTML/CSV/JSON consistency. The static tables work without JavaScript.

The [16 October data](data/h200-results-2026-10-16.json) remains an archived release of 44 published single-run results and five pending entries; its protocol differs from this repeated-call release.

## Archived DBLP manuscript and catalogue — 13 October 2026

The 13 October manuscript has **263 cited references** and 58 pages. The website retains **185 unique papers**. Of 284 combined citation records, 270 matched DBLP: 252 of the 263 cited manuscript references and 180 of the 185 website entries. The 14 unmatched records are retained with their original sources and listed explicitly; they are not declared DBLP-verified.

- [13 October survey PDF](assets/survey/survey-2026-10-13-dblp.pdf) and [complete source package](assets/survey/virtual-human-survey-dblp-2026-10-13.zip).
- [Reference update notes](data/dblp-update-2026-10-13.md), [catalogue BibTeX](data/references-dblp-2026-10-13.bib), [before/after metadata](data/dblp-reference-check-2026-10-13.json), and [release manifest](data/snapshots/2026-10-13-dblp/manifest.json).

Matched records use DBLP titles, ordered authors, condensed venues, citation years, pages and identifiers. Conference citation years follow the event year, as in DBLP BibTeX. Later version names such as JoyStreamer-Flash and FluentAvatar remain searchable and are explained alongside the DBLP titles JoyAvatar and AvatarSync. Source-specific method descriptions and measurements remain attached to the reviewed versions.

All earlier PDF files, source packages and frozen snapshots remain unchanged. The archived measurement template contains only a header; current results are linked above.

## Previous literature revision — 13 October 2026

The manuscript now cites 263 references, including 26 selected additions checked against primary manuscripts. The catalogue contains **185 unique papers with source previews**: 21 newly added records and five revised existing entries. Primary route totals are GAN 21, diffusion 53, visual AR 5, and rendering 59; 47 supporting references are counted separately.

- [Revised survey PDF](assets/survey/survey-2026-10-13-literature.pdf) and [complete source package](assets/survey/virtual-human-survey-literature-2026-10-13.zip).
- [Literature update notes](data/literature-update-2026-10-13.md), [added BibTeX](data/literature-additions-2026-10-13.bib), and [release manifest](data/snapshots/2026-10-13-literature/manifest.json).
- [Measurement template](data/measurement-template-2026-10-13.csv): header only. The authors will measure output frames, resolution, preprocessing/generation/postprocessing time, and peak GPU memory for all open-source methods in a common environment. This historical template predates the measurements linked above.

Cards describe methods and original-source measurements in plain language. The current literature annotations use `mechanisms` with a code, explanation, and primary-source URL. L2 requires bounded recent and older memory with an update policy; a within-chunk feature cache alone does not qualify. Existing source configuration records remain available without displaying the earlier assessment labels.

## Content and preserved sources

- `data/papers.json`: curated records, summaries, DBLP-aligned bibliography entries where matched, and manuscript provenance.
- `data/catalog-notes.md`: selection policy and source limitations.
- `data/ar-supplement-notes.md`: review of all 28 AR-labelled CSV rows, including the later correction to FluentAvatar's classification.
- `data/ar-collection-review.md`: review of the 15-paper AR collection, baseline cross-listing, foundations, and streaming-diffusion additions.
- `data/ar-second-pass-review.md`: historical AR additions, spatial and unresolved boundary cases, and recommended survey placements.
- `data/image-supplement-review.md` and `data/image-supplement-audit.json`: validation and source checks for the 92 supplied missing previews.
- `assets/papers/manifest.json`: preview provenance, source pages, figure captions, and image paths.
- `assets/survey/survey-measured-v7.pdf`: current measured revision; `survey-2026-10-13-dblp.pdf` preserves the 58-page DBLP revision; `survey-2026-10-13-literature.pdf` preserves the 55-page literature revision; `survey-2026-10-09-final.pdf` preserves the earlier illustrated revision.
- `assets/survey/survey-2026-10-09.pdf`: the preserved earlier revision associated with snapshot VH-2026-10-09.
- `assets/survey/survey.pdf`: the preserved draft reviewed on 9 October (`main_revised.pdf`, 48 pages).
- `assets/survey/provenance.json`: source information for the survey PDF and diagrams.
- `data/evidence-2026-10-09-final.json`: 57 inherited system records and 25 checked configuration/architecture records for 13 systems. OmniResponse adds a full configuration and two synchronization ablations.
- `data/omniresponse-review.md`: official-source checks and the distinction between AR response control and visual ownership.
- `data/configurations-2026-10-09-final.csv` and `data/cohort-2026-10-09.csv`: configuration and inherited-cohort exports.
- `data/evidence-guide-final.md`: selection, missing-value, source-edition, and mechanism-evidence conventions.
- `data/snapshots/2026-10-09-final/`: frozen catalogue and a manifest pairing its hashes with the revised PDF and evidence files.

Methods are assigned by the manuscript's **visual owner**, not solely by whether any component uses GANs, diffusion, autoregression, or rendering. Supporting foundations, datasets, evaluation work, surveys, and related methods retain their own categories. Verified baselines and explicitly labelled AR controllers may also appear in route browsing through `crossListings`. Route filters show names without counts; the landscape shows only overall publication totals by year, counting each source paper once across the full catalogue regardless of active filters. This avoids mixing overlapping browsing counts with exclusive category totals. The strict AR route requires temporal visual-state dependence; regional outputs and model variants are labelled explicitly. Years follow the DBLP citation edition where matched; unmatched records retain their original-source year. Citation years may differ from the earliest preprint. Counts describe the curated collection and are not an exhaustive census or a speed leaderboard.

The supplied Feishu literature document returned HTTP 404 during preparation. The local CSV and two AR collections were reviewed against original papers. The archived 9 October catalogue contains **164 unique papers, all with source previews**; AR browsing shows **five visual-AR papers, three cross-listed baselines, and one AR controller**. The second pass added DualLip, the MMVID and ParaLip source papers, and spatial-AR context for Taming Transformer. FluentAvatar remains available as related context because its strict temporal dependence is unresolved. The review notes explain the evidence and survey implications. Source paper previews are reproduced for scholarly reference and remain attributable to their respective authors. The supplied missing-image package filled all 92 remaining preview gaps after checksum, original-source, and visual checks. A visibly labelled text cover remains the fallback if an image cannot load. Manrope is distributed under its included SIL Open Font License.

## Update the catalogue

Add or revise a record in `data/papers.json`, keeping its citation key unique. Required fields are checked by `scripts/validate.py`. Provide an original paper URL, a faithful one- or two-sentence summary, the primary category, bibliography year, mechanism tags, and BibTeX. Every record should identify its manuscript/bibliography or supplied-literature source. Mark supplemental records explicitly and verify their classification against the original paper.

To expose a separately verified baseline or AR controller from an existing paper, add a `crossListings` entry with `route`, `label`, `summary`, and an HTTPS `evidenceUrl`; optional `shortTitle` and `tags` identify it in its route view and search. Set `kind: "controller"` for an AR control branch whose appearance owner belongs to another route; the default is `baseline`. Reuse the same record and BibTeX. `countRoutes` and `countBrowseRoutes` remain available to validate exclusive categories and overlapping browsing membership, respectively; neither supplies a visible category count. General-video AR foundations use the `AR foundations` tag. Spatial and unresolved AR cases use category `context` and the `AR scope context` tag, without a strict-AR cross-listing.

For a preview, add an optimized image under `assets/papers/` and an entry keyed by the paper's citation ID in `assets/papers/manifest.json`. Include the original source URL, caption, and figure/page provenance; do not fabricate a paper preview. `heroPath` optionally points to a larger source crop.

Run the tests and build, then commit and push. The Pages workflow publishes only the packaged `dist/` directory; development notes, tests, and design records are excluded.

## Preserved 9 October source records

The 9 October revision uses documented source collections and a retrospective audit, not an undocumented systematic-search claim. Each checked configuration identifies a primary-source edition, SHA256 hash, page/table/section location, timing boundary, and explicit field status. Do not average values across configurations or treat missing fields as zero. Live Avatar v6's Table 3/Table 10 TTFF discrepancy is retained as a conflict. REA-Listener's unavailable primary paper remains an inherited, unverified cohort record and does not support the new quantitative analyses.

`evidence.js` attaches configurations to catalogue records. Every linked record must list the matching `evidenceIds`; validation checks these links. The archived records retain their original architecture and assessment fields. Current cards display the mechanism and source conditions without the old assessment labels; filters accept documented archived mechanisms and the new primary-source `mechanisms` records. L4-G and L4-C distinguish generated from corrupted ground-truth histories. Hypotheses alone do not create filter matches. The audit is selective: a paper without an evidence disclosure has not thereby been shown to lack measurements.

StyleAvatar is now rendering-primary under the same geometric-reuse rule used for LivePortrait. The frozen 9 October counts are GAN 21, diffusion 43, AR 5, and rendering 54, for 123 primary method papers; current counts are given above. ART-V links to the cited CVPR proceedings rather than silently mixing its table with arXiv editions. Every card exposes catalogue provenance, including records without a detailed measurement extraction.

OmniResponse is cited as NeurIPS 2025; its stable catalogue ID retains the old year to preserve preview and external links. Its source-reported 64 ms has unspecified timing endpoints and must not be presented as TTFF. The illustrated manuscript, evidence, and catalogue are paired in the final archive; earlier frozen releases remain unchanged.

Preserve dated snapshots when adding later evidence. Create a new snapshot identifier and record its manifest, then update the display and tests. Use `python3 scripts/build.py --output /tmp/a-new-site-build-directory` to package an isolated preview without changing an earlier build. Search supports Ctrl/Cmd+K; bare character keys are not intercepted.

## Contributions

Open an issue with a source link for missing papers, metadata fixes, or taxonomy questions. Link verification is a point-in-time check; external publishers can change URLs or restrict automated access.
