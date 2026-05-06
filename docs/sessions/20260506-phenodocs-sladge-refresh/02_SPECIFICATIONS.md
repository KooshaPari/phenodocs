# Specifications

## Functional Contract

- The README badge block must include:
  `[![AI Slop Inside](https://sladge.net/badge.svg)](https://sladge.net)`.
- The badge must appear in the top README status/badge section.
- The change must not modify workflow remediation, ADR, changelog, SOTA, or
  scorecard files from other active workstreams.

## Assumptions, Risks, Uncertainties

- Assumption: Sladge remains governance metadata and should not be added to any
  project catalog data.
- Risk: Active PhenoDocs branches diverge; integration should stay deferred
  unless the owner chooses the target branch.
- Uncertainty: Full docs validation may expose existing link or generated-file
  issues unrelated to the README badge.
