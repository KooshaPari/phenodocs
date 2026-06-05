# phenodocs-bootstrap

- **Journey id:** `phenodocs-bootstrap`
- **Repo:** phenodocs
- **Flow:** new contributor clones phenodocs, runs the dev server, sees the
  landing page render with the journey-traceability standard linked from the
  sidebar.
- **Owner:** phenodocs maintainers
- **Related:** [Journey Traceability Standard](../operations/journey-traceability.md),
  [Journey Governance](../governance/journeys.md)
- **Capture date:** 2026-06-05
- **Environment:** macOS 25.6.0, bun 1.x, Node 22.x, Chromium stable

## User Story

> As a new contributor to phenodocs, I can clone the repo, run `bun install`
> followed by `bun run dev`, and within two minutes I see the docs site render
> with the journey-traceability standard linked from the sidebar. No console
> errors, no broken navigation links.

## Acceptance Criteria

- `bun run dev` returns HTTP 200 within 60 s of the first request.
- The sidebar lists the "Journey Traceability" page.
- The page renders the canonical `<ShotGallery>` + `<RecordingEmbed>` stub.
- The manifest at `docs/journeys/manifests/phenodocs-bootstrap.journey.yaml`
  passes `phenotype-journey verify` (assertions below).

## Keyframe + Recording Stub

<!--
STUB: rich journey embed pending.
Real evidence lives under docs/journeys/cli-journeys/{keyframes,recordings}/phenodocs-bootstrap/.
Replace this block with:

  <ShotGallery
    title="phenodocs-bootstrap: clone, install, dev, see standard"
    :shots='[
      {"src":"/docs/journeys/cli-journeys/keyframes/phenodocs-bootstrap/frame-001.png","caption":"terminal: bun install + bun run dev"},
      {"src":"/docs/journeys/cli-journeys/keyframes/phenodocs-bootstrap/frame-002.png","caption":"browser: docs landing renders without console errors"},
      {"src":"/docs/journeys/cli-journeys/keyframes/phenodocs-bootstrap/frame-003.png","caption":"browser: Journey Traceability page renders ShotGallery + RecordingEmbed stub"}
    ]' />

  <RecordingEmbed tape="phenodocs-bootstrap" kind="cli" caption="End-to-end bootstrap from clone to rendered journey page" />
-->

## Manifest

The companion manifest lives at
[`docs/journeys/manifests/phenodocs-bootstrap.journey.yaml`](./manifests/phenodocs-bootstrap.journey.yaml).

```yaml
id: phenodocs-bootstrap
intent: Clone phenodocs, install, run dev server, see journey-traceability page render
keyframe_count: 3
passed: false
recording: cli-journeys/recordings/phenodocs-bootstrap.gif
recording_gif: cli-journeys/recordings/phenodocs-bootstrap.gif
steps:
  - index: 1
    slug: dev-server-up
    assertions:
      must_contain:
        - "Local:"
        - "ready in"
      must_not_contain:
        - "error:"
      ocr_required: true
  - index: 2
    slug: landing-renders
    assertions:
      must_contain:
        - "phenodocs"
      must_not_contain:
        - "404"
        - "error:"
      ocr_required: true
  - index: 3
    slug: journey-page
    assertions:
      must_contain:
        - "Journey Traceability"
      must_not_contain:
        - "error:"
      expected_exit: 0
      ocr_required: true
```

## Traceability

| Layer | Artifact |
|-------|----------|
| Spec | `FUNCTIONAL_REQUIREMENTS.md` § "New contributor onboarding" |
| Code | `apps/*` (docs site), `kitty-specs/` |
| Test | `bun test` (TDD); gherkin under `kitty-specs/` (BDD); `phenotype-journey verify` (XDD) |
| Doc | this page |
| Journey manifest | `docs/journeys/manifests/phenodocs-bootstrap.journey.yaml` |
| Eval / Gate | CI: `phenotype-journey verify` must pass before merge |
