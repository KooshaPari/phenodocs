# packages/landing/ — DEFERRED ABSORPTION STUB

**Status:** Forward-pointer only. **No code copied.** This directory exists to
record the 2026-07-17 absorption decision for `KooshaPari/phenotype-landing`.

## Why this directory is empty (intentionally)

The original absorption plan was to copy the entire `phenotype-landing` repo
into this directory as a single workspace package. That plan was rejected on
2026-07-17 for the following concrete reasons:

### Source is not a single landing page

`phenotype-landing` is a **7-site Astro multi-tenant factory**, not one site:

| Site | Stack | On-disk size |
|------|-------|--------------|
| `sites/agileplus-landing` | Astro + Bun | ~201 MB |
| `sites/byteport-landing` | Astro + Bun | ~197 MB |
| `sites/hwledger-landing` | Astro + Bun | ~196 MB |
| `sites/phenokits-landing` | Astro + Bun | ~196 MB |
| `sites/projects-landing` | Astro + Bun | ~196 MB |
| `sites/thegent-landing` | Astro + Bun | ~196 MB |
| `sites/odin-landing` | Static HTML | ~184 MB |

Each site has its own `package.json` + `bun.lock` + `vercel.json` +
`.github/workflows/ci.yml`. The root has **no** `package.json` — coordination
is via `Taskfile.yml` only.

### phenodocs's bun workspace can't ingest it

phenodocs has `workspaces: ["packages/*"]` which expects each child to be a
single package. A 7-site factory with no root `package.json` is not a single
package. Adding `packages/landing/sites/*` to the workspace glob would split
the factory across 7 unrelated workspace entries, each with conflicting
`astro`/`vite`/etc. pins.

### Each site deploys independently

`vercel.json` per site + CI workflow per site = 7 independent deploy targets.
phenodocs's VitePress build has no concept of marketing-site deploys.

### Build is heavy

Tracked source is ~1.5 MB, but on-disk footprint is ~1.6 GB (mostly
`node_modules`). `cp -r` + `bun install` would bloat the repo and conflict
with phenodocs's existing `bun.lock`.

## What was done instead (failsafe path)

Per the task failsafe clause ("ARCHIVE_ONLY + boundary doc if build is heavy
or conflicts exist"):

1. **`phenotype-registry` row updated** — `repo-phenotype-landing` →
   `disposition=ARCHIVE_ONLY`, `fsm=absorbed`, `archived_at=2026-07-17T15:50:00Z`,
   target=this forward-pointer.
2. **`catalog/registry.yaml` row updated** — `phenotype-landing` →
   `status=archived`, `boundary=docs/boundary/phenotype-landing.md`,
   `intent=docs/intent/phenotype-landing.md`.
3. **Boundary + intent docs filled** in the registry repo.
4. **Audit artifact created** — `audits/absorption-justifications/phenotype-landing-deferred-2026-07-17.md`.
5. **Per-project metadata created** — `projects/phenotype-landing.json`.
6. **Source repo archived on GitHub** — `gh repo archive KooshaPari/phenotype-landing --yes`.

This forward-pointer (this `README.md`) is the **only artifact** in
`phenodocs/packages/landing/`. No `package.json`, no source code, no
configuration.

## Future absorption (preconditions)

If a future absorption is desired, one of these preconditions must be met:

1. **Each site is migrated to VitePress or static HTML** — then `phenodocs`
   can ingest each site as a documentation surface (`docs/agileplus/`,
   `docs/byteport/`, etc.) via the existing federation pattern.
2. **A new dedicated `phenotype-sites` monorepo is created** with its own
   Astro workspace + VitePress doc hybrid. Not currently planned.
3. **The sites are decomposed** so each landing site is a stand-alone Bun
   workspace package at `phenodocs/packages/landing-{name}/`. This requires
   per-site absorb PRs × 7 (or a batched subtree split).

Until then, the source repo remains archived at
`KooshaPari/phenotype-landing` and this forward-pointer stands.

## Cross-references

- `phenotype-registry/registry/disposition-index.json` — row `repo-phenotype-landing`
- `phenotype-registry/catalog/registry.yaml` — row `phenotype-landing` (status: archived)
- `phenotype-registry/projects/phenotype-landing.json` — per-project metadata
- `phenotype-registry/docs/boundary/phenotype-landing.md` — boundary doc
- `phenotype-registry/docs/intent/phenotype-landing.md` — intent doc
- `phenotype-registry/audits/absorption-justifications/phenotype-landing-deferred-2026-07-17.md` — audit
- Parallel precedent: `omniroute-rust` and `PhenoVCS` (both ARCHIVE_ONLY 2026-07-17)