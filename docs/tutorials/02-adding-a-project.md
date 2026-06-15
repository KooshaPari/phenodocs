---
title: 02 — Adding a project to the hub
---

# 02 — Adding a project to the hub

Federate a new project into the hub. The hub expects a `docs/` tree that
follows the Phenotype doc taxonomy (see
[`/guide/architecture`](/guide/architecture#layer-system)).

## Steps

### 1. Add the project as a submodule

```bash
git submodule add https://github.com/<org>/<project>.git projects/<project>
git submodule update --init --recursive
```

### 2. Register the project in the federation map

Edit `scripts/federation.py` (or whichever aggregator is current in your
checkout) and add the project to the `PROJECTS` dict:

```python
PROJECTS["<project>"] = {
    "source": "projects/<project>/docs",
    "mount":  "/<project>/",
}
```

### 3. Rebuild the sidebar

```bash
bun run build
```

### 4. Verify

- [ ] The project's section appears in the sidebar.
- [ ] Local search finds at least one page from the new project.

## When the project has no `docs/` yet

Stub it:

```bash
mkdir -p projects/<project>/docs
cat > projects/<project>/docs/index.md <<'MD'
# <Project>

Placeholder. Replace with the real landing page.
MD
git -C projects/<project> add .
git -C projects/<project> commit -m "docs: bootstrap"
```

## Next

Continue to [03 — Generating the API reference](./03-generating-api-reference).
