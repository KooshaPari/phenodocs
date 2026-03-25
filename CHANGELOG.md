# Changelog

## [Unreleased]

### Added

- **`docs/views/index.md`** — **Shipping** row linking to the full-turn delivery guide.
- **`docs/guides/full-turn-delivery.md`** — PR merge to `main`/release, `gh` visibility, changelog, version, docs build; **`docs/planning/full-turn-next24-20260326.md`** — Next 24 execution plan.
- **`AGENTS.md` / `README.md`** — full-turn expectations.
- **Workspace views** hub: `/views/` — changelog, commit log, WBS entry points.
- **Planning:** `docs/planning/rich-workspace-views.md` — product plan for rich plan/research/spec/work modules, roadmap, changelog, git log, WBS.
- **CommitLog** Vue component and `.vitepress/data/commit-log.json` sample.
- **Roadmap** page expanded with horizons, themes, milestones.
- **VitePress:** `srcDir: 'docs'`; nav links for Roadmap and Workspace views; sidebars for `/roadmap/`, `/planning/`, `/views/`.
- **Data stubs:** `.vitepress/data/audit-log.json`, `kb-graph.json` (fix build).

### Fixed

- **CI:** `workflow-permissions` workflow now defines a `jobs` block (GitHub Actions rejects workflows with no jobs); removed stray merge conflict markers from this file.
- **CodeQL:** removed duplicate `setup-node` / `npm ci` steps in the analyze job.
- **Deploy / quality:** Vue theme components and TS unused bindings fixed so `bun run check` passes in the Deploy Docs workflow.
- **VitePress config:** duplicate `srcDir` key removed from `.vitepress/config.mts`.
- **CodeQL (analysis):** `npm ci` installs deps so JS/TS under `.vitepress` is analyzed; autobuild alone did not extract VitePress sources.
- Build failures from missing theme data JSON imports.
