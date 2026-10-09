# Fast and Stable Virtual Human Video Generation: A Survey

A visual research companion for the survey: searchable papers, original figure previews, concise summaries, bibliography downloads, and statistics derived from the catalogue.

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
- `assets/papers/manifest.json`: preview provenance, source pages, figure captions, and image paths.
- `assets/survey/survey.pdf`: the supplied October 2026 revised draft (`main_revised.pdf`), which matches the current source abstract.
- `assets/survey/provenance.json`: source information for the survey PDF and diagrams.

Methods are assigned by the manuscript's **visual owner**, not solely by whether any component uses GANs, diffusion, autoregression, or rendering. Supporting foundations, datasets, evaluation work, and surveys are counted separately. Years follow the cited bibliography edition and may differ from the earliest preprint. Counts describe the curated collection and are not an exhaustive census or a speed leaderboard.

The supplied Feishu literature document returned HTTP 404 during preparation. This release uses the local survey and its bibliography; it does not claim to include Feishu-only entries. Source paper previews are reproduced for scholarly reference and remain attributable to their respective authors. Records without a source preview use visibly labelled text covers. Manrope is distributed under its included SIL Open Font License.

## Update the catalogue

Add or revise a record in `data/papers.json`, keeping its citation key unique. Required fields are checked by `scripts/validate.py`. Provide an original paper URL, a faithful one- or two-sentence summary, the primary category, bibliography year, mechanism tags, and BibTeX. Every record should identify its manuscript/bibliography source.

For a preview, add an optimized image under `assets/papers/` and an entry keyed by the paper's citation ID in `assets/papers/manifest.json`. Include the original source URL, caption, and figure/page provenance; do not fabricate a paper preview. `heroPath` optionally points to a larger source crop.

Run the tests and build, then commit and push. The Pages workflow publishes only the packaged `dist/` directory; development notes, tests, and design records are excluded.

## Contributions

Open an issue with a source link for missing papers, metadata fixes, or taxonomy questions. Link verification is a point-in-time check; external publishers can change URLs or restrict automated access.
