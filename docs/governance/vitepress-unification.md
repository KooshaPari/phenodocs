# VitePress Unification

PhenoDocs is the **single unified VitePress site** for the Phenotype documentation
ecosystem. This page records the unification decision and how content is
routed across the monorepo.

## TL;DR

| Source | Mount point in phenodocs site | Build status |
| --- | --- | --- |
| `docs/` (phenodocs hub) | `/`, `/guide/`, `/governance/`, `/reference/`, `/api/`, `/tutorials/`, `/rfcs/`, `/changelog/`, `/views/`, `/roadmap/` | Active |
| `packages/design/docs/` | `/design/` (federated link) | Standalone, deprecated as primary surface |
| `packages/shared-utils/docs/` | `/shared-utils/` (federated link) | Standalone, deprecated as primary surface |
| `docs/.vitepress/config.ts` | (legacy inner config) | Removed from build path |

The VitePress build entry point is `.vitepress/config.mts` at the repo root
(see `package.json::scripts.build → vitepress build`).

## Why unify

1. **One search index.** A single VitePress site produces a single
   `localSearch` index, so cross-package queries just work.
2. **One deployment.** `deploy.yml` ships `.vitepress/dist/` to GitHub Pages
   from `main`; we don't fan out per package.
3. **One theme.** The `@phenotype/docs` shared theme (keycap palette) is the
   only theme under active development; package-level themes drift.
4. **One router.** Internal links never break because the route table is
   owned by phenodocs, not by N independent sites.

## Federation pattern

The phenodocs site mounts content from other sources as **virtual sections**:

```text
phenodocs/
├── .vitepress/config.mts        # root VitePress entry
├── docs/                         # hub-owned content
│   ├── guide/                   # /guide/...
│   ├── reference/               # /reference/...
│   ├── api/                     # /api/...
│   ├── tutorials/               # /tutorials/... (new)
│   ├── rfcs/                    # /rfcs/... (new)
│   ├── changelog/               # /changelog/... (new)
│   ├── governance/
│   ├── views/
│   ├── roadmap/
│   └── templates/
├── packages/                    # federated sources (build disabled)
│   ├── design/docs/             # see /design/ via cross-link
│   └── shared-utils/docs/       # see /shared-utils/ via cross-link
└── scripts/
    ├── generate_api_reference.py  # OpenAPI → Markdown
    └── changelog_automation.py    # CHANGELOG.md section builder
```

The `scripts/` directory is the orchestration layer; VitePress just renders
the generated Markdown.

## Migration from package-level sites

| Old URL | New URL | Owner |
| --- | --- | --- |
| `/guide/getting-started` (phenodocs) | unchanged | docs lead |
| `/guide/architecture` (phenodocs) | unchanged | docs lead |
| `/api/` (phenodocs) | unchanged + `/api/openapi/` (generated) | docs lead |
| `/governance/overview` (phenodocs) | unchanged | docs lead |
| `/roadmap/` (phenodocs) | unchanged | docs lead |
| `/views/` (phenodocs) | unchanged | docs lead |
| `packages/design/docs/guide/...` | `/design/` (cross-link stub) | design lead |
| `packages/shared-utils/docs/...` | `/shared-utils/` (cross-link stub) | utils lead |

Cross-link stubs render a brief description and an "open in package" link,
deferring to the package's own deploy (or a future copy-into-hub step).

## Adding a new section to the unified site

1. Create a directory under `docs/<section>/`.
2. Add at least one `index.md`.
3. Edit `.vitepress/config.mts`:
   - Add `{ text: '<Section>', link: '/<section>/' }` to the top-level `nav`.
   - Add a `sidebar['/<section>/']` block (auto-generator in
     `packages/docs/src/utils/sidebar-generator.ts` produces a default).
4. Add the section title to the federation table above.
5. Run `bun run check` to verify links and lint.

## Why we keep `packages/docs/`

`packages/docs/` is the shared VitePress config + theme package. It is **not**
a documentation site — it ships `createPhenotypeConfig`, the keycap theme, and
sidebar generators. Consumers import it via `@phenotype/docs/config` and
`@phenotype/docs/theme`. Removing it would break every dependent repo.

## Acceptance criteria

- `bun run build` produces a single `.vitepress/dist/`.
- `.vitepress/config.mts` is the only VitePress entry in CI (see
  `quality-gate.yml`).
- The link checker (`scripts/check_docs_links.py`) sees every page.
- The generated API reference appears under `/api/openapi/`.
- The changelog automation workflow runs on every release tag.
