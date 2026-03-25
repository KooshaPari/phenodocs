# Product Requirements Document -- phenodocs

## Product Vision

PhenoDocs is a VitePress federation hub that aggregates documentation from multiple Phenotype projects into a unified, searchable portal. It provides layered views (lab, docs, audit, knowledge base) and generates AI-ready `.llms.txt` files for LLM context consumption.

## E1: Documentation Federation

### E1.1: Multi-Project Aggregation

As a developer, I can browse documentation from all Phenotype projects in one portal without visiting each repo individually.

**Acceptance Criteria:**
- Docs from 10+ projects aggregated into a single VitePress site
- Navigation auto-generated from project structures
- Full-text search across all federated content

### E1.2: Layered Views

As a reader, I can switch between views (lab, docs, audit, kb) to see content relevant to my role.

**Acceptance Criteria:**
- Sidebar navigation groups content by layer
- Each layer has its own index page
- Content can belong to multiple layers via frontmatter tags

## E2: Content Generation

### E2.1: AI-Ready Export

As an AI agent, I can consume project documentation via `.llms.txt` files that contain structured context.

**Acceptance Criteria:**
- `.llms.txt` generated at build time for each project section
- Includes: project name, file tree, key content summaries
- Regenerated on every `docs:build`

### E2.2: Automated Updates

As a maintainer, documentation is automatically pulled and rebuilt when source repos change.

**Acceptance Criteria:**
- Git hooks or CI trigger rebuild on upstream changes
- Build fails explicitly if a source repo is unreachable
- Deploy to GitHub Pages on successful build

## E3: Site Quality

### E3.1: Static Site Build

As a reader, the documentation site loads fast and works without JavaScript when possible.

**Acceptance Criteria:**
- VitePress static generation produces HTML files
- Site builds in < 60 seconds for full rebuild
- Deployed via GitHub Pages with automatic HTTPS
