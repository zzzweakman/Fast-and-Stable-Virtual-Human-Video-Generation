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

## Current survey — 31 October 2026

The current **46-page survey** is `1031_integrated_revision` v4, with **293 cited references** and **304 unique bibliography entries**. The website reproduces both updated main-text figures: the full **136-method timeline** with institution icons and solid/dashed branches, and **14 selected mechanism groups** with representative examples. Diffusion and visual AR each have three aligned groups; dense conditioned generation remains a short historical background in the text.

- [Current survey PDF](assets/survey/survey-measured-v12.pdf) and [complete source package](assets/survey/virtual-human-survey-measured-v12.zip).
- [Timeline PDF](assets/survey/timeline-2026-10-31.pdf) and [mechanism diagram PDF](assets/survey/taxonomy-2026-10-31.pdf).
- [Survey BibTeX](data/references-2026-10-31.bib), [method–citation mapping](data/figure-citation-audit-2026-10-31.csv), [revision notes](data/survey-update-2026-10-31.md), and [release manifest](data/snapshots/measured-v12/manifest.json).

The catalogue contains **220 unique papers**: 24 GAN, 75 diffusion, 69 rendering, six visual AR, and 46 supporting references. This revision adds 34 records and covers every timeline method. Its broader scope includes older methods and related work; catalogue totals differ from the selected timeline. Existing source previews remain available; newly added records without a crop use explicitly labelled text covers. Citation metadata follows the current manuscript where covered, without claiming a fresh DBLP or full-paper audit of every record.

The timeline caption highlights **solid branches: claimed real-time performance; dashed branches: real-time capability not reported**. Different sources use different hardware and timing boundaries. The representative mechanism diagram does not certify speed or stability. EMO and MultiTalk support continuation; longer output alone does not establish real-time or stable long-session operation.

## Current measured results

**51 measured configurations covering 51 methods** use one H200 each: 8 GAN, 16 diffusion, 26 rendering, and one UniLS motion visualization. Three complete warm-ups and three measured calls give **306 included calls**. The measurement values are unchanged; routes now follow the current manuscript.

- [Results page](measurements.html), [runtime CSV](data/h200-results-v12.csv), [runtime JSON](data/h200-results-v12.json), and [306 included calls](data/h200-trials-v12.csv).
- [HDTF CSV](data/hdtf-results-v12.csv), [StreamEval CSV](data/streameval-results-v12.csv), and [benchmark JSON](data/benchmark-results-v12.json).
- [Measurement protocol](data/h200-measurement-notes-v12.md) and [original 56-configuration archive](data/h200-results-2026-10-19.json), including [all 336 calls](data/h200-trials-2026-10-19.csv).

Load₁ is the loading interval in the first invocation, `warmup_01`. Pre, Gen, Post and Call summarize the later three measured calls. Initial loading cannot be added to warmed means to obtain a measured total. Ten configurations retain audited models; 41 reload models each call. Warm peak is the maximum NVML peak across measured calls. Call includes loading in that call; suite total covers the entire 3+3 process and is not TTFF.

HDTF reports 23 configurations on 40 matched fifteen-second cases. StreamEval reports six configurations on a 20% avatar-performance subset using local Qwen judges: Quality, Stability, Following and Identity. Synchronization and its dependent aggregate scores remain omitted. The fixed customization bonus is omitted because all tested configurations accept a supplied portrait. The subset and uncalibrated local judges limit comparison with published StreamEval scores.

Unless stated otherwise, inputs follow official README demos; Wav2Lip+GAN uses the EDTalk pair and FOMM uses the TPS pair. Detailed input, stage and attention-backend records remain in the downloads. Runtime workloads differ and do not establish a controlled quality/speed ranking or continuous-session stability. Public exports omit internal machine identifiers and absolute server paths.

Regenerate data from the preserved records and current manuscript:

```sh
python3 scripts/export_measurements.py --input data/h200-results-2026-10-19.json --manuscript-dir <current-manuscript> --output-dir <new-directory>
python3 scripts/export_benchmarks.py --manuscript-dir <current-manuscript> --output-dir <new-directory>
python3 scripts/render_measurements.py --output <new-html-file>
```

Copy exported files into `data/` before rendering. Run `npm test`, the Python unit tests and `scripts/build.py` before publishing. Checks reconcile selection, loading, statistics, phase unions, frame sequences, classification and HTML/CSV/JSON/source consistency. Preserve old releases and create a new snapshot for subsequent revisions. The [v11 manuscript](assets/survey/survey-measured-v11.pdf) and [v11 release](data/snapshots/measured-v11/manifest.json) remain archived.

## Archived DBLP manuscript and catalogue — 13 October 2026

The 13 October manuscript has **263 cited references** and 58 pages. Its archived catalogue has **185 unique papers**. Of 284 combined citation records, 270 matched DBLP: 252 of the 263 cited manuscript references and 180 of the 185 catalogue entries. The 14 unmatched records are retained with their original sources and listed explicitly; they are not declared DBLP-verified.

- [13 October survey PDF](assets/survey/survey-2026-10-13-dblp.pdf) and [complete source package](assets/survey/virtual-human-survey-dblp-2026-10-13.zip).
- [Reference update notes](data/dblp-update-2026-10-13.md), [catalogue BibTeX](data/references-dblp-2026-10-13.bib), [before/after metadata](data/dblp-reference-check-2026-10-13.json), and [release manifest](data/snapshots/2026-10-13-dblp/manifest.json).

Matched records use DBLP titles, ordered authors, condensed venues, citation years, pages and identifiers. Conference citation years follow the event year, as in DBLP BibTeX. Later version names such as JoyStreamer-Flash and FluentAvatar remain searchable and are explained alongside the DBLP titles JoyAvatar and AvatarSync. Source-specific method descriptions and measurements remain attached to the reviewed versions.

All earlier PDF files, source packages and frozen snapshots remain unchanged. The archived measurement template contains only a header; current results are linked above.

## Previous literature revision — 13 October 2026

That revision cites 263 references, including 26 selected additions checked against primary manuscripts. Its catalogue contains **185 unique papers with source previews**: 21 newly added records and five revised existing entries. Primary route totals are GAN 21, diffusion 53, visual AR 5, and rendering 59; 47 supporting references are counted separately.

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
- `assets/survey/survey-measured-v12.pdf`: current 31 October revision; `survey-measured-v11.pdf` preserves the 43-page revision; `survey-measured-v10.pdf` preserves the previous benchmark release; `survey-measured-v9.pdf` preserves the earlier runtime release; `survey-measured-v8.pdf` preserves the earlier output-crop revision; `survey-2026-10-13-dblp.pdf` preserves the 58-page DBLP revision; `survey-2026-10-13-literature.pdf` preserves the 55-page literature revision; `survey-2026-10-09-final.pdf` preserves the earlier illustrated revision.
- `assets/survey/survey-2026-10-09.pdf`: the preserved earlier revision associated with snapshot VH-2026-10-09.
- `assets/survey/survey.pdf`: the preserved draft reviewed on 9 October (`main_revised.pdf`, 48 pages).
- `assets/survey/provenance.json`: source information for the survey PDF and diagrams.
- `data/evidence-2026-10-09-final.json`: 57 inherited system records and 25 checked configuration/architecture records for 13 systems. OmniResponse adds a full configuration and two synchronization ablations.
- `data/omniresponse-review.md`: official-source checks and the distinction between AR response control and visual ownership.
- `data/configurations-2026-10-09-final.csv` and `data/cohort-2026-10-09.csv`: configuration and inherited-cohort exports.
- `data/evidence-guide-final.md`: selection, missing-value, source-edition, and mechanism-evidence conventions.
- `data/snapshots/2026-10-09-final/`: frozen catalogue and a manifest pairing its hashes with the revised PDF and evidence files.

Methods are assigned by the manuscript's **visual owner**, not solely by whether any component uses GANs, diffusion, autoregression, or rendering. Supporting foundations, datasets, evaluation work, surveys, and related methods retain their own categories. Verified baselines and explicitly labelled AR controllers may also appear in route browsing through `crossListings`. Route filters show names without counts; the landscape shows only overall publication totals by year, counting each source paper once across the full catalogue regardless of active filters. This avoids mixing overlapping browsing counts with exclusive category totals. The strict AR route requires temporal visual-state dependence; regional outputs and model variants are labelled explicitly. Years follow the current manuscript’s cited edition where covered; other records retain their documented bibliography year. Citation years may differ from the earliest preprint. Counts describe the curated collection and are not an exhaustive census or a speed leaderboard.

The supplied Feishu literature document returned HTTP 404 during preparation. The local CSV and two AR collections were reviewed against original papers. The archived 9 October catalogue contains **164 unique papers, all with source previews**; AR browsing shows **five visual-AR papers, three cross-listed baselines, and one AR controller**. The second pass added DualLip, the MMVID and ParaLip source papers, and spatial-AR context for Taming Transformer. That archived release treated FluentAvatar as related context. The current manuscript retains AvatarSync / FluentAvatar under visual AR while explicitly preserving the unresolved temporal and streaming boundaries. The review notes explain the evidence and survey implications. Source paper previews are reproduced for scholarly reference and remain attributable to their respective authors. The supplied missing-image package filled all 92 remaining preview gaps after checksum, original-source, and visual checks. A visibly labelled text cover remains the fallback if an image cannot load. Manrope is distributed under its included SIL Open Font License.

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
