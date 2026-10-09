---
name: Fast and Stable
description: Visual research catalogue for virtual-human video generation
colors:
  forest: "#193e35"
  lime: "#e0edb8"
  background: "#fcfdfa"
  surface: "#fff"
  ink: "#1b302a"
  muted: "#62716a"
  line: "#dfe6df"
  mineral: "#eff3ed"
  gan: "#956333"
  diffusion: "#536dc6"
  autoregressive: "#92558b"
  rendering: "#27786e"
  supporting: "#68736c"
typography:
  display:
    fontFamily: "Manrope, Arial, sans-serif"
    fontSize: "clamp(42px, 4.55vw, 67px)"
    fontWeight: 800
    lineHeight: 1.09
    letterSpacing: "-0.04em"
  headline:
    fontFamily: "Manrope, Arial, sans-serif"
    fontSize: "32px"
    fontWeight: 750
    lineHeight: 1.2
    letterSpacing: "-0.035em"
  title:
    fontFamily: "Manrope, Arial, sans-serif"
    fontSize: "18px"
    fontWeight: 800
    lineHeight: 1.3
    letterSpacing: "-0.025em"
  body:
    fontFamily: "Manrope, Arial, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.6
  summary:
    fontFamily: "Manrope, Arial, sans-serif"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.75
rounded:
  tag: "3px"
  mechanism: "4px"
  control: "6px"
  button: "7px"
  input: "8px"
  card: "12px"
  gallery: "14px"
spacing:
  compact: "8px"
  small: "12px"
  medium: "16px"
  card: "17px"
  large: "24px"
components:
  button-primary:
    backgroundColor: "{colors.forest}"
    textColor: "{colors.surface}"
    rounded: "{rounded.button}"
    padding: "11px 18px"
  button-outline:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.button}"
    padding: "11px 18px"
  search:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.input}"
    padding: "0 16px"
  mechanism:
    backgroundColor: "#f0f3ed"
    textColor: "#5f7058"
    rounded: "{rounded.mechanism}"
    padding: "5px 9px"
  mechanism-active:
    backgroundColor: "{colors.forest}"
    textColor: "{colors.surface}"
    rounded: "{rounded.mechanism}"
    padding: "5px 9px"
  paper-card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.card}"
---

# Design System: Fast and Stable

## Overview

**Creative North Star: "The Visual Research Index"**

A spacious research index pairs open Manrope typography with real paper imagery. Forest headings and controls establish the reading hierarchy; mineral panels separate supporting material, and restrained lime marks the invitation to read the survey. This descriptive name records the implemented world.

**Key Characteristics:**
- Clear reading surfaces with thin borders and restrained rounding.
- Source figures or explicitly labelled text covers.
- Categorical colors connecting navigation, papers, and charts.
- Dense literature browsing beneath a spacious introduction.

## Colors

### Primary

Forest carries the identity, principal actions, heading emphasis, and selected mechanisms. Lime supplies the survey callout and text selection.

### Secondary

The categorical palette is semantic: warm brown for GAN, blue for diffusion, plum for autoregressive generation, and teal for rendering. Supporting references use muted green-gray. Preserve these mappings across route markers, paper metadata, filters, bars, and legends.

### Neutral

Background is the cool near-white page; surface is the white reading sheet; mineral separates the gallery and landscape band. Ink supplies primary text, muted supplies secondary text, and line separates controls and sections. Smaller metadata follows the contrast adjustments at the end of the stylesheet.

**The Route Continuity Rule.** A route retains its color across every representation and is also identified by text.

## Typography

Locally served variable Manrope spans weights 200–800, with Arial and sans-serif fallbacks. Heavy, tightly spaced headings contrast with open body copy. Frontmatter records default desktop roles; responsive overrides in styles.css remain authoritative.

Section headlines step down to 28px and 26px. Paper titles range from 16px on denser grids to 20px in the narrow single-column view. Full paper titles use 12px, authors 11px, and category/year/tag metadata 10px. Perspective and expanded stability copy uses 14px.

**The Reading Floor Rule.** Paper summaries use 13px with 1.75 line height; mobile cards use 14px while compact list summaries remain 13px. Apply the final overrides, not the superseded smaller declarations.

## Layout

The main container is capped at 1344px, with 48px side margins on wide screens, 32px below 1190px, and 20px below 720px. The desktop hero pairs a wider text column with a figure gallery. The catalogue uses a 190px filter rail and a three-column grid; the rail narrows to 166px at 1190px. Cards switch to two columns at 960px and one at 430px.

Below 720px, filters wrap above results, the hero and supporting panels stack, and sticky navigation uses two rows. Anchor offsets account for the header. List view uses a 174px image column that shrinks to 100px on mobile. Principal mobile filter, citation, view, gallery, and chart-row controls have a 44px target floor.

## Elevation & Depth

Thin borders and tonal surfaces establish depth. Cards remain flat and change border color on hover. Only the transient notification uses a diffuse shadow (0 8px 28px #193e3526).

Image changes use a 350ms opacity reveal; most control transitions take 180–200ms. Reduced-motion preferences disable animations, transitions, and smooth scrolling. The gallery advances through explicit controls.

## Shapes

Small tags and controls use compact rounding; reading cards and lens panels use the card radius; the figure gallery is slightly softer. Category dots and square swatches identify routes. Icons are inline SVG with rounded line caps and joins. Figures are contained on white; page previews use a cropped page view.

## Components

- **Buttons:** forest primary and outlined secondary actions use compact, bold labels. Primary hover lightens the forest; secondary hover gains a mineral fill. Interactive elements receive a 3px olive focus outline with a 4px offset.
- **Search and selectors:** white bordered fields. Search receives a forest border and pale 2px outline when focused. The desktop slash-key hint corresponds to the implemented shortcut.
- **Navigation:** muted links turn forest on hover; the active section receives a thin underline. Scroll tracking updates the active state and aria-current.
- **Filters and chips:** selected routes use a pale green surface; selected mechanisms use forest and white. Active-filter chips include an SVG remove control. Mobile filters wrap.
- **Paper cards:** source preview or labelled text cover, route/year, title, citation metadata, summary, and up to three tags. The ruled footer holds source and citation actions; citations expand inside the card. Failed images use the text cover.
- **Feedback and statistics:** live result counts accompany filters; empty and error states offer recovery actions. Chart bars filter the catalogue and repeat category text, colors, and a legend.
- **Stability disclosures:** native details/summary rows use thin rules. An SVG plus rotates when open; expanded text retains the reading floor.

## Do's and Don'ts

### Do:
- **Do** preserve route-to-color mappings and visible category names.
- **Do** apply the final reading and mobile interaction floors.
- **Do** use real source imagery or the labelled text-cover fallback.
- **Do** retain focus visibility and reduced-motion behavior.

### Don't:
- **Don't** substitute color alone for category labels or chart legends.
- **Don't** promote superseded small text declarations into new components.
- **Don't** add card shadows where the shipped system uses borders and tonal surfaces.
