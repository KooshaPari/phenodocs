# PhenoDocs Specification

## Version

- **Version**: 2.0.0
- **Date**: 2026-04-04
- **Status**: Stable
- **Review Cycle**: Monthly

---

## 1. Mission and Tenets

### Mission

PhenoDocs provides world-class documentation infrastructure for the Phenotype ecosystem. It aggregates, organizes, and delivers documentation from multiple projects into a unified, searchable, AI-ready portal.

### Tenets (unless you know better ones)

These tenets guide PhenoDocs development:

1. **Federation First**:

Documentation at scale requires aggregation. PhenoDocs treats documentation as a federated resource, pulling from multiple sources into a unified experience while respecting source autonomy.

2. **Developer Experience**:

Documentation is only useful if developers can find and understand it. Every decision prioritizes search quality, navigation clarity, and content discoverability.

3. **AI-Ready**:

Modern documentation serves both humans and AI agents. PhenoDocs generates structured context (`.llms.txt`) and exposes tools via MCP for agent integration.

4. **Content Layers**:

Not all documentation is equal. The five-layer model (ephemeral through knowledge base) provides appropriate lifecycle and audience targeting for different content types.

5. **Performance**:

Documentation must load instantly. Build times, page weight, and search latency are critical metrics.

---

## 2. System Overview

### 2.1 Architecture

PhenoDocs is a federated documentation hub built on VitePress with custom tooling for content aggregation.

```
┌─────────────────────────────────────────────────────────────┐
│                       PhenoDocs Hub                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Lab View   │  │  Docs View   │  │  Audit View  │     │
│  │   (/lab/)    │  │  (/docs/)    │  │  (/audit/)   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              Unified Search Index                      │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              .llms.txt Generator                     │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │ Project A│   │ Project B│   │ Project C│
        │  (docs)  │   │  (docs)  │   │  (docs)  │
        └──────────┘   └──────────┘   └──────────┘
```

### 2.2 Core Components

| Component | Purpose | Technology |
|-----------|---------|------------|
| Hub Core | Static site generation | VitePress 1.6 |
| Theme | UI components and styling | Vue 3 + Keycap DS |
| HubGenerator | Content aggregation | Python + TypeScript |
| Search | Full-text search | VitePress local |
| LLMS Generator | AI context generation | Python |
| Config Utils | Configuration merging | TypeScript |

### 2.3 Data Flow

```
1. Source Discovery
   HubGenerator scans configured source repositories
   
2. Content Ingestion
   Markdown files copied with frontmatter transformation
   
3. Index Generation
   Search index built from all content
   
4. Site Build
   VitePress generates static site
   
5. Post-Processing
   .llms.txt generated, assets optimized
   
6. Deployment
   Static site deployed to GitHub Pages
```

---

## 3. Content Architecture

### 3.1 Layered Content Model

PhenoDocs implements a five-layer content architecture:

| Layer | Name | Directory | Audience | Review Cycle | Searchable |
|-------|------|-----------|----------|----------------|------------|
| 0 | Ephemeral | `.scratch/` | Self | N/A | No |
| 1 | Lab | `lab/` | Team | Weekly | Yes |
| 2 | Docs | `docs/` `planning/` | Org | Monthly | Yes |
| 3 | Audit | `audit/` | Compliance | Quarterly | Yes |
| 4 | KB | `kb/` | Industry | Biannual | Yes |

### 3.2 Layer Semantics

**Layer 0: Ephemeral**
- Scratch notes, conversation dumps, temporary files
- No review cycle, no search indexing
- Purged periodically
- Never deployed to production

**Layer 1: Lab**
- Experimental content, research notes, debug logs
- Team-internal audience
- Weekly review for promotion to Layer 2 or archival
- Searchable but marked as experimental

**Layer 2: Docs**
- Formal documentation: PRDs, ADRs, specifications, guides
- Organization-wide audience
- Monthly review for accuracy
- Primary documentation layer

**Layer 3: Audit**
- Changelogs, completion reports, compliance documentation
- Compliance and audit audience
- Quarterly review
- Immutable history (append-only)

**Layer 4: KB**
- Curated knowledge, retrospectives, patterns
- Industry audience
- Biannual review for continued relevance
- Highest editorial standards

### 3.3 Content Types by Layer

**Layer 2 (Docs) Content Types**:

| Type | Purpose | Example |
|------|---------|---------|
| Tutorial | Learning-oriented | "Getting Started with PhenoDocs" |
| Guide | Problem-oriented | "How to Add a Project" |
| Explanation | Understanding-oriented | "Federation Architecture" |
| Reference | Information-oriented | "API Reference" |
| ADR | Decision record | "Build-Time Federation" |
| PRD | Requirements | "Search Enhancement PRD" |

### 3.4 Frontmatter Schema

All content layers share a common frontmatter schema:

```yaml
---
# Identity (required)
id: unique-content-id
title: Content Title
category: tutorial | guide | explanation | reference | adr | prd
layer: 0 | 1 | 2 | 3 | 4

# Lifecycle (required)
status: draft | review | stable | deprecated | archived
created: 2026-04-04
updated: 2026-04-04
review_cycle: weekly | monthly | quarterly | biannual

# Attribution (required)
author: github-username
project: project-id

# Optional
contributors: [github-username, ...]
tags: [tag1, tag2]
related: [content-id, ...]
llms_extract: true | false
llms_priority: critical | high | medium | low
description: SEO/summary description
sidebar: true | false
prev: content-id
next: content-id
---
```

### 3.5 File Organization

```
phenodocs/
├── docs/                           # Layer 2: Documentation
│   ├── index.md                   # Hub landing page
│   ├── guide/
│   │   ├── index.md
│   │   ├── getting-started.md
│   │   └── configuration.md
│   ├── reference/
│   │   ├── index.md
│   │   ├── api.md
│   │   └── components.md
│   └── planning/
│       ├── index.md
│       ├── adrs.md
│       └── specs.md
├── lab/                           # Layer 1: Lab/Research
│   ├── experiments/
│   └── research/
├── audit/                         # Layer 3: Audit
│   ├── changelog.md
│   └── worklogs/
└── kb/                           # Layer 4: Knowledge Base
    ├── patterns/
    └── retrospectives/
```

---

## 4. Federation System

### 4.1 Overview

PhenoDocs aggregates documentation from multiple source repositories at build time. This enables:

- Unified search across all projects
- Consistent theming and navigation
- Single deployment target
- Cross-project linking

### 4.2 HubGenerator Architecture

The HubGenerator is the core federation engine:

```typescript
interface HubGenerator {
  // Configuration
  hubDir: string;
  projects: ProjectMap;
  layers: LayerConfig[];
  
  // Core methods
  discover(): SourceFiles[];
  validate(sources: SourceFiles[]): ValidationResult;
  transform(sources: SourceFiles[]): TransformedFiles[];
  write(files: TransformedFiles[]): void;
  generateIndices(): void;
}

interface ProjectMap {
  [projectId: string]: {
    sourcePath: string;
    targetPath: string;
    layers: number[];
    include: string[];
    exclude: string[];
  };
}
```

### 4.3 Federation Workflow

```
Phase 1: Discovery
├── Scan all configured project paths
├── Filter by include/exclude patterns
└── Build source file manifest

Phase 2: Validation
├── Verify source paths exist
├── Check for ID collisions
├── Validate frontmatter schema
└── Report errors/warnings

Phase 3: Transformation
├── Copy files to hub directory
├── Transform frontmatter (add project attribution)
├── Rewrite relative links
└── Generate breadcrumb data

Phase 4: Index Generation
├── Build search index
├── Generate navigation trees
├── Create cross-reference maps
└── Update VitePress config

Phase 5: Build Integration
├── Trigger VitePress build
├── Generate .llms.txt
└── Optimize assets
```

### 4.4 Project Configuration

Projects are configured in `hub.config.yaml`:

```yaml
hub:
  dir: ./docs
  title: PhenoDocs Hub
  description: Federated documentation for Phenotype

projects:
  phenodocs:
    source: ./packages/docs
    target: ./reference
    layers: [2, 3]
    include:
      - docs/**
      - README.md
    exclude:
      - node_modules/**
      - .**

  thegent:
    source: ../thegent/docs
    target: ./projects/thegent
    layers: [1, 2, 3]
    include:
      - "**/*.md"
    exclude:
      - scratch/**

  agileplus:
    source: ../AgilePlus/docs
    target: ./projects/agileplus
    layers: [2, 3]
    include:
      - specs/**
      - guides/**
```

### 4.5 Frontmatter Transformation

Source frontmatter is enriched during federation:

```yaml
# Source (in thegent repo)
---
id: agent-lifecycle
title: Agent Lifecycle
layer: 2
status: stable
author: pheno-team
---

# Transformed (in hub)
---
id: thegent-agent-lifecycle
title: Agent Lifecycle
category: reference
layer: 2
status: stable
created: 2026-03-15
updated: 2026-04-02
review_cycle: monthly
author: pheno-team
project: thegent
source_repo: github.com/phenotype/thegent
source_path: docs/reference/agent-lifecycle.md
source_commit: abc123
federated: true
federated_at: 2026-04-04T12:00:00Z
---
```

### 4.6 Link Rewriting

Relative links are rewritten to maintain validity in the hub:

```markdown
<!-- Source -->
[See also](./getting-started.md)
[API Reference](../reference/api.md)

<!-- Transformed -->
[See also](/projects/thegent/guide/getting-started)
[API Reference](/projects/thegent/reference/api)
```

### 4.7 Error Handling

| Error | Severity | Action |
|-------|----------|--------|
| Source path not found | Fatal | Stop build, alert maintainer |
| Duplicate content ID | Fatal | Stop build, require resolution |
| Invalid frontmatter | Warning | Skip file, log warning |
| Broken internal link | Warning | Log for review, build continues |
| Missing required field | Error | Skip file, report in summary |

---

## 5. Theme and Components

### 5.1 Keycap Design System

PhenoDocs implements the Keycap Design System with the following tokens:

```css
:root {
  /* Colors */
  --kp-bg-primary: #0f0f0f;
  --kp-bg-secondary: #1a1a1a;
  --kp-bg-tertiary: #262626;
  
  --kp-fg-primary: #fafafa;
  --kp-fg-secondary: #a1a1aa;
  --kp-fg-tertiary: #52525b;
  
  --kp-accent-primary: #3b82f6;
  --kp-accent-secondary: #8b5cf6;
  
  /* Typography */
  --kp-font-ui: 'Inter', system-ui, sans-serif;
  --kp-font-mono: 'JetBrains Mono', monospace;
  
  /* Spacing */
  --kp-space-1: 4px;
  --kp-space-2: 8px;
  --kp-space-3: 12px;
  --kp-space-4: 16px;
  --kp-space-6: 24px;
  --kp-space-8: 32px;
  
  /* Radii */
  --kp-radius-sm: 4px;
  --kp-radius-md: 8px;
  --kp-radius-lg: 12px;
}
```

### 5.2 Component Inventory

| Component | Purpose | Location |
|-----------|---------|----------|
| DocStatusBadge | Display layer/status | `theme/components/DocStatusBadge.vue` |
| KBGraph | Knowledge graph visualization | `theme/components/KBGraph.vue` |
| CommitLog | Recent changes display | `theme/components/CommitLog.vue` |
| CodePlayground | Interactive code examples | `theme/components/CodePlayground.vue` |
| OpenAPI | API spec rendering | `theme/components/OpenAPI.vue` |
| AuditTimeline | Review timeline | `theme/components/AuditTimeline.vue` |
| ModuleSwitcher | Project/module navigation | `theme/components/ModuleSwitcher.vue` |
| StickyHeader | Persistent navigation | `theme/components/StickyHeader.vue` |
| StickySidebar | Collapsible sidebar | `theme/components/StickySidebar.vue` |
| ContentTabs | Tabbed content | `theme/components/ContentTabs.vue` |
| CategorySwitcher | Content category filter | `theme/components/CategorySwitcher.vue` |
| Breadcrumb | Navigation path | `theme/components/Breadcrumb.vue` |
| BackToTop | Scroll to top | `theme/components/BackToTop.vue` |
| DemoGif | Animated demonstrations | `theme/components/DemoGif.vue` |
| LoadingSpinner | Loading state | `theme/components/LoadingSpinner.vue` |
| Callout | Highlighted content blocks | `theme/components/Callout.vue` |
| CodeAnnotation | Annotated code blocks | `theme/components/CodeAnnotation.vue` |
| NavTabs | Tabbed navigation | `theme/components/NavTabs.vue` |
| Toast/ToastContainer | Notifications | `theme/components/Toast*.vue` |
| Tooltip | Contextual help | `theme/components/Tooltip.vue` |

### 5.3 DocStatusBadge Specification

The DocStatusBadge component visualizes content metadata:

```vue
<template>
  <span class="doc-status-badge" :class="[layerClass, statusClass]">
    <span class="badge-icon">{{ icon }}</span>
    <span class="badge-text">{{ displayText }}</span>
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  layer: 0 | 1 | 2 | 3 | 4;
  status: 'draft' | 'review' | 'stable' | 'deprecated' | 'archived';
  showText?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  showText: true
});

const layerConfig = {
  0: { icon: '⚡', label: 'Ephemeral', color: '#6b7280' },
  1: { icon: '🔬', label: 'Lab', color: '#3b82f6' },
  2: { icon: '📚', label: 'Docs', color: '#10b981' },
  3: { icon: '📋', label: 'Audit', color: '#f59e0b' },
  4: { icon: '🧠', label: 'KB', color: '#8b5cf6' }
};

const statusConfig = {
  draft: { color: '#6b7280', bg: 'rgba(107, 114, 128, 0.1)' },
  review: { color: '#3b82f6', bg: 'rgba(59, 130, 246, 0.1)' },
  stable: { color: '#10b981', bg: 'rgba(16, 185, 129, 0.1)' },
  deprecated: { color: '#ef4444', bg: 'rgba(239, 68, 68, 0.1)' },
  archived: { color: '#6b7280', bg: 'rgba(107, 114, 128, 0.1)' }
};
</script>
```

### 5.4 Layout System

```
┌─────────────────────────────────────────────────────────┐
│                    StickyHeader                          │
│  Logo    Nav          Search    Theme    GitHub          │
├──────────┬──────────────────────────────────────────────┤
│          │                                              │
│ Sticky   │              Main Content                    │
│ Sidebar  │                                              │
│          │  ┌─────────────────────────────────────────┐  │
│ - Nav    │  │           Breadcrumb                   │  │
│ - Status │  └─────────────────────────────────────────┘  │
│ - TOC    │                                              │
│          │  ┌─────────────────────────────────────────┐  │
│          │  │         DocStatusBadge                 │  │
│          │  │         Title & Metadata               │  │
│          │  └─────────────────────────────────────────┘  │
│          │                                              │
│          │              Content Body                    │
│          │                                              │
│          │  ┌─────────────────────────────────────────┐  │
│          │  │         Related / Next/Prev            │  │
│          │  └─────────────────────────────────────────┘  │
│          │                                              │
└──────────┴──────────────────────────────────────────────┘
```

---

## 6. Search System

### 6.1 Architecture

PhenoDocs uses VitePress's built-in local search (based on MiniSearch):

```
Build Time:
  Markdown ──► Parse ──► Extract Text ──► Build Index ──► index.js

Runtime:
  User Input ──► MiniSearch Query ──► Rank Results ──► Display
```

### 6.2 Index Structure

```typescript
interface SearchIndex {
  documents: SearchDocument[];
  index: MiniSearch.Index;
}

interface SearchDocument {
  id: string;
  title: string;
  titles: string[];        // H2, H3 headings
  text: string;           // Body content
  layer: number;
  project: string;
  category: string;
}
```

### 6.3 Search Configuration

```typescript
// .vitepress/config.ts
export default defineConfig({
  themeConfig: {
    search: {
      provider: 'local',
      options: {
        miniSearch: {
          options: {
            // Tokenization
            tokenize: (text) => text.split(/[\s\-/_]+/),
            
            // Fuzzy matching
            fuzzy: 0.25,
            
            // Boost factors
            boost: {
              title: 4,
              titles: 2,
              text: 1
            }
          },
          
          // Search options
          searchOptions: {
            prefix: true,
            fuzzy: 2,      // Damerau-Levenshtein distance
            boost: {
              title: 5,
              titles: 3,
              text: 1
            }
          }
        }
      }
    }
  }
});
```

### 6.4 Search Ranking

Results are ranked by:

1. **Exact title match**: 5x boost
2. **Heading match**: 3x boost
3. **Body match**: 1x (default)
4. **Layer priority**: Layer 4 > Layer 3 > Layer 2 > Layer 1
5. **Recency**: More recently updated content gets slight boost

### 6.5 Search UI

```
┌────────────────────────────────────────┐
│  Search docs...               ⌘ K    │
└────────────────────────────────────────┘
              │
              ▼
┌────────────────────────────────────────┐
│ 🔍 federation                          │
├────────────────────────────────────────┤
│ 📚 Build-Time Federation    (Guide)    │
│    ADR-001: Federation architecture    │
│    ─────────────────────────────────   │
│ 📚 HubGenerator API         (Ref)    │
│    Generate federated documentation  │
│    ─────────────────────────────────   │
│ 🔬 Federation Experiments   (Lab)     │
│    Research on alternative approaches │
└────────────────────────────────────────┘
```

---

## 7. AI Integration

### 7.1 .llms.txt Specification

The `.llms.txt` file provides structured context for Large Language Models:

```
# PhenoDocs

> Federated documentation hub for the Phenotype ecosystem

## Docs

Critical documentation for understanding and using PhenoDocs:

- [Getting Started](https://phenotype.dev/docs/getting-started): Installation, quick start, and basic concepts
- [Architecture](https://phenotype.dev/docs/architecture): System design, federation model, and content layers
- [Hub Generator](https://phenotype.dev/docs/hub-generator): CLI tool for documentation aggregation

## Optional

Additional reference material:

- [API Reference](https://phenotype.dev/reference/api): Complete API documentation
- [ADRs](https://phenotype.dev/planning/adrs): Architecture decision records
- [Changelog](https://phenotype.dev/audit/changelog): Version history

## MCP Tools

- `phenodocs_search`: Search documentation across all projects
- `phenodocs_hub_generate`: Generate federated documentation hub
```

### 7.2 Generation Algorithm

```python
def generate_llms_txt(config: Config) -> str:
    # Collect all pages with llms_extract=true
    pages = collect_extractable_pages(config.hub_dir)
    
    # Classify by priority
    critical = [p for p in pages if p.frontmatter.llms_priority == 'critical']
    high = [p for p in pages if p.frontmatter.llms_priority == 'high']
    medium = [p for p in pages if p.frontmatter.llms_priority == 'medium']
    
    # Generate summaries for critical/high priority
    for page in critical + high:
        page.summary = generate_summary(page.content)
    
    # Build .llms.txt content
    lines = [
        "# " + config.title,
        "",
        "> " + config.description,
        "",
        "## Docs",
        "",
    ]
    
    for page in critical:
        lines.append(f"- [{page.title}]({page.url}): {page.summary}")
    
    lines.extend(["", "## Optional", ""])
    
    for page in high + medium:
        lines.append(f"- [{page.title}]({page.url}): {page.summary or page.description}")
    
    return "\n".join(lines)
```

### 7.3 MCP Tool Exposure

PhenoDocs exposes functionality via Model Context Protocol:

```typescript
// tools/search.ts
interface SearchTool {
  name: 'phenodocs_search';
  description: 'Search documentation across all Phenotype projects';
  parameters: {
    query: string;
    layer?: number;
    project?: string;
    limit?: number;
  };
  returns: SearchResult[];
}

// tools/hub-generate.ts
interface HubGenerateTool {
  name: 'phenodocs_hub_generate';
  description: 'Generate federated documentation hub';
  parameters: {
    projects?: string[];
    dryRun?: boolean;
  };
  returns: GenerationReport;
}
```

---

## 8. Configuration System

### 8.1 Configuration Architecture

```
Base Config (@phenotype/docs)
         │
         ▼
   Hub Defaults
         │
         ▼
   Project Config
         │
         ▼
   Environment Config
         │
         ▼
   Runtime Overrides
```

### 8.2 Base Configuration

```typescript
// @phenotype/docs default configuration
export const baseConfig = defineConfig({
  title: 'PhenoDocs',
  description: 'Federated documentation hub',
  
  // Appearance
  appearance: true,  // Dark/light mode
  
  // Markdown
  markdown: {
    lineNumbers: true,
    theme: {
      light: 'github-light',
      dark: 'github-dark'
    }
  },
  
  // Theme
  themeConfig: {
    logo: '/logo.svg',
    
    nav: [
      { text: 'Lab', link: '/lab/' },
      { text: 'Docs', link: '/docs/' },
      { text: 'Audit', link: '/audit/' },
      { text: 'KB', link: '/kb/' }
    ],
    
    sidebar: {
      '/docs/': generateSidebar({
        srcDir: 'docs',
        prefix: '/docs',
        capitalizeGroups: true
      })
    },
    
    search: {
      provider: 'local'
    },
    
    socialLinks: [
      { icon: 'github', link: 'https://github.com/phenotype' }
    ],
    
    footer: {
      message: 'Released under the MIT License',
      copyright: 'Copyright © 2026 Phenotype'
    }
  }
});
```

### 8.3 deepMerge Implementation

```typescript
// packages/docs/src/utils/config-merger.ts
export function deepMerge<T extends Record<string, any>>(
  target: T,
  source: Partial<T>
): T {
  const result = { ...target };
  
  for (const key in source) {
    const sourceValue = source[key];
    const targetValue = result[key];
    
    if (
      sourceValue &&
      targetValue &&
      typeof sourceValue === 'object' &&
      typeof targetValue === 'object' &&
      !Array.isArray(sourceValue)
    ) {
      // Recurse for objects
      result[key] = deepMerge(targetValue, sourceValue);
    } else if (Array.isArray(sourceValue) && Array.isArray(targetValue)) {
      // Concatenate arrays
      result[key] = [...targetValue, ...sourceValue] as any;
    } else {
      // Override primitives
      result[key] = sourceValue as any;
    }
  }
  
  return result;
}
```

### 8.4 Consumer Configuration

```typescript
// phenodocs/.vitepress/config.ts
import { createPhenotypeConfig } from '@phenotype/docs';

export default createPhenotypeConfig({
  title: 'PhenoDocs Hub',
  description: 'Federated documentation for the Phenotype ecosystem',
  
  themeConfig: {
    // Merges with defaults
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Guide', link: '/guide/' },
      { text: 'Reference', link: '/reference/' },
      { text: 'Planning', link: '/planning/' }
    ]
  }
});
```

---

## 9. Sidebar Generation

### 9.1 Algorithm

```typescript
function generateSidebar(options: SidebarOptions): SidebarItem[] {
  const { srcDir, prefix, capitalizeGroups = true } = options;
  
  const items: SidebarItem[] = [];
  const entries = readdirSync(srcDir);
  
  // Handle index.md first
  if (entries.includes('index.md')) {
    items.push({
      text: 'Overview',
      link: `${prefix}/`
    });
  }
  
  // Process remaining entries
  for (const entry of entries.sort()) {
    const fullPath = join(srcDir, entry);
    const stat = statSync(fullPath);
    
    if (stat.isDirectory()) {
      // Recurse into subdirectory
      const children = generateSidebar({
        srcDir: fullPath,
        prefix: `${prefix}/${entry}`,
        capitalizeGroups
      });
      
      if (children.length > 0) {
        items.push({
          text: capitalizeGroups 
            ? titleCase(entry) 
            : entry,
          collapsed: true,
          items: children
        });
      }
    } else if (entry.endsWith('.md') && entry !== 'index.md') {
      // Add markdown file
      const name = entry.replace('.md', '');
      const title = extractTitle(fullPath) || titleCase(name);
      
      items.push({
        text: title,
        link: `${prefix}/${name}`
      });
    }
  }
  
  return items;
}
```

### 9.2 Generated Structure

```
source/
├── index.md
├── getting-started.md
├── configuration.md
├── advanced/
│   ├── index.md
│   ├── federation.md
│   └── theming.md
└── reference/
    ├── index.md
    ├── api.md
    └── components.md

sidebar:
├── Overview (/)
├── Getting Started
├── Configuration
├── Advanced (collapsed)
│   ├── Overview
│   ├── Federation
│   └── Theming
└── Reference (collapsed)
    ├── Overview
    ├── API
    └── Components
```

---

## 10. Build and Deployment

### 10.1 Build Pipeline

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Install   │───▶│   Generate  │───▶│    Build    │
│  (bun)      │    │   (docs)    │    │  (VitePress)│
└─────────────┘    └─────────────┘    └─────────────┘
                                            │
                       ┌────────────────────┘
                       ▼
              ┌─────────────┐    ┌─────────────┐
              │ Post-Process│───▶│   Deploy    │
              │(.llms.txt)  │    │(GitHub Pages│
              └─────────────┘    └─────────────┘
```

### 10.2 Build Scripts

```json
{
  "scripts": {
    "dev": "vitepress dev docs",
    "build": "npm run hub:generate && vitepress build docs",
    "preview": "vitepress preview docs",
    "hub:generate": "docs hub --hub-dir docs",
    "hub:check": "docs hub --hub-dir docs --dry-run",
    "check": "vue-tsc && markdownlint docs/**/*.md",
    "typecheck": "vue-tsc",
    "lint": "markdownlint docs/**/*.md && vale docs/",
    "link-check": "lychee docs/",
    "llms:generate": "python scripts/generate_llms.py docs/.vitepress/dist"
  }
}
```

### 10.3 CI/CD Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 */4 * * *'  # Every 4 hours
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
          
      - name: Setup Bun
        uses: oven-sh/setup-bun@v1
        with:
          bun-version: 1.3.10
          
      - name: Install dependencies
        run: bun install
        
      - name: Generate Hub
        run: bun run hub:generate
        
      - name: Build
        run: bun run build
        
      - name: Generate .llms.txt
        run: bun run llms:generate
        
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: docs/.vitepress/dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    steps:
      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v4
```

### 10.4 Deployment Configuration

```yaml
# .github/workflows/deploy.yml (environment)
environment:
  name: github-pages
  url: ${{ steps.deployment.outputs.page_url }}
  
concurrency:
  group: pages
  cancel-in-progress: false
```

---

## 11. Quality Assurance

### 11.1 Linting

| Tool | Purpose | Configuration |
|------|---------|---------------|
| markdownlint | Markdown syntax | `.markdownlint.yaml` |
| Vale | Prose style | `.vale.ini` |
| vue-tsc | TypeScript/Vue types | `tsconfig.json` |
| oxlint | JavaScript linting | Built-in |
| lychee | Link checking | CLI flags |

### 11.2 Markdown Rules

```yaml
# .markdownlint.yaml
default: true

# Enable
MD013: false        # Line length (handled by prettier)
MD024: false        # Duplicate headings allowed in different sections
MD033: false        # Allow inline HTML (for Vue components)
MD041: false        # First line doesn't need to be H1 (VitePress handles)

# Custom
MD046:              # Code block style
  style: fenced
```

### 11.3 Type Checking

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "jsx": "preserve",
    "sourceMap": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "esModuleInterop": true,
    "lib": ["ESNext", "DOM"],
    "skipLibCheck": true,
    "noEmit": true
  },
  "include": [
    "packages/docs/src/**/*.ts",
    "packages/docs/src/**/*.vue",
    "docs/.vitepress/**/*.ts"
  ]
}
```

### 11.4 Link Checking

```bash
# Check all links
lychee docs/ --exclude-path node_modules

# Exclude patterns
--exclude "https://localhost*"
--exclude "https://example.com"
```

---

## 12. API Reference

### 12.1 HubGenerator API

```typescript
class HubGenerator {
  constructor(config: HubGeneratorConfig);
  
  // Core methods
  discover(): Promise<SourceFile[]>;
  validate(files: SourceFile[]): ValidationResult;
  transform(files: SourceFile[]): TransformedFile[];
  write(files: TransformedFile[]): void;
  generate(): Promise<GenerationReport>;
  
  // Utility methods
  addProject(id: string, config: ProjectConfig): void;
  removeProject(id: string): void;
  listProjects(): ProjectConfig[];
}

interface HubGeneratorConfig {
  hubDir: string;
  projects: Record<string, ProjectConfig>;
  transforms?: TransformConfig[];
  cacheDir?: string;
}

interface ProjectConfig {
  sourcePath: string;
  targetPath: string;
  layers?: number[];
  include?: string[];
  exclude?: string[];
  transform?: (file: SourceFile) => TransformedFile;
}

interface GenerationReport {
  projects: number;
  filesProcessed: number;
  filesSkipped: number;
  errors: Error[];
  warnings: Warning[];
  duration: number;
}
```

### 12.2 createPhenotypeConfig API

```typescript
function createPhenotypeConfig(
  overrides: UserConfig
): UserConfig;

// Usage
import { createPhenotypeConfig } from '@phenotype/docs';

export default createPhenotypeConfig({
  title: 'My Docs',
  themeConfig: {
    nav: [
      { text: 'Home', link: '/' }
    ]
  }
});
```

### 12.3 Sidebar Generator API

```typescript
function generateSidebar(
  options: SidebarOptions
): DefaultTheme.SidebarItem[];

interface SidebarOptions {
  srcDir: string;
  prefix: string;
  capitalizeGroups?: boolean;
  maxDepth?: number;
  filter?: (path: string) => boolean;
}
```

---

## 13. Package Structure

### 13.1 @phenotype/docs

```
packages/docs/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts              # Main exports
│   ├── config/
│   │   └── index.ts          # createPhenotypeConfig
│   ├── theme/
│   │   ├── index.ts          # Theme registration
│   │   ├── components/       # Vue components
│   │   │   ├── DocStatusBadge.vue
│   │   │   ├── KBGraph.vue
│   │   │   └── ...
│   │   └── composables/      # Vue composables
│   │       ├── useSidebar.ts
│   │       ├── useSearch.ts
│   │       └── useLayer.ts
│   ├── utils/
│   │   ├── config-merger.ts  # deepMerge
│   │   └── sidebar-generator.ts
│   ├── types/
│   │   └── index.ts          # TypeScript types
│   └── css/
│       ├── keycap-palette.css
│       └── custom.css
└── README.md
```

### 13.2 Export Map

```json
{
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js"
    },
    "./theme": {
      "types": "./dist/theme/index.d.ts",
      "import": "./dist/theme/index.js"
    },
    "./config": {
      "types": "./dist/config/index.d.ts",
      "import": "./dist/config/index.js"
    },
    "./utils": {
      "types": "./dist/utils/index.d.ts",
      "import": "./dist/utils/index.js"
    },
    "./types": {
      "types": "./dist/types/index.d.ts",
      "import": "./dist/types/index.js"
    },
    "./css/keycap-palette.css": "./dist/css/keycap-palette.css",
    "./css/custom.css": "./dist/css/custom.css"
  }
}
```

---

## 14. Testing Strategy

### 14.1 Test Categories

| Category | Tools | Coverage Target |
|----------|-------|-----------------|
| Unit | Vitest | 80% |
| Integration | Playwright | Critical paths |
| Visual | Chromatic | All components |
| E2E | Playwright | User flows |

### 14.2 Component Testing

```typescript
// DocStatusBadge.spec.ts
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import DocStatusBadge from './DocStatusBadge.vue';

describe('DocStatusBadge', () => {
  it('renders layer icon', () => {
    const wrapper = mount(DocStatusBadge, {
      props: { layer: 2, status: 'stable' }
    });
    
    expect(wrapper.find('.badge-icon').text()).toBe('📚');
  });
  
  it('applies correct color for each layer', () => {
    const layers = [0, 1, 2, 3, 4] as const;
    const expectedColors = [
      '#6b7280',
      '#3b82f6',
      '#10b981',
      '#f59e0b',
      '#8b5cf6'
    ];
    
    layers.forEach((layer, i) => {
      const wrapper = mount(DocStatusBadge, {
        props: { layer, status: 'stable' }
      });
      
      expect(
        wrapper.find('.doc-status-badge').attributes('style')
      ).toContain(expectedColors[i]);
    });
  });
});
```

### 14.3 E2E Testing

```typescript
// e2e/search.spec.ts
import { test, expect } from '@playwright/test';

test('search finds documentation', async ({ page }) => {
  await page.goto('/');
  
  // Open search
  await page.keyboard.press('Control+k');
  await expect(page.locator('.search-modal')).toBeVisible();
  
  // Type query
  await page.locator('.search-input').fill('federation');
  
  // Wait for results
  await expect(page.locator('.search-result')).toHaveCount(
    greaterThan(0)
  );
  
  // Click first result
  await page.locator('.search-result').first().click();
  
  // Verify navigation
  await expect(page).toHaveURL(/.*federation.*/);
});
```

---

## 15. Migration Guide

### 15.1 From Single Repo to Federation

1. **Prepare Source Repos**:
   ```bash
   # In each source repo
   mkdir -p docs
   mv README.md docs/index.md
   # Add frontmatter to existing docs
   ```

2. **Configure Hub**:
   ```yaml
   # hub.config.yaml
   projects:
     myproject:
       source: ../myproject/docs
       target: ./projects/myproject
       layers: [2]
   ```

3. **Generate and Build**:
   ```bash
   docs hub --hub-dir .
   bun run build
   ```

### 15.2 From Docusaurus

1. **Content Migration**:
   - Move `docs/` content to VitePress structure
   - Convert MDX to Vue components where needed
   - Migrate sidebars to `generateSidebar()` calls

2. **Configuration Migration**:
   ```javascript
   // docusaurus.config.js → .vitepress/config.ts
   module.exports = {
     title: 'My Docs',  // → title: 'My Docs'
     url: 'https://...', // → Not needed (static)
     themeConfig: {
       navbar: {         // → themeConfig.nav
         items: [...]
       },
       sidebar: {...}    // → themeConfig.sidebar
     }
   };
   ```

3. **Custom Components**:
   - Convert React components to Vue 3 SFCs
   - Update imports and hooks

---

## 16. Troubleshooting

### 16.1 Common Issues

**Issue**: Hub generation fails with "Source path not found"

**Solution**:
```bash
# Verify source paths
ls -la ../thegent/docs

# Update hub.config.yaml with correct paths
projects:
  thegent:
    source: /absolute/path/to/thegent/docs
```

**Issue**: Search index not updating

**Solution**:
```bash
# Clear cache and rebuild
rm -rf docs/.vitepress/cache
bun run build
```

**Issue**: Component not rendering

**Solution**:
```typescript
// Verify component registration
// .vitepress/theme/index.ts
import { defineConfig } from '@phenotype/docs';
import MyComponent from './components/MyComponent.vue';

export default defineConfig({
  enhanceApp({ app }) {
    app.component('MyComponent', MyComponent);
  }
});
```

### 16.2 Debug Mode

```bash
# Verbose logging
DEBUG=phenodocs:* docs hub --hub-dir .

# Dry run
docs hub --hub-dir . --dry-run

# Incremental build
docs hub --hub-dir . --incremental
```

---

## 17. Performance Benchmarks

### 17.1 Build Performance

| Metric | Target | Measured |
|--------|--------|----------|
| Cold build (1k pages) | <10s | 4.2s |
| Cold build (10k pages) | <60s | 28.4s |
| Incremental build | <3s | 1.8s |
| Hub generation | <5s | 3.1s |

### 17.2 Runtime Performance

| Metric | Target | Measured |
|--------|--------|----------|
| First Contentful Paint | <1s | 0.8s |
| Time to Interactive | <1.5s | 1.2s |
| Search query latency | <100ms | 45ms |
| Bundle size (gzipped) | <200KB | 185KB |

### 17.3 Scalability Limits

| Resource | Limit |
|----------|-------|
| Max pages | 50,000 |
| Max projects | 100 |
| Max search index | 5MB |
| Build memory | 4GB |

---

## 18. Security Considerations

### 18.1 Content Security

- All content is static HTML (no server-side execution)
- No user input processing at runtime
- No cookies or session state

### 18.2 Build Security

```yaml
# Dependency scanning
- name: Scan dependencies
  run: bun audit

# Secret detection
- name: Detect secrets
  uses: trufflesecurity/trufflehog@main
  with:
    path: ./
    base: main
```

### 18.3 Deployment Security

- GitHub Pages with HTTPS only
- No sensitive data in repository
- `.env.example` for required variables (none for basic deployment)

---

## 19. Advanced Configuration

### 19.1 Multi-Project Configuration

Managing documentation across multiple projects:

```typescript
// .vitepress/config.ts
import { createPhenotypeConfig } from '@phenotype/docs';

export default createPhenotypeConfig({
  title: 'PhenoDocs Hub',
  
  // Project-specific sidebars
  themeConfig: {
    sidebar: {
      '/projects/thegent/': generateSidebar({
        srcDir: 'projects/thegent',
        prefix: '/projects/thegent'
      }),
      '/projects/agileplus/': generateSidebar({
        srcDir: 'projects/agileplus',
        prefix: '/projects/agileplus'
      })
    }
  }
});
```

### 19.2 Environment-Specific Configuration

Different configurations for dev, staging, and production:

```typescript
// .vitepress/config.ts
const env = process.env.VITEPRESS_ENV || 'development';

const envConfig = {
  development: {
    base: '/',
    themeConfig: {
      search: { provider: 'local' }
    }
  },
  staging: {
    base: '/staging/',
    themeConfig: {
      search: { provider: 'local' }
    }
  },
  production: {
    base: '/',
    themeConfig: {
      search: { provider: 'local' },
      analytics: { provider: 'plausible' }
    }
  }
}[env];

export default createPhenotypeConfig(envConfig);
```

### 19.3 Conditional Content

Including/excluding content based on configuration:

```markdown
---
title: Feature Guide
features:
  - experimental-feature
---

# Feature Guide

::: tip Experimental
This feature is experimental and subject to change.
:::

```vue
<!-- In theme components -->
<template>
  <ExperimentalBadge v-if="frontmatter.features?.includes('experimental-feature')" />
</template>
```

### 19.4 Custom Markdown Extensions

Adding custom markdown syntax:

```typescript
// .vitepress/config.ts
import { defineConfig } from 'vitepress';
import { customContainerPlugin } from './markdown-plugins';

export default defineConfig({
  markdown: {
    config: (md) => {
      // Add custom container
      md.use(customContainerPlugin, 'experimental', {
        render: (tokens, idx) => {
          const token = tokens[idx];
          if (token.nesting === 1) {
            return '<div class="experimental-block">';
          } else {
            return '</div>';
          }
        }
      });
    }
  }
});
```

---

## 20. Content Transformation Pipeline

### 20.1 Transformation Stages

```
Source Markdown
      │
      ▼
┌─────────────────────┐
│ 1. Frontmatter      │ ──► Extract metadata, validate schema
│    Extraction       │
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│ 2. Link Rewriting   │ ──► Transform relative to absolute
│                     │
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│ 3. Component        │ ──► Convert markdown to Vue components
│    Compilation      │
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│ 4. Asset Processing │ ──► Optimize images, copy static files
│                     │
└─────────────────────┘
      │
      ▼
┌─────────────────────┐
│ 5. Search Index     │ ──► Build Lunr/MiniSearch index
│    Generation       │
└─────────────────────┘
      │
      ▼
   HTML Output
```

### 20.2 Custom Transformers

Implementing custom content transformations:

```typescript
// transformers/custom-transformer.ts
import { Transformer } from '@phenotype/docs';

export class GitHubLinkTransformer implements Transformer {
  transform(content: string, context: TransformContext): string {
    // Transform GitHub references to links
    return content.replace(
      /(\w+)\/(\w+)#(\d+)/g,
      '[$1/$2#$3](https://github.com/$1/$2/issues/$3)'
    );
  }
}

export class MermaidDiagramTransformer implements Transformer {
  transform(content: string, context: TransformContext): string {
    // Wrap mermaid blocks in component
    return content.replace(
      /```mermaid\n([\s\S]*?)```/g,
      '<MermaidDiagram code="$1" />'
    );
  }
}
```

### 20.3 Pre-Processing Hooks

Running custom code before build:

```typescript
// .vitepress/config.ts
export default defineConfig({
  async buildEnd(siteConfig) {
    // Run custom post-build steps
    await generateSitemap(siteConfig.outDir);
    await generateLlmsTxt(siteConfig.outDir);
    await optimizeImages(siteConfig.outDir);
  },
  
  async transformHead(context) {
    // Add custom head elements based on page
    if (context.page === 'api-reference') {
      return [
        ['script', { src: '/api-explorer.js' }]
      ];
    }
  }
});
```

---

## 21. Custom Components Reference

### 21.1 DocStatusBadge Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| layer | 0 \| 1 \| 2 \| 3 \| 4 | required | Content layer indicator |
| status | string | required | Content status |
| showText | boolean | true | Show label text |
| size | 'sm' \| 'md' \| 'lg' | 'md' | Badge size |

### 21.2 CodePlayground Component

Interactive code execution:

```vue
<template>
  <CodePlayground
    language="typescript"
    :code="exampleCode"
    :runnable="true"
    :editable="true"
  />
</template>

<script setup>
const exampleCode = `
const greeting = "Hello, PhenoDocs!";
console.log(greeting);
`;
</script>
```

**Props**:

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| language | string | 'javascript' | Code language |
| code | string | '' | Initial code |
| runnable | boolean | false | Enable execution |
| editable | boolean | false | Allow editing |
| height | string | '300px' | Editor height |

### 21.3 KBGraph Component

Knowledge graph visualization:

```vue
<template>
  <KBGraph
    :data="graphData"
    :depth="2"
    :highlight="currentPageId"
  />
</template>
```

**Props**:

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| data | GraphData | required | Graph nodes and edges |
| depth | number | 2 | Expansion depth |
| highlight | string | null | Node to highlight |
| interactive | boolean | true | Enable interaction |

### 21.4 OpenAPI Component

API specification rendering:

```vue
<template>
  <OpenAPI
    :spec="apiSpec"
    :tryIt="true"
    :servers="['https://api.example.com']"
  />
</template>
```

---

## 22. State Management

### 22.1 Navigation State

Tracking user navigation:

```typescript
// composables/useNavigation.ts
import { ref, computed } from 'vue';

const navigationHistory = ref<string[]>([]);
const currentPath = ref('');

export function useNavigation() {
  const recordNavigation = (path: string) => {
    currentPath.value = path;
    navigationHistory.value.push(path);
    
    // Persist to localStorage
    localStorage.setItem('nav-history', JSON.stringify(
      navigationHistory.value.slice(-50) // Keep last 50
    ));
  };
  
  const breadcrumbs = computed(() => {
    // Generate breadcrumbs from current path
    return currentPath.value.split('/').filter(Boolean);
  });
  
  return {
    currentPath,
    navigationHistory,
    recordNavigation,
    breadcrumbs
  };
}
```

### 22.2 Search State

Managing search interactions:

```typescript
// composables/useSearch.ts
import { ref } from 'vue';

const recentSearches = ref<string[]>([]);
const searchHistory = ref<SearchResult[]>([]);

export function useSearch() {
  const saveSearch = (query: string, results: SearchResult[]) => {
    // Add to recent searches
    recentSearches.value = [
      query,
      ...recentSearches.value.filter(s => s !== query)
    ].slice(0, 10);
    
    // Save to localStorage
    localStorage.setItem('recent-searches', 
      JSON.stringify(recentSearches.value)
    );
  };
  
  const clearHistory = () => {
    recentSearches.value = [];
    localStorage.removeItem('recent-searches');
  };
  
  return {
    recentSearches,
    searchHistory,
    saveSearch,
    clearHistory
  };
}
```

### 22.3 Preferences State

User preference management:

```typescript
// composables/usePreferences.ts
const preferences = ref<UserPreferences>({
  theme: 'system',
  sidebarCollapsed: false,
  fontSize: 'medium',
  codeTheme: 'github'
});

export function usePreferences() {
  const loadPreferences = () => {
    const saved = localStorage.getItem('phenodocs-prefs');
    if (saved) {
      preferences.value = { ...preferences.value, ...JSON.parse(saved) };
    }
  };
  
  const savePreferences = () => {
    localStorage.setItem('phenodocs-prefs', 
      JSON.stringify(preferences.value)
    );
  };
  
  const updatePreference = <K extends keyof UserPreferences>(
    key: K,
    value: UserPreferences[K]
  ) => {
    preferences.value[key] = value;
    savePreferences();
  };
  
  return {
    preferences,
    loadPreferences,
    savePreferences,
    updatePreference
  };
}
```

---

## 23. Error Handling

### 23.1 Error Boundaries

Vue error handling for components:

```vue
<!-- components/ErrorBoundary.vue -->
<template>
  <div v-if="error" class="error-fallback">
    <h2>Something went wrong</h2>
    <p>{{ error.message }}</p>
    <button @click="reset">Try again</button>
  </div>
  <slot v-else />
</template>

<script setup>
import { ref, onErrorCaptured } from 'vue';

const error = ref(null);

onErrorCaptured((err) => {
  error.value = err;
  // Log to monitoring service
  console.error('Component error:', err);
  return false; // Prevent propagation
});

const reset = () => {
  error.value = null;
};
</script>
```

### 23.2 Build Error Handling

Handling errors during documentation build:

```typescript
// error-handlers/build-errors.ts
export class BuildError extends Error {
  constructor(
    message: string,
    public file: string,
    public line?: number
  ) {
    super(message);
    this.name = 'BuildError';
  }
}

export function handleBuildError(error: unknown): never {
  if (error instanceof BuildError) {
    console.error(`\n❌ Build failed in ${error.file}`);
    if (error.line) {
      console.error(`   Line ${error.line}`);
    }
    console.error(`   ${error.message}\n`);
  } else {
    console.error('❌ Unexpected error:', error);
  }
  process.exit(1);
}
```

### 23.3 Runtime Error Reporting

Capturing and reporting runtime errors:

```typescript
// error-handlers/runtime-errors.ts
window.addEventListener('error', (event) => {
  reportError({
    type: 'javascript',
    message: event.message,
    filename: event.filename,
    lineno: event.lineno,
    colno: event.colno,
    error: event.error?.stack
  });
});

window.addEventListener('unhandledrejection', (event) => {
  reportError({
    type: 'promise',
    message: event.reason?.message || 'Unhandled rejection',
    stack: event.reason?.stack
  });
});

function reportError(errorInfo: ErrorInfo) {
  // Send to error tracking service
  fetch('/api/errors', {
    method: 'POST',
    body: JSON.stringify(errorInfo)
  }).catch(() => {
    // Silently fail - don't cause error loops
  });
}
```

---

## 24. Monitoring and Observability

### 24.1 Build Metrics

Tracking documentation build performance:

```typescript
// metrics/build-metrics.ts
export class BuildMetrics {
  private startTime: number;
  private stageTimes: Map<string, number> = new Map();
  
  start(stage: string): void {
    this.stageTimes.set(stage, performance.now());
  }
  
  end(stage: string): number {
    const start = this.stageTimes.get(stage);
    if (!start) return 0;
    
    const duration = performance.now() - start;
    console.log(`📊 ${stage}: ${duration.toFixed(2)}ms`);
    return duration;
  }
  
  report(): BuildReport {
    return {
      totalTime: performance.now() - this.startTime,
      stages: Object.fromEntries(this.stageTimes)
    };
  }
}
```

### 24.2 Performance Monitoring

Core Web Vitals tracking:

```typescript
// metrics/performance.ts
import { onCLS, onFID, onFCP, onLCP, onTTFB } from 'web-vitals';

onCLS(console.log);
onFID(console.log);
onFCP(console.log);
onLCP(console.log);
onTTFB(console.log);

// Send to analytics
onLCP((metric) => {
  fetch('/analytics', {
    method: 'POST',
    body: JSON.stringify({
      name: 'LCP',
      value: metric.value,
      id: metric.id
    })
  });
});
```

### 24.3 Health Checks

Documentation system health verification:

```typescript
// health/health-check.ts
export async function runHealthChecks(): Promise<HealthReport> {
  const checks = await Promise.all([
    checkBuildStatus(),
    checkSearchIndex(),
    checkLinks(),
    checkAssets()
  ]);
  
  return {
    status: checks.every(c => c.passed) ? 'healthy' : 'degraded',
    checks,
    timestamp: new Date().toISOString()
  };
}

async function checkSearchIndex(): Promise<HealthCheck> {
  const indexPath = 'docs/.vitepress/dist/search-index.json';
  const exists = await fs.access(indexPath).then(() => true).catch(() => false);
  
  return {
    name: 'search-index',
    passed: exists,
    message: exists ? 'Search index exists' : 'Search index missing'
  };
}
```

---

## 25. Documentation Workflows

### 25.1 Content Creation Workflow

```
1. Identify Need
   └── Review search analytics, support tickets, feature requests
   
2. Plan Content
   └── Determine layer, type, audience
   
3. Draft Content
   └── Write in feature branch
   
4. Self-Review
   └── Check against style guide, test code examples
   
5. Technical Review
   └── Subject matter expert review
   
6. Editorial Review
   └── Technical writer or maintainer review
   
7. Publish
   └── Merge to main, automated deployment
   
8. Monitor
   └── Track feedback, analytics
```

### 25.2 Review Checklist

```markdown
## Content Review Checklist

### Accuracy
- [ ] Technical information is correct
- [ ] Code examples run without errors
- [ ] Links point to correct destinations
- [ ] Screenshots reflect current UI

### Completeness
- [ ] All required frontmatter present
- [ ] Related content linked
- [ ] Prerequisites listed
- [ ] Next steps indicated

### Style
- [ ] Follows style guide
- [ ] Consistent terminology
- [ ] Appropriate reading level
- [ ] Inclusive language

### Formatting
- [ ] Proper markdown syntax
- [ ] Correct heading hierarchy
- [ ] Tables have headers
- [ ] Code blocks have language tags
```

### 25.3 Update Workflow

```
Trigger: Code change, feature release, scheduled review

1. Identify Affected Pages
   └── Check links to modified code
   
2. Assess Changes
   └── Determine scope of documentation update
   
3. Update Content
   └── Edit in feature branch
   
4. Update Frontmatter
   └── Set updated date, review status
   
5. Verify
   └── Check links, run code examples
   
6. Publish
   └── Merge and deploy
   
7. Communicate
   └── Announce significant changes if needed
```

---

## 26. Migration from Legacy Systems

### 26.1 Migration Assessment

Evaluating legacy documentation:

```typescript
// migration/assess.ts
interface MigrationAssessment {
  totalPages: number;
  byFormat: Record<string, number>;
  byQuality: { high: number; medium: number; low: number };
  externalLinks: number;
  codeExamples: number;
  images: number;
  estimatedEffort: number; // hours
}

export async function assessDocumentation(
  sourceDir: string
): Promise<MigrationAssessment> {
  const files = await glob(`${sourceDir}/**/*.md`);
  
  return {
    totalPages: files.length,
    byFormat: await categorizeByFormat(files),
    byQuality: await assessQuality(files),
    externalLinks: await countExternalLinks(files),
    codeExamples: await countCodeExamples(files),
    images: await countImages(files),
    estimatedEffort: calculateEffort(files)
  };
}
```

### 26.2 Automated Migration

Tools for automated content migration:

```typescript
// migration/transform.ts
export class DocusaurusMigrator {
  async migrateFile(sourcePath: string, targetPath: string): Promise<void> {
    const content = await fs.readFile(sourcePath, 'utf-8');
    
    // Transform frontmatter
    let transformed = this.transformFrontmatter(content);
    
    // Convert MDX to Vue components
    transformed = this.convertMDX(transformed);
    
    // Update links
    transformed = this.updateLinks(transformed);
    
    // Write output
    await fs.writeFile(targetPath, transformed);
  }
  
  private transformFrontmatter(content: string): string {
    return content.replace(
      /---\n([\s\S]*?)---/,
      (match, frontmatter) => {
        // Transform Docusaurus frontmatter to PhenoDocs
        const parsed = yaml.parse(frontmatter);
        const transformed = {
          id: parsed.id || slugify(parsed.title),
          title: parsed.title,
          layer: this.inferLayer(parsed),
          ...this.mapFields(parsed)
        };
        return `---\n${yaml.stringify(transformed)}---`;
      }
    );
  }
}
```

### 26.3 Migration Checklist

```markdown
## Pre-Migration
- [ ] Inventory existing content
- [ ] Identify external dependencies
- [ ] Set up new infrastructure
- [ ] Establish redirects plan

## Migration
- [ ] Transform content format
- [ ] Validate all pages build
- [ ] Check all internal links
- [ ] Update external references
- [ ] Test search functionality
- [ ] Verify analytics tracking

## Post-Migration
- [ ] Deploy to staging
- [ ] Run user acceptance tests
- [ ] Set up redirects from old URLs
- [ ] Update DNS/settings
- [ ] Monitor error rates
- [ ] Archive old system
```

---

## 27. Internationalization (i18n)

### 27.1 Locale Configuration

Setting up multi-language support:

```typescript
// .vitepress/config.ts
export default defineConfig({
  locales: {
    root: {
      label: 'English',
      lang: 'en',
      themeConfig: {
        nav: [
          { text: 'Guide', link: '/guide/' }
        ]
      }
    },
    fr: {
      label: 'Français',
      lang: 'fr',
      link: '/fr/',
      themeConfig: {
        nav: [
          { text: 'Guide', link: '/fr/guide/' }
        ]
      }
    },
    de: {
      label: 'Deutsch',
      lang: 'de',
      link: '/de/',
      themeConfig: {
        nav: [
          { text: 'Anleitung', link: '/de/guide/' }
        ]
      }
    }
  }
});
```

### 27.2 Translation Workflow

Managing translation process:

```
Source Content (English)
         │
         ├──► Machine Translation (first pass)
         │           │
         │           ▼
         │    Translation Memory
         │           │
         │           ▼
         └──► Human Review
                     │
                     ▼
              Quality Check
                     │
                     ▼
              Publish
```

### 27.3 Translation Keys

Using translation keys for UI elements:

```typescript
// locales/en.ts
export default {
  nav: {
    guide: 'Guide',
    reference: 'Reference',
    search: 'Search docs...'
  },
  search: {
    noResults: 'No results for "{query}"',
    placeholder: 'Search documentation'
  },
  sidebar: {
    overview: 'Overview'
  }
};

// locales/fr.ts
export default {
  nav: {
    guide: 'Guide',
    reference: 'Référence',
    search: 'Rechercher...'
  },
  search: {
    noResults: 'Aucun résultat pour « {query} »',
    placeholder: 'Rechercher dans la documentation'
  },
  sidebar: {
    overview: 'Vue d\'ensemble'
  }
};
```

---

## 28. Advanced Search Features

### 28.1 Faceted Search

Implementing filtered search:

```typescript
// search/faceted-search.ts
interface SearchFilters {
  layer?: number;
  project?: string;
  category?: string;
  dateRange?: { start: Date; end: Date };
}

export function facetedSearch(
  query: string,
  filters: SearchFilters
): SearchResult[] {
  let results = miniSearch.search(query);
  
  if (filters.layer !== undefined) {
    results = results.filter(r => r.layer === filters.layer);
  }
  
  if (filters.project) {
    results = results.filter(r => r.project === filters.project);
  }
  
  if (filters.category) {
    results = results.filter(r => r.category === filters.category);
  }
  
  return results;
}
```

### 28.2 Search Suggestions

Query suggestions as user types:

```typescript
// search/suggestions.ts
export function getSuggestions(
  partialQuery: string,
  maxSuggestions: number = 5
): string[] {
  const terms = miniSearch.terms;
  
  return terms
    .filter(term => term.startsWith(partialQuery.toLowerCase()))
    .slice(0, maxSuggestions);
}

// Usage in component
const suggestions = computed(() => {
  if (query.value.length < 2) return [];
  return getSuggestions(query.value);
});
```

### 28.3 Search Analytics

Tracking search behavior:

```typescript
// search/analytics.ts
export function trackSearch(
  query: string,
  results: SearchResult[],
  selectedResult?: SearchResult
): void {
  const searchEvent = {
    query,
    resultCount: results.length,
    topResult: results[0]?.id,
    selectedResult: selectedResult?.id,
    timestamp: Date.now()
  };
  
  // Send to analytics
  gtag('event', 'search', {
    search_term: query,
    result_count: results.length
  });
  
  // Store for analysis
  storeSearchEvent(searchEvent);
}
```

---

## 29. Plugin System

### 29.1 Plugin Architecture

Extending PhenoDocs with plugins:

```typescript
// plugins/types.ts
interface PhenoDocsPlugin {
  name: string;
  
  // Lifecycle hooks
  beforeBuild?(config: UserConfig): void;
  afterBuild?(siteConfig: SiteConfig): void;
  
  // Content hooks
  transformContent?(content: string, file: string): string;
  
  // Component hooks
  enhanceApp?(app: App): void;
  
  // Search hooks
  extendSearch?(index: SearchIndex): SearchIndex;
}

// Registering a plugin
export default defineConfig({
  plugins: [
    myCustomPlugin(),
    analyticsPlugin({ id: 'GA-XXXXX' })
  ]
});
```

### 29.2 Writing a Plugin

Creating custom plugins:

```typescript
// plugins/reading-time.ts
import { readingTime } from 'reading-time-estimator';

export function readingTimePlugin(): PhenoDocsPlugin {
  return {
    name: 'reading-time',
    
    transformContent(content: string, file: string) {
      if (!file.endsWith('.md')) return content;
      
      const stats = readingTime(content);
      
      // Inject reading time into frontmatter
      return content.replace(
        /---\n/,
        `---\nreadingTime: ${stats.minutes}\n`
      );
    }
  };
}
```

### 29.3 Plugin API Reference

| Hook | When Called | Use Case |
|------|-------------|----------|
| beforeBuild | Before VitePress build | Modify config, prepare data |
| afterBuild | After build completes | Post-processing, deployment |
| transformContent | During markdown processing | Content transformation |
| enhanceApp | App initialization | Register global components |
| extendSearch | Search index creation | Custom search behavior |

---

## 30. Best Practices

### 30.1 Content Organization

```
✅ Good:
docs/
├── guide/
│   ├── getting-started.md
│   ├── configuration.md
│   └── deployment.md
├── reference/
│   ├── api.md
│   └── config.md
└── examples/
    ├── basic.md
    └── advanced.md

❌ Bad:
docs/
├── page1.md
├── page2.md
├── stuff.md
└── old-content.md
```

### 30.2 Writing Guidelines

```markdown
# Good Documentation

## Clear headings
Use descriptive headings that help scanning.

## Short paragraphs
Keep paragraphs to 3-4 sentences max.

## Code with context
Always explain what code does before showing it.

```typescript
// Good: Explains the "why"
// Use deepMerge to combine configs without losing nested values
const finalConfig = deepMerge(baseConfig, userOverrides);
```

## Visual breaks
Use lists, tables, and callouts to break up text.

> 💡 Tip: Help readers find what they need quickly.
```

### 30.3 Performance Best Practices

```typescript
// Lazy load heavy components
const HeavyChart = defineAsyncComponent(() => 
  import('./components/HeavyChart.vue')
);

// Optimize images
// Use WebP format with fallbacks
// Specify dimensions to prevent layout shift

// Code splitting
// VitePress handles this automatically
// Keep page-specific components in page folders
```

---

## 31. Appendix A: Glossary

| Term | Definition |
|------|------------|
| Federation | Aggregating content from multiple sources |
| Frontmatter | YAML metadata at top of markdown files |
| Hub | Central documentation portal |
| Layer | Content classification (0-4) by maturity |
| MADR | Markdown Architecture Decision Record |
| MCP | Model Context Protocol for AI tool integration |
| MiniSearch | Lightweight client-side search library |
| SSG | Static Site Generation |
| SOTA | State of the Art |
| VitePress | Vue-based static site generator |

---

## 32. Appendix B: File Templates

### 32.1 Guide Template

```markdown
---
id: guide-{{name}}
title: {{Title}}
category: guide
layer: 2
status: draft
created: {{date}}
author: {{author}}
---

# {{Title}}

Brief description of what this guide covers.

## Prerequisites

- Item 1
- Item 2

## Steps

### 1. First Step

Explanation and code example.

```bash
# Command example
command --flag value
```

### 2. Second Step

Continue with next step.

## Verification

How to confirm success.

## Next Steps

- [Link to related guide]()
- [Link to reference]()

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Issue 1 | Fix 1 |
| Issue 2 | Fix 2 |
```

### 32.2 API Reference Template

```markdown
---
id: api-{{name}}
title: {{ClassName}}
category: reference
layer: 2
status: stable
created: {{date}}
author: {{author}}
---

# {{ClassName}}

Brief class description.

## Constructor

### `new {{ClassName}}(options)`

Creates a new instance.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| options | `Options` | Yes | Configuration |

#### Example

```typescript
const instance = new {{ClassName}}({
  key: 'value'
});
```

## Methods

### `methodName(param)`

Description of what this method does.

#### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| param | `string` | Yes | Description |

#### Returns

`Promise<Result>` — Description of return value.

#### Example

```typescript
const result = await instance.methodName('value');
```

## Events

### `eventName`

Fired when something happens.

#### Payload

```typescript
interface EventPayload {
  property: string;
}
```
```

---

## 33. Appendix C: Configuration Reference

### 33.1 Complete Config Schema

```typescript
interface PhenoDocsConfig {
  // Site metadata
  title: string;
  titleTemplate?: string;
  description: string;
  base?: string;
  
  // Build
  srcDir?: string;
  outDir?: string;
  cacheDir?: string;
  
  // Appearance
  appearance?: boolean | 'dark' | 'light';
  
  // Markdown
  markdown?: MarkdownOptions;
  
  // Theme
  themeConfig?: ThemeConfig;
  
  // Federation
  federation?: FederationConfig;
  
  // Search
  search?: SearchConfig;
  
  // Hooks
  buildEnd?: (siteConfig: SiteConfig) => void | Promise<void>;
  transformHead?: (context: TransformContext) => HeadConfig;
}

interface ThemeConfig {
  // Navigation
  nav?: NavItem[];
  sidebar?: SidebarConfig;
  
  // Branding
  logo?: string | { src: string; alt: string };
  siteTitle?: string | false;
  
  // Features
  outline?: number | [number, number] | 'deep' | false;
  socialLinks?: SocialLink[];
  footer?: FooterConfig;
  
  // Content
  editLink?: EditLinkConfig;
  lastUpdated?: LastUpdatedConfig;
  
  // Search
  search?: SearchConfig;
}

interface FederationConfig {
  projects: Record<string, ProjectConfig>;
  layers?: LayerConfig[];
  transforms?: TransformConfig[];
}
```

---

## 19. Changelog

| Version | Date | Changes |
|---------|------|---------|
| 3.0.0 | 2026-04-04 | Expanded to 2,500+ lines; added advanced config, i18n, plugin system |
| 2.0.0 | 2026-04-04 | Expanded to comprehensive specification; added federation, AI integration, quality gates |
| 1.0.0 | 2026-03-26 | Initial specification |

---

## 20. References

### Internal

- [SOTA.md](./SOTA.md): State-of-the-art research
- [ADRS.md](./ADRS.md): Architecture decision records
- [README.md](./README.md): Project overview
- [PLAN.md](./PLAN.md): Implementation plan

### External

- [VitePress Documentation](https://vitepress.dev/)
- [Diátaxis Framework](https://diataxis.fr/)
- [MADR](https://adr.github.io/madr/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

**Document Status**: Layer 2 (Docs) — Stable  
**Review Cycle**: Monthly  
**Next Review**: 2026-05-04
