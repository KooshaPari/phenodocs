---
title: 01 — First-time setup
---

# 01 — First-time setup

Get the PhenoDocs dev environment running in under five minutes.

## Prerequisites

| Tool | Version | Why |
| --- | --- | --- |
| `bun` | `1.3.x` | Package manager + VitePress runtime |
| `uv` | `0.5.x+` | Python toolchain for the scripts |
| `git` | `2.40+` | Submodule support |

Install instructions live in [`/guide/getting-started`](/guide/getting-started).

## Steps

### 1. Clone

```bash
git clone https://github.com/KooshaPari/phenodocs.git
cd phenodocs
```

### 2. Install JS deps

```bash
bun install --frozen-lockfile
```

### 3. Install Python deps

```bash
uv sync --group dev
```

### 4. Start the dev server

```bash
bun run dev
```

VitePress prints the local URL (default `http://localhost:5173`).

## Verify

- [ ] The hub index loads at the URL above.
- [ ] The sidebar lists **Guide**, **Architecture**, **API**, **Governance**, **Tutorials**, **RFCs**, **Changelog**.
- [ ] The "Edit this page on GitHub" link resolves to a real file.

## Next

Continue to [02 — Adding a project to the hub](./02-adding-a-project).
