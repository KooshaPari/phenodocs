# RFC flow

Proposals for substantial changes go through the RFC process. The flow is
intentionally lightweight: it should take less than fifteen minutes to
file a new RFC.

## When you need an RFC

| Change | RFC required? |
| --- | --- |
| New top-level nav section in the hub | yes |
| New toolchain dependency (swap `bun` for `pnpm`, etc.) | yes |
| Public API surface change (OpenAPI) | yes |
| Cross-cutting governance or process change | yes |
| New tutorial or guide | no (open a PR) |
| Bug fix / copy edit / broken link | no (open a PR) |
| Internal refactor with no external surface change | optional |

When in doubt, file a one-paragraph `pre-RFC` issue first — the
maintainers will tell you whether it warrants a full RFC.

## Lifecycle

```text
draft → proposed → accepted   ──►  implemented
                ↘
                 rejected
                ↘
                 superseded (by later RFC NNNN)
```

Statuses live in the frontmatter `status:` field. The VitePress site
groups RFCs in the index at [`/rfcs/`](/rfcs/).

## Review SLA

| Stage | Time-box |
| --- | --- |
| First maintainer response | 3 business days |
| Comment window | 7 calendar days |
| Second approval (for `accepted`) | within 14 days of first approval |

If the comment window closes with no objections from a `@phenotype/maintainer`,
the author may mark the RFC `accepted` by merging the PR.

## Merge checklist

Before merging an RFC PR, confirm:

- [ ] `status:` frontmatter matches the decision (`accepted` / `rejected` / `superseded`).
- [ ] The RFC index at `/rfcs/README.md` is updated.
- [ ] All open questions are checked off or moved to follow-up issues.
- [ ] The PR has at least one label: `rfc`, `rfc-accepted`, or `rfc-rejected`.
- [ ] If `accepted`, a tracking issue is opened for the implementation work.

## Implementation handoff

When an RFC is `accepted`:

1. The author (or designee) opens one or more implementation issues
   referencing the RFC number (`refs RFC-NNNN`).
2. Implementation PRs reference the RFC (`Closes #<issue>` where the
   issue references the RFC).
3. The changelog automation tags the merge under **Governance** the
   next time a release cuts.

## Superseding an RFC

An accepted RFC can be superseded by a later RFC. The original RFC
moves to `status: superseded` and gets a `supersededBy: NNNN` line in
its frontmatter. The newer RFC must reference the older one in the
**Motivation** section.

## Out of band

For emergencies (security incidents, broken main build), the
maintainers may ship a change without an RFC. The post-hoc
`postmortem.md` should reference what was bypassed and why.
