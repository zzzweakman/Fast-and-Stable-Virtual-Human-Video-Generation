# Missing-paper image review

Reviewed 9 October 2026 from the supplied `Missing_Paper_Images/assets/papers` collection and its `manifest_additions.json` and `image_sources.json` records. The package targets catalogue commit `5c74992553cdcd10c34e7d03d2708a3ef845a725`.

**All 92 supplied images were accepted.** Together with the 72 existing previews, they provide an original-source preview for all **164 catalogue papers**. Paper records, citations, classifications, and statistical paper counts were not changed.

## Validation

- All 92 paper IDs, titles, and article URLs match existing catalogue records. None overlaps an existing preview, and no catalogue paper remains without a preview.
- Every WebP decodes successfully, has one frame, matches the supplied dimensions and SHA-256 checksum, and has a distinct file hash.
- All 92 source downloads returned HTTP 200: 90 original-paper PDFs and two author repository/project images. The 90 PDF first pages contain all normalized title words from their associated catalogue records.
- Each PDF crop was rendered again from its recorded page and rectangle; source-image dimensions were checked directly. Sixty-eight supplied images match the new source pixels exactly. Twenty-four have small rasterization differences, with a maximum mean absolute channel difference of 0.38 on a 0–255 scale. The four largest differences—FID, HeadGaS, Ditto, and OmniTalker—were also inspected side by side. They show the same figures and content.
- All 92 images were visually reviewed for subject, figure composition, readable orientation, and correspondence with the supplied captions. Figure labels were checked against source-page captions, including the two captions with nonstandard PDF text extraction.

File-level source URLs, source-download hashes, supplied-file hashes, published-file hashes, dimensions, and comparison results are recorded in [image-supplement-audit.json](image-supplement-audit.json). Figure/page/crop provenance and English alternative text are recorded in `assets/papers/manifest.json`.

## Integration and size

Web copies preserve each figure's composition and aspect ratio, with a maximum dimension of 1200 pixels and no upscaling. They are encoded as WebP at quality 89. The 92-image payload falls from **46,605,476 bytes to 7,352,140 bytes**, a reduction of **84.22%**; the largest added image is 225,918 bytes. Existing lazy loading and pagination limit what a visitor downloads while browsing.

The source filename `peng2025synctalk++.webp` contains characters outside the website's accepted image-path format. Its new web copy is named `peng2025synctalk-plus-plus.webp`; the paper ID and source filename remain recorded exactly. All other source filenames are retained. No supplied file or existing website preview was overwritten.

Captions were translated into English to match the website. Method diagrams, dataset overviews, evaluation plots, and result comparisons are identified by their actual contents. Performance charts are described as results reported by their source papers, without deriving a cross-paper ranking.

## Attribution and edition notes

Original-author/publisher attribution is preserved for every image. Instant-NGP's figure includes a photograph credited to Trevor Dobson under CC BY-NC-ND 2.0; that credit remains in the manifest. The digital-human survey's Figure 1 credits its background to Google Gemini; the caption and provenance preserve that disclosure. These are reproductions of supplied published figures, not newly generated covers.

RAD-NeRF's image comes from the author's arXiv preprint while the catalogue retains its 2025 IJCV citation. OmniTalker's figure comes from its linked arXiv edition while its manuscript publication metadata is retained. These edition differences do not create additional paper records.

## Website checks

The catalogue tests and static build passed. A browser loaded all 164 catalogue images, including every new preview, with no text-cover fallbacks or JavaScript errors. The image count, unchanged AR counts, search, SyncTalk++ filename, citation panel, and export of 164 unique citations were checked. An intentionally failed image request correctly produced the labelled text-cover fallback while preserving the article link.

Desktop and mobile visual review confirmed that the supplied figures fit the existing cards. Grid and list layouts at 390 and 320 pixels had no horizontal overflow. Automated WCAG A/AA checks reported no violations in the tested desktop and mobile views. The existing design, filtering behavior, and paper catalogue are preserved.
