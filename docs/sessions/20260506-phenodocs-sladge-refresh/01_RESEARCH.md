# Research

## Existing State

- Current active worktree: `phenodocs` on `ci/add-mypy`, ahead of origin and
  dirty with unrelated workflow and `.agileplus` changes.
- Scorecard remediation worktree: `phenodocs-scorecard-remediation` on
  `ci/pin-trufflehog`, dirty with unrelated workflow, ADR, changelog, SOTA,
  SPEC, README, and `FUNDING.yml` changes.
- Older Sladge worktree: `worktrees/phenodocs/docs/sladge-badge` at commit
  `f8f100f`, clean but not an ancestor of the active `ci/add-mypy` head.

## Decision

Prepare a refreshed README-only badge branch from current `ci/add-mypy` head in
an isolated worktree instead of merging the older prepared branch or touching
dirty sibling checkouts.
