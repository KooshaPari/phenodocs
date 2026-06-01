# Known Issues

## Stale Prepared Branch

`worktrees/phenodocs/docs/sladge-current` is not an ancestor of the active
`fix/tsconfig-strict-mode` branch. It includes broad unrelated workflow and docs
tree changes and should not be integrated.

## Validation Limits

No implementation changes are part of this refresh. Any broader build or check
failures should be treated as current-branch baseline or environment blockers
unless they involve README/session docs.

## Sandbox UV Cache Blocker

`bun run check` runs oxlint and vue-tsc successfully when the canonical
dependency tree is linked into the isolated worktree, then fails at the Python
link-check step because `uv` cannot open
`/Users/kooshapari/.cache/uv/sdists-v9/.git` in this sandbox.
