# Functional Requirements -- phenodocs

## FR-FED: Documentation Federation

### FR-FED-001: Multi-Project Aggregation
The build system SHALL pull documentation from 10+ source repositories and aggregate them into a single VitePress site.
**Traces to:** E1.1

### FR-FED-002: Auto-Generated Navigation
The build system SHALL auto-generate sidebar navigation from the aggregated project directory structure.
**Traces to:** E1.1

### FR-FED-003: Full-Text Search
The site SHALL provide full-text search across all federated documentation content.
**Traces to:** E1.1

### FR-FED-004: Layered Views
The site SHALL organize content into layers (lab, docs, audit, kb) with per-layer navigation and index pages.
**Traces to:** E1.2

## FR-GEN: Content Generation

### FR-GEN-001: LLMs.txt Export
The build system SHALL generate `.llms.txt` files at build time containing structured summaries per project section.
**Traces to:** E2.1

### FR-GEN-002: Automated Rebuild
The CI pipeline SHALL trigger documentation rebuilds when source repositories are updated.
**Traces to:** E2.2

### FR-GEN-003: Build Failure on Missing Source
The build SHALL fail explicitly with an actionable error if any configured source repository is unreachable.
**Traces to:** E2.2

## FR-QAL: Site Quality

### FR-QAL-001: Static Build Performance
The full site build SHALL complete in under 60 seconds.
**Traces to:** E3.1

### FR-QAL-002: GitHub Pages Deploy
The CI pipeline SHALL deploy the built site to GitHub Pages with automatic HTTPS.
**Traces to:** E3.1
