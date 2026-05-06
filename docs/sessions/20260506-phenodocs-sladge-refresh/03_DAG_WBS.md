# DAG / WBS

## Work Breakdown

1. Inspect live PhenoDocs worktrees and branch ancestry.
2. Verify no existing Sladge-specific AgilePlus/spec record is current.
3. Create an isolated current-head worktree for the badge refresh.
4. Add README badge and a scoped `kitty-specs` record.
5. Validate diff hygiene, badge presence, and repo-native checks.
6. Commit the isolated downstream change.
7. Update `projects-landing` governance and task ledgers with proof.

## Dependencies

- Steps 3-6 depend on preserving dirty sibling checkouts.
- Step 7 depends on the downstream commit hash and validation results.
