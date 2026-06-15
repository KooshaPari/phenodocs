# OpenAPI Reference

This section hosts the **auto-generated** API reference. The pages here are
emitted by `scripts/generate_api_reference.py` (run with `uv run python
scripts/generate_api_reference.py --spec <spec.yaml> --out docs/.generated/api`)
and must not be edited by hand — re-run the generator after any spec change.

## How generation works

```bash
uv run python scripts/generate_api_reference.py \
    --spec docs/api/openapi/phenodocs.yaml \
    --out   docs/.generated/api
```

The script:

1. Loads the OpenAPI 3.x spec (YAML or JSON).
2. Walks `paths` grouped by tag, rendering one Markdown file per spec.
3. Walks `components.schemas` and emits a `components.md` per spec.
4. Writes everything under `docs/.generated/api/<spec-stem>/`.

The output directory is git-ignored by `.gitignore` (line: `.generated/`),
but the index page you are reading is **committed** so the route is stable.

## Available references

| Spec | Source | Status |
| --- | --- | --- |
| [phenodocs](./phenodocs/) | `docs/api/openapi/phenodocs.yaml` | generated |

To add a new reference, drop an OpenAPI spec under `docs/api/openapi/` (or
`packages/<x>/api/openapi.yaml`) and extend the
`generate_api_reference` step in the build workflow (see
`.github/workflows/api-reference.yml`).

## Conventions

- Path parameters use `{name}` and are described in the parameters table.
- OneOf / AnyOf / AllOf are rendered as nested headings.
- `$ref` is resolved recursively up to depth 4 to avoid loops.
- Deprecated operations carry a `> **DEPRECATED**` banner.
