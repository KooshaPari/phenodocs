---
layout: home
---

<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  console.log('PhenoDocs loaded')
})
</script>

# Welcome to PhenoDocs

**PhenoDocs** is the VitePress Federation Hub that aggregates documentation from multiple projects in the Kush ecosystem into a unified, searchable portal.

## Quick Links

- [Getting Started](/guide/getting-started) — Set up and configure your hub
- [Architecture Guide](/guide/architecture) — Understand the system design
- [API Reference](/reference/api) — Programmatic access
- [Governance](/governance/overview) — Standards and processes

## Documentation Layers

| Layer | View | Purpose |
|:-----:|------|---------|
| 0 | (internal) | Raw/ephemeral docs |
| 1 | [/lab/](/lab/) | Ideas, research, debugging |
| 2 | [/docs/](/docs/) | Specifications, PRDs, ADRs |
| 3 | [/audit/](/audit/) | Changelogs, reports |
| 4 | [/kb/](/kb/) | Knowledge base, retrospectives |

## Features

- **Federated** — Aggregate docs from multiple repositories
- **Layered** — Separate views for different audiences
- **Automated** — Git hooks trigger updates
- **AI-Ready** — `.llms.txt` for LLM context
- **Searchable** — Full-text search across all projects

## Contributing

See our [Governance](/governance/overview) document for contribution guidelines.
