---
status: proposed
number: 0000
title: 'RFC template - copy and fill'
date: YYYY-MM-DD
author: your-handle
---

# RFC NNNN — <Title>

> Status: **proposed** · Last updated: YYYY-MM-DD · Author: @handle

## Summary

One paragraph. What does this RFC change, in one sentence?

## Motivation

Why now? What problem does this solve? What is the user-visible impact if
we do nothing?

## Detailed design

This is the meat of the RFC. Cover:

- API surface changes (new endpoints, removed endpoints, schema changes)
- VitePress routing / sidebar implications
- Build / CI / toolchain impact
- Migration plan for existing consumers

Include code snippets, ASCII diagrams, or Mermaid blocks where they help.

## Drawbacks

Be honest. Why might this be a bad idea? What does it cost in
complexity, build time, or operational burden?

## Alternatives considered

What other approaches did you consider? Why is this design better?

## Open questions

- [ ] Question 1 — assignee / decision needed by YYYY-MM-DD
- [ ] Question 2

## Unresolved decisions

Anything the review thread should hit hard before merging.

---

## Review process

1. PR opened with `rfc` label.
2. Maintainers have 7 days to comment.
3. Two approvals (one must be a `@phenotype/maintainer`) move the RFC
   to **accepted**; merging the PR sets `status: accepted` in the
   frontmatter.
4. To reject, merge with `status: rejected` and a one-line note in
   the **Drawbacks** section.

See [`/governance/rfc-flow`](/governance/rfc-flow) for the full flow.
