# RFCs

This directory hosts Request-For-Comments documents. Each RFC is a single
Markdown file numbered `NNNN-short-title.md`. The status is tracked in
the frontmatter.

## Index

The index below is hand-maintained. Update it when an RFC changes
status. (We do not auto-generate it because the doc site must render
even when the script that scans frontmatter is broken.)

### Proposed

- [RFC 0000 — RFC template](./template.md) (reference, do not count)

### Accepted

_None yet._

### Rejected

_None yet._

### Superseded

_None yet._

## Numbering

The next free number is **0001**. Use it for the next new RFC.

To allocate a number:

1. Run `just new-rfc` (or copy `template.md` manually).
2. Update this index immediately so reviewers see the new entry.
3. Open a PR.

## Process

See [`/governance/rfc-flow`](/governance/rfc-flow) for the end-to-end
flow, including review timelines, label conventions, and the merge
checklist.
