---
title: 03 — Generating the API reference
---

# 03 — Generating the API reference

Render the OpenAPI specs in `docs/api/openapi/` to Markdown and surface
them under `/api/openapi/`.

## Steps

### 1. Write (or copy) an OpenAPI 3.x spec

Specs live at `docs/api/openapi/<name>.openapi.yaml` (or `.json`).

A minimal example:

```yaml
openapi: 3.0.3
info:
  title: Example
  version: 0.1.0
paths: {}
components:
  schemas:
    Hello:
      type: object
      required: [message]
      properties:
        message: { type: string, description: "Greeting" }
```

### 2. Run the generator

```bash
uv run python scripts/generate_api_reference.py \
    --spec docs/api/openapi/example.openapi.yaml \
    --out   docs/.generated/api
```

### 3. Build the site

```bash
bun run build
```

### 4. Verify

- [ ] `docs/.generated/api/example/index.md` exists.
- [ ] `docs/.generated/api/example/components.md` lists the `Hello` schema.
- [ ] The site renders `/api/openapi/example/` with a stable table of contents.

## CI integration

`.github/workflows/api-reference.yml` runs the generator on every push
to `main` and on any PR that touches `docs/api/openapi/`. Generated
files are committed by the workflow; reviewers should not edit them
manually.

## Next

Continue to [04 — Writing an RFC](./04-writing-an-rfc).
