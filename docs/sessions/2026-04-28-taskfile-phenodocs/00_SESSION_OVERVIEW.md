# Session Overview

## Goal

Add a repo-local `Taskfile.yml` that exposes common `build`, `test`, `lint`, and `clean` tasks.

## Success Criteria

- Tasks dispatch correctly for the repo's actual stack.
- Bun/VitePress commands are wired from `package.json`.
- Python helper commands are wired from `pyproject.toml` / `scripts/`.
- The change is committed, pushed, opened as a PR, and merged.

## Scope

- `Taskfile.yml`
- Minimal session notes in `docs/sessions/`

## Implementation Note

- Split `clean` into `clean:site` and `clean:python` so cleanup follows the same repo-manifest detection pattern as the build, test, and lint task groups.
