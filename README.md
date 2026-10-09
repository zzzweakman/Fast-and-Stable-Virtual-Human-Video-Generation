# Fast and Stable Virtual Human Video Generation: A Survey

A research companion for the survey: searchable papers, source figure previews, configuration-level Fast/Stable evidence, bibliography downloads, and statistics derived from the catalogue.

**Website:** https://zzzweakman.github.io/Fast-and-Stable-Virtual-Human-Video-Generation/

The website is a static HTML/CSS/JavaScript application. It has no production dependencies, external image hosts, analytics, or API keys. GitHub Actions validates and publishes it to GitHub Pages on every push to `main`.

## Run locally

Python 3.10+ and Node.js 18+ are recommended. No package installation is needed.

```sh
npm test
python3 scripts/build.py
python3 -m http.server 4173 --bind 127.0.0.1 --directory dist
```

Open http://127.0.0.1:4173. Serve over HTTP rather than opening the HTML as a local file, because the catalogue loads as JSON.

## Content and sources

- `data/papers.json`: curated records, summaries, original bibliography entries, and manuscript provenance.
- `data/catalog-notes.md`: selection policy and source limitations.
- `data/ar-supplement-notes.md`: review of all 28 AR-labelled CSV rows, including the later correction to FluentAvatar's classification.
- `data/ar-collection-review.md`: review of the 15-paper AR collection, baseline cross-listing, foundations, and streaming-diffusion additions.
- `data/ar-second-pass-review.md`: historical AR additions, spatial and unresolved boundary cases, and recommended survey placements.
- `data/image-supplement-review.md` and `data/image-supplement-audit.json`: validation and source checks for the 92 supplied missing previews.
- `assets/papers/manifest.json`: preview provenance, source pages, figure captions, and image paths.
- `assets/survey/survey-2026-10-09.pdf`: the manuscript revision associated with snapshot VH-2026-10-09.
- `assets/survey/survey.pdf`: the preserved draft reviewed on 9 October (`main_revised.pdf`, 48 pages).
- `assets/survey/provenance.json`: source information for the survey PDF and diagrams.
- `data/evidence-2026-10-09.json`: 57 inherited system records and 22 freshly checked configuration/architecture records for 12 systems. These levels of verification are deliberately distinct.
- `data/configurations-2026-10-09.csv` and `data/cohort-2026-10-09.csv`: configuration and inherited-cohort exports.
- `data/evidence-guide.md`: selection, missing-value, source-edition, and mechanism-evidence conventions.
- `data/snapshots/2026-10-09/`: frozen catalogue and a manifest pairing its hashes with the revised PDF and evidence files.

Methods are assigned by the manuscript's **visual owner**, not solely by whether any component uses GANs, diffusion, autoregression, or rendering. Supporting foundations, datasets, evaluation work, surveys, and related methods are counted separately. Verified baselines may also appear in route browsing through `crossListings`, while charts count each source paper once under its primary category. The strict AR route requires temporal visual-state dependence; regional outputs and model variants are labelled explicitly. Years follow the cited bibliography edition and may differ from the earliest preprint. Counts describe the curated collection and are not an exhaustive census or a speed leaderboard.

The supplied Feishu literature document returned HTTP 404 during preparation. The local CSV and two AR collections were reviewed against original papers. The catalogue now contains **164 unique papers, all with source previews**; AR browsing shows **five primary-route papers plus three cross-listed baselines**. The second pass added DualLip, the MMVID and ParaLip source papers, and spatial-AR context for Taming Transformer. FluentAvatar remains available as related context because its strict temporal dependence is unresolved. The review notes explain the evidence and survey implications. Source paper previews are reproduced for scholarly reference and remain attributable to their respective authors. The supplied missing-image package filled all 92 remaining preview gaps after checksum, original-source, and visual checks. A visibly labelled text cover remains the fallback if an image cannot load. Manrope is distributed under its included SIL Open Font License.

## Update the catalogue

Add or revise a record in `data/papers.json`, keeping its citation key unique. Required fields are checked by `scripts/validate.py`. Provide an original paper URL, a faithful one- or two-sentence summary, the primary category, bibliography year, mechanism tags, and BibTeX. Every record should identify its manuscript/bibliography or supplied-literature source. Mark supplemental records explicitly and verify their classification against the original paper.

To expose a separately verified baseline from an existing paper, add a `crossListings` entry with `route`, `label`, `summary`, and an HTTPS `evidenceUrl`; optional `shortTitle` and `tags` identify the baseline in its route view and search. Reuse the same record and BibTeX. `countRoutes` supplies exclusive chart totals; `countBrowseRoutes` includes cross-listings for navigation. General-video AR foundations use the `AR foundations` tag. Spatial and unresolved AR cases use category `context` and the `AR scope context` tag, without a strict-AR cross-listing.

For a preview, add an optimized image under `assets/papers/` and an entry keyed by the paper's citation ID in `assets/papers/manifest.json`. Include the original source URL, caption, and figure/page provenance; do not fabricate a paper preview. `heroPath` optionally points to a larger source crop.

Run the tests and build, then commit and push. The Pages workflow publishes only the packaged `dist/` directory; development notes, tests, and design records are excluded.

## Maintain source evidence

The 9 October revision uses documented source collections and a retrospective audit, not an undocumented systematic-search claim. Each checked configuration identifies a primary-source edition, SHA256 hash, page/table/section location, timing boundary, and explicit field status. Do not average values across configurations or treat missing fields as zero. Live Avatar v6's Table 3/Table 10 TTFF discrepancy is retained as a conflict. REA-Listener's unavailable primary paper remains an inherited, unverified cohort record and does not support the new quantitative analyses.

`evidence.js` attaches configurations to catalogue records. Every linked record must list the matching `evidenceIds`; validation checks these links. Pattern filters use documented architecture (A), with qualitative (Q), temporal quantitative (T), component-ablation (B), and hypothesis (H) annotations shown separately. L4-G and L4-C distinguish generated from corrupted ground-truth histories. Hypotheses alone do not create filter matches. The audit is selective: a paper without an evidence disclosure has not thereby been shown to lack measurements.

StyleAvatar is now rendering-primary under the same geometric-reuse rule used for LivePortrait. Exclusive counts are GAN 21, diffusion 43, AR 5, and rendering 54; the primary total stays 123. ART-V links to the cited CVPR proceedings rather than silently mixing its table with arXiv editions. Every card exposes catalogue provenance, including records without a detailed measurement extraction.

Preserve dated snapshots when adding later evidence. Create a new snapshot identifier and record its manifest, then update the display and tests. Use `python3 scripts/build.py --output /tmp/a-new-site-build-directory` to package an isolated preview without changing an earlier build. Search supports Ctrl/Cmd+K; bare character keys are not intercepted.

## Contributions

Open an issue with a source link for missing papers, metadata fixes, or taxonomy questions. Link verification is a point-in-time check; external publishers can change URLs or restrict automated access.
