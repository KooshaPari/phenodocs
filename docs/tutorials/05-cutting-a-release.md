---
title: 05 — Cutting a release
---

# 05 — Cutting a release

The changelog is generated from conventional commits. The automation
also opens a release PR that bumps the version, updates `CHANGELOG.md`,
and tags the merge.

## Steps

### 1. Make sure your branch is conventional

Each commit on `main` since the last tag follows
[Conventional Commits](https://www.conventionalcommits.org/):

```text
feat(scope): short summary
fix(scope): short summary
chore(deps): bump vitepress to 1.6.0
```

`feat:` triggers a minor bump; `fix:` triggers a patch; a commit with
`BREAKING CHANGE:` in the footer triggers a major bump.

### 2. Wait for the release PR

A bot opens a PR titled `chore(release): vX.Y.Z` whenever `main` has
conventional commits that warrant a bump. CI runs the link checker and
the OpenAPI generator against the candidate.

### 3. Review and merge

Approve the PR if the diff looks right (CHANGELOG.md + version bump).
Merging tags `vX.Y.Z` automatically.

### 4. Verify

- [ ] `git tag --list 'v*'` shows the new tag.
- [ ] `docs/changelog/index.md` lists the new release at the top.
- [ ] GitHub Pages deploys the new build within ~2 minutes.

## Rollback

To roll back a release, revert the merge commit on `main`, then push an
empty commit annotated with `chore: revert vX.Y.Z` so the next release
PR is forced.

## Next

- Browse the [RFC flow](/governance/rfc-flow) for cross-cutting proposals.
- See the [governance overview](/governance/overview) for review timelines.
