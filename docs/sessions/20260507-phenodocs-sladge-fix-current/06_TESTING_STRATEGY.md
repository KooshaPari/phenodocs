# Testing Strategy

## Targeted Checks

- `git diff --check`
- README/session badge presence search
- `bun run build`
- `bun run check` when local tooling permits

## Expected Limits

This is a docs-governance-only change, so source or workflow failures outside
README/session docs should be recorded rather than folded into this commit.

## Validation Result

- `git diff --check` passed.
- README/session badge presence passed.
- `bun run build` passed with a temporary `node_modules` symlink to the clean
  canonical dependency tree.
- `bun run check` ran oxlint and vue-tsc successfully with the same temporary
  dependency symlink, then failed at `uv run python scripts/check_docs_links.py`
  because sandbox permissions block the local uv cache path.
