---
title: 04 — Writing an RFC
---

# 04 — Writing an RFC

Propose a substantial change using the RFC flow. Use this for changes
that affect public contracts, theme behavior, or build pipeline.

## When to write an RFC

- New top-level nav section.
- New toolchain dependency (e.g. swapping `bun` for `pnpm`).
- Schema changes to the OpenAPI surface.
- Any change that requires a coordinated migration across federated projects.

For small bug fixes or copy edits, open a PR directly — no RFC needed.

## Steps

### 1. Copy the template

```bash
cp docs/rfcs/template.md docs/rfcs/NNN-my-proposal.md
```

Choose the next available `NNN` (check `docs/rfcs/README.md` for the
counter).

### 2. Fill the required sections

The template requires:

- Summary (1–2 paragraphs)
- Motivation (the problem + why now)
- Detailed design
- Drawbacks
- Alternatives considered
- Open questions

### 3. Open a PR in `status: proposed`

Set the frontmatter `status: proposed` and open a PR titled
`rfc(NNN): <title>`. Tag `@phenotype/maintainers`.

### 4. Address review

Reviewers comment on the PR. Once two maintainers approve and a 7-day
comment window has elapsed, the maintainer merges the PR with
`status: accepted`. If rejected, `status: rejected` with a short note.

### 5. Announce

The changelog automation picks up the merged RFC and lists it under
"Governance changes" in the next release.

## Verify

- [ ] The RFC appears in the [RFC index](/rfcs/) under the correct status.
- [ ] Cross-links from the affected docs resolve.
- [ ] The PR has the `rfc` label and at least two approvals.

## Next

Continue to [05 — Cutting a release](./05-cutting-a-release).
