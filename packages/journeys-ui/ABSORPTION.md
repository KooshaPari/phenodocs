# Absorption marker — @phenotype/journeys-ui

- **Source:** `KooshaPari/phenotype-journeys` @ `60352ae` (HEAD, 2026-07-16) —
  Vue 3 component library (`npm/journey-viewer/`) previously published as
  `@phenotype/journey-viewer` at version `0.1.3`.
- **Absorbed at:** 2026-07-17 into `KooshaPari/phenodocs` under
  `packages/journeys-ui/`.
- **Renamed:** `@phenotype/journey-viewer` → `@phenotype/journeys-ui` so the
  package name mirrors the directory (matches the existing
  `@phenotype/docs`, `@phenotype/design-tokens`, etc. convention in this
  monorepo). All Vue exports are backward-compatible — every named component
  (`JourneyViewer`, `RecordingEmbed`, `KeyframeLightbox`, `KeyframeGallery`,
  `JourneyStep`, `JudgeScore`, `Shot`, `ShotGallery`, `StructuralPane`) plus
  all type exports remain unchanged.
- **Dropped from copy:** the four `phenotype-journey-viewer-0.1.*.tgz` tarballs
  and `bun.lock` from the source `npm/journey-viewer/` directory were
  intentionally excluded — only the runtime source (`src/*.vue`, `src/*.ts`,
  `CHANGELOG.md`) was lifted. The `public/` static asset directory
  (`apple-touch-icon.png`, `favicon.ico`, `logo.svg`) is also excluded; if
  any of those assets are needed, replicate under `packages/journeys-ui/public/`
  at the consuming VitePress site.
- **Phenotype-eng exclusions:** the sibling `@phenotype/journey-playwright`
  and `@phenotype/playwright-record` packages in the source repo's `npm/`
  tree are NOT absorbed here — those are separate Playwright fixtures and
  belong in their own substrate (alongside any future
  `@phenotype/playwright-record` consumer project). They are out of scope
  for the journeys-ui viewer.
- **Workspace registration:** picked up automatically by
  `phenodocs/package.json`'s `"workspaces": ["packages/*"]` glob. No root
  `package.json` change needed.
- **Peer deps:** unchanged — `vue ^3.4.0` + `vitepress ^1.0.0`. phenodocs
  already pins `vue ^3.5.0` and `vitepress ^1.5.0`, so the peer range is
  satisfied transitively.
- **Companion Rust half:** the verify-loop + schema lib absorbed into
  `phenotype-tooling/crates/journeys-cli/` (see its ABSORPTION.md). The
  journey manifest schema is byte-compatible across both halves
  (schemars 1.2 + JSON Schema Draft 2020-12).
- **Registry row:** `repo-phenotype-journeys` flipped from
  `disposition=AFFIRM/fsm=active` to `disposition=ABSORB/fsm=absorbed/
  target="phenotype-tooling (crates/journeys-cli/) + phenodocs
  (packages/journeys-ui/)"`. Source repo archived via
  `gh repo archive KooshaPari/phenotype-journeys -y`.

Restoration command:

```bash
gh repo clone KooshaPari/phenotype-journeys /tmp/phenotype-journeys-restore
```
