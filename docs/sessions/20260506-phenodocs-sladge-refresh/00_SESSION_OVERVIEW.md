# PhenoDocs Sladge Refresh

## Goal

Refresh the older PhenoDocs Sladge badge branch against the current active
`ci/add-mypy` head while preserving unrelated local workflow and scorecard
remediation work in sibling checkouts.

## Outcome

- Created isolated worktree `worktrees/phenodocs/docs/sladge-current`.
- Added the Sladge badge to `README.md`.
- Added `kitty-specs/phenodocs-sladge-governance/SPEC.md`.
- Kept dirty canonical and scorecard remediation checkouts untouched.

## Success Criteria

- README badge proof passes.
- `git diff --check` passes.
- Repo-native validation is attempted and any unrelated blockers are recorded.
