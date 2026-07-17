# `@phenotype/journeys-ui`

Vue 3 component library for rendering Phenotype journey manifests in
VitePress docs. Formerly `@phenotype/journey-viewer` (v0.1.3); absorbed
2026-07-17 from `KooshaPari/phenotype-journeys`.

## Components

- `<JourneyViewer>` — top-level manifest render (steps, screenshots, judge
  score, agreement chip).
- `<RecordingEmbed>` — embed a recorded video/gif with caption.
- `<KeyframeLightbox>` — full-screen keyframe with annotation overlay.
- `<KeyframeGallery>` — scrollable thumbnail strip of keyframes.
- `<JourneyStep>` — single step render (intent + screenshot + assertions).
- `<JudgeScore>` — coloured confidence pill.
- `<Shot>` / `<ShotGallery>` — discrete sub-step shots inside a journey.
- `<StructuralPane>` — three-column structural layout (shot list + lightbox +
  description) used by `JourneyViewer` for wide viewports.

## Usage

```ts
// Anywhere in the VitePress docs:
import { JourneyViewer } from "@phenotype/journeys-ui";
```

```vue
<JourneyViewer :manifest="manifest" />
```

The package picks up the `vue` (≥3.4.0) and `vitepress` (≥1.0.0) peer
dependencies from the `phenodocs` workspace root.

## Provenance

See `ABSORPTION.md` for the source commit, rename rationale, and the list
of sibling npm packages (`@phenotype/journey-playwright`,
`@phenotype/playwright-record`) deliberately excluded from this copy.
