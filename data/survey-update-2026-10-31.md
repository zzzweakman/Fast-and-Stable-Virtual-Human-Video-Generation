# Survey update — 31 October 2026

The website now follows `1031_integrated_revision` v4: 46 pages, 293 cited references, and 304 unique bibliography entries. Earlier releases remain unchanged.

## Figures and scope

The full tree contains 136 methods: 21 GAN, 52 rendering, 58 diffusion, and five visual-AR methods. Original institution icons and solid/dashed branches are preserved. Solid branches indicate claimed real-time performance; dashed branches indicate that real-time capability was not reported. These inherited annotations do not constitute a new timing audit.

The mechanism diagram shows representative examples for 14 selected groups. GAN and rendering each have four groups; diffusion and visual AR each have three, aligned in the lower row. Dense conditioned video remains historical background in the text. EMO and MultiTalk support continuation; output duration alone does not establish real-time performance or stable long-session deployment.

## Catalogue and citations

The catalogue has 220 unique records: 24 GAN, 75 diffusion, 69 rendering, six visual AR, and 46 supporting references. The broader catalogue includes older methods and related work beyond the timeline. Its six visual-AR entries include the older regional DualLip baseline alongside the five timeline entries.

This revision adds 34 records to the website and covers all 136 timeline methods. Existing previews are preserved. New records without a source crop use the site's explicitly labelled text covers. Citation keys, titles, authors, years and BibTeX follow the current manuscript where covered; older editions and source-specific measurement records retain their stated scope.

DINet, EDTalk, EAT, RAM-Avatar, FixTalk and the newly added IP-LAP follow rendering because source appearance is transported or represented spatially. FixTalk's assignment is a paper-based inference from its inherited generator. UniTalker's speech/landmark autoregression conditions EchoMimic; diffusion owns RGB. OmniResponse remains supporting context because its RGB backend is insufficiently specified. AvatarSync and FluentAvatar are one work, retained in visual AR with unresolved cross-keyframe causality and streaming execution stated explicitly. GANimate is not presented as a real-time demonstration.

The method–citation CSV preserves review depth and primary-source links. Reviews range from metadata and abstract checks to selected full-text or code inspection; this release does not claim a fresh full-paper audit of every reference. The downloadable survey bibliography contains 304 entries; catalogue exports contain the selected catalogue records.

## Measurements

All measured values and 306 runtime calls are unchanged. Current runtime grouping is 8 GAN, 16 diffusion, 26 rendering, and one UniLS motion-visualization configuration. The HDTF table has 4 GAN, 12 diffusion and 7 rendering configurations. StreamEval retains the same six configurations, four content metrics and local-Qwen limitations. No new experiments were run for this website update.
