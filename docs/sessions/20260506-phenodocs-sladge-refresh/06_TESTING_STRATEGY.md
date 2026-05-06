# Testing Strategy

## Required

- `git diff --check`
- `rg -n "sladge|AI Slop" README.md`

## Repo-Native

- `bun run build`
- `bun run check`

Any failures from generated docs, stale links, or unrelated toolchain state must
be recorded as blockers instead of broadening this README-only change.
