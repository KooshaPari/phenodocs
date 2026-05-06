# PhenoDocs Sladge Governance Badge

## Purpose

Make the repository's LLM-heavy documentation and agent-facing context work
explicit by adding the Sladge badge near the top of the project README.

## Scope

- Add the Sladge badge to `README.md`.
- Keep the badge as governance metadata only.
- Preserve existing branch and workflow remediation changes in other worktrees.
- Record validation and integration blockers in session documentation.

## Acceptance Criteria

- `README.md` includes the Sladge badge with the canonical `sladge.net` link.
- The change is prepared in an isolated worktree from the current active head.
- Diff hygiene and README badge presence checks pass.
- Any broader build or link-check blockers are documented without modifying
  unrelated files.
