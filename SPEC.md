# Phenodocs Specification

## Repository Overview

Phenodocs is a VitePress documentation federation hub that aggregates documentation from multiple Phenotype ecosystem projects.

## Architecture

```
phenodocs/
├── docs/                    # VitePress documentation
│   ├── index.md
│   ├── api/
│   ├── guides/
│   └── reference/
├── .vitepress/
│   ├── config.ts           # VitePress configuration
│   └── theme/
├── package.json
└── SPEC.md
```

## xDD Methodologies Applied

### TDD (Test-Driven Development)
- [ ] Unit tests for documentation generation scripts
- [ ] Integration tests for link checking
- [ ] E2E tests for documentation site

### BDD (Behavior-Driven Development)
- [ ] Gherkin scenarios for documentation workflows
- [ ] Feature files for doc generation pipeline

### DDD (Domain-Driven Design)
- [ ] Bounded Contexts: API docs, guides, reference
- [ ] Aggregates: Documentation modules
- [ ] Value Objects: Markdown content, frontmatter schemas

### ATDD (Acceptance TDD)
- [ ] Acceptance criteria for doc rendering
- [ ] Link validation acceptance tests

### MDD (Model-Driven Development)
- [x] VitePress frontmatter schemas
- [ ] TypeScript interfaces for doc models

### IDD (Intent-Driven Development)
- [ ] Intent classification for doc organization
- [ ] Tool definitions for doc generation

## Quality Gates

- markdownlint for style enforcement
- Link validation (check-links script)
- Build verification (vitepress build)
- TypeScript type checking

## CI/CD Pipeline

```yaml
lint:
  - markdownlint docs/**/*.md
  
check-links:
  - python3 scripts/check-docs-links.py

build:
  - npm run build
  
deploy:
  - vitepress deploy
```

## Best Practices

### Documentation as Code
- Treat documentation like source code
- Version control all docs
- Review changes via PRs

### Content Organization
- Modular structure by domain
- Cross-references between docs
- Consistent frontmatter schema

### Maintenance
- Regular link validation
- Stale content detection
- Automated freshness checks

## Related Documentation

- VitePress: https://vitepress.dev
- Documentation Systems: /docs/documentation-systems
- DocOps: /docs/docops
