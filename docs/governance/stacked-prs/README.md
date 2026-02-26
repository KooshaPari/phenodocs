# Stacked PR & Release Governance

Use this module for all roadmap, feature, and review planning.

- [01 Branching and Channels](./01-branching-and-channels.md)
- [02 WBS + DAG Rules](./02-wbs-and-dag.md)
- [03 PR Template](./03-pr-template.md)
- [04 Merge Scenarios](./04-merge-scenarios.md)
- [05 PR Reconciliation](./05-pr-reconciliation.md)
<<<<<<< HEAD
<<<<<<< HEAD
- [06 Release Matrix Template](../../templates/release-matrix-template.md)
=======
- [06 Release Matrix Template](../templates/release-matrix-template.md)
>>>>>>> 0ae50d7 (docs: add stacked PR reconciliation handbook module)
=======
- [06 Release Matrix Template](../../templates/release-matrix-template.md)
>>>>>>> 891a625 (docs: address stacked PR review feedback)

General rules:
- Keep canonical folders on `main`.
- Use `PROJECT-wtrees/<topic>` for all work, QA, and PR prep.
- No top-level merge until required dependencies are in place.
- UI/renderer changes require beta/rc policy unless duplicate-safe.
