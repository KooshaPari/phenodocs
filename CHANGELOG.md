# Changelog

## [Unreleased]

### Added

- **`docs/planning/full-turn-next50-20260326.md`** — **Next 50** batch: five lanes (A–E), ten waves (W1–W10), explicit **Depends** DAG; supersedes Next 24 as default batch size.
- **`docs/guides/full-turn-delivery.md`** — PR merge to `main`/release, `gh`, changelog, version, docs; **batch planning** links Next 50; **`docs/planning/full-turn-next24-20260326.md`** (legacy Next 24).
- **`docs/views/index.md`** / **`docs/views/wbs.md`** — **Shipping** + Next 50 / DAG pointers.
- **`AGENTS.md` / `README.md`** — full-turn expectations.
- **Workspace views** hub: `/views/` — changelog, commit log, WBS entry points.
- **Planning:** `docs/planning/rich-workspace-views.md` — product plan for rich plan/research/spec/work modules, roadmap, changelog, git log, WBS.
- **CommitLog** Vue component and `.vitepress/data/commit-log.json` sample.
- **Roadmap** page expanded with horizons, themes, milestones.
- **VitePress:** `srcDir: 'docs'`; nav links for Roadmap and Workspace views; sidebars for `/roadmap/`, `/planning/`, `/views/`.
- **Data stubs:** `.vitepress/data/audit-log.json`, `kb-graph.json` (fix build).

### Fixed

- **CodeQL:** `languages: actions` (workflow security). JavaScript analysis fails on this VitePress/Vue workspace (“no source code seen”); Actions scanning stays green.
- Build failures from missing theme data JSON imports.
