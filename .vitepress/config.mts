// Edited 2026-05-04 (frontend-engineer task):
//   Fix shared VitePress asset 404s on GitHub Pages.
//   Changes:
//     1. `themeConfig.logo` left as '/logo.svg' — VitePress automatically
//        prefixes themeConfig.logo with `base`, so DO NOT prepend `${base}`
//        manually (would produce `/phenodocs/phenodocs/logo.svg`).
//     2. Favicon is now wired via `createPhenotypeConfig`'s shared `head[]`
//        which prepends the normalized `base` for non-auto-prefixed entries.
//        Static assets (favicon.svg, logo.svg) live in `docs/public/` because
//        VitePress resolves `public/` relative to `srcDir: 'docs'`.
//     3. `docsBase` is normalized to always end with `/` — required by
//        VitePress for correct asset URL composition under GitHub Pages.
import { createPhenotypeConfig } from '../packages/docs/src/config/index.ts'

// Environment-based configuration for GitHub Pages compatibility.
// On Pages, repo lives at `/<repo>/`; locally and on a custom domain root, `/`.
const isPagesBuild = process.env.GITHUB_ACTIONS === 'true' || process.env.GITHUB_PAGES === 'true'
const repoName = process.env.GITHUB_REPOSITORY?.split('/')[1] || 'phenodocs'
const rawBase = isPagesBuild ? `/${repoName}/` : '/'
// Defensive: ensure leading + trailing slash even if repoName was malformed.
const docsBase = (rawBase.startsWith('/') ? rawBase : `/${rawBase}`).replace(/\/+$/, '/') || '/'

export default createPhenotypeConfig({
  title: 'PhenoDocs',
  description: 'Federation hub for multi-project documentation',
  lang: 'en-US',
  srcDir: 'docs',
  base: docsBase,
  githubOrg: 'KooshaPari',
  githubRepo: repoName,

  nav: [
    { text: 'Guide', link: '/guide/getting-started' },
    { text: 'Architecture', link: '/guide/architecture' },
    { text: 'Tutorials', link: '/tutorials/' },
    { text: 'API', link: '/reference/api' },
    { text: 'Governance', link: '/governance/overview' },
    { text: 'RFCs', link: '/rfcs/' },
    { text: 'Changelog', link: '/changelog/' },
    { text: 'Roadmap', link: '/roadmap/' },
    { text: 'Workspace views', link: '/views/' },
  ],

  themeConfig: {
    logo: '/logo.svg',
    siteTitle: 'PhenoDocs',

    nav: [
      { text: 'Guide', link: '/guide/getting-started' },
      { text: 'Architecture', link: '/guide/architecture' },
      { text: 'Tutorials', link: '/tutorials/' },
      { text: 'API', link: '/reference/api' },
      { text: 'Governance', link: '/governance/overview' },
      { text: 'RFCs', link: '/rfcs/' },
      { text: 'Changelog', link: '/changelog/' },
      { text: 'Roadmap', link: '/roadmap/' },
      { text: 'Workspace views', link: '/views/' }
    ],

    sidebar: {
      '/guide/': [
        {
          text: 'Getting Started',
          items: [
            { text: 'Introduction', link: '/guide/getting-started' },
            { text: 'Architecture', link: '/guide/architecture' },
            { text: 'Full-turn delivery', link: '/guides/full-turn-delivery' }
          ]
        }
      ],
      '/tutorials/': [
        {
          text: 'Tutorials',
          items: [
            { text: 'Index', link: '/tutorials/' },
            { text: '01 — First-time setup', link: '/tutorials/01-first-time-setup' },
            { text: '02 — Adding a project', link: '/tutorials/02-adding-a-project' },
            { text: '03 — Generating API reference', link: '/tutorials/03-generating-api-reference' },
            { text: '04 — Writing an RFC', link: '/tutorials/04-writing-an-rfc' },
            { text: '05 — Cutting a release', link: '/tutorials/05-cutting-a-release' }
          ]
        }
      ],
      '/reference/': [
        {
          text: 'Reference',
          items: [
            { text: 'API', link: '/reference/api' },
            { text: 'OpenAPI index', link: '/api/openapi/' }
          ]
        }
      ],
      '/api/': [
        {
          text: 'API',
          items: [
            { text: 'Index', link: '/api/' },
            { text: 'OpenAPI reference', link: '/api/openapi/' }
          ]
        }
      ],
      '/rfcs/': [
        {
          text: 'RFCs',
          items: [
            { text: 'Index', link: '/rfcs/' },
            { text: 'Template', link: '/rfcs/template' }
          ]
        }
      ],
      '/changelog/': [
        {
          text: 'Changelog',
          items: [
            { text: 'Releases', link: '/changelog/' }
          ]
        }
      ],
      '/governance/': [
        {
          text: 'Governance',
          items: [
            { text: 'Overview', link: '/governance/overview' },
            { text: 'VitePress unification', link: '/governance/vitepress-unification' },
            { text: 'RFC flow', link: '/governance/rfc-flow' },
            { text: 'Stacked PRs', link: '/governance/stacked-prs/' }
          ]
        }
      ],
      '/templates/': [
        {
          text: 'Templates',
          items: [
            { text: 'Release Matrix Template', link: '/templates/release-matrix-template' }
          ]
        }
      ],
      '/roadmap/': [
        {
          text: 'Roadmap',
          items: [
            { text: 'Overview', link: '/roadmap/' }
          ]
        }
      ],
      '/planning/': [
        {
          text: 'Planning',
          items: [
            { text: 'Rich workspace views', link: '/planning/rich-workspace-views' },
            { text: 'Full-turn Next 24', link: '/planning/full-turn-next24-20260326' }
          ]
        }
      ],
      '/views/': [
        {
          text: 'Workspace views',
          items: [
            { text: 'Overview', link: '/views/' },
            { text: 'Changelog (rich)', link: '/views/changelog' },
            { text: 'Commit log', link: '/views/commits' },
            { text: 'WBS & DAG', link: '/views/wbs' }
          ]
        }
      ]
    },

    socialLinks: [
      { icon: 'github', link: `https://github.com/kooshapari/${repoName}` }
    ],

    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2024 Kush Team'
    },

    search: {
      provider: 'local'
    },

    editLink: {
      pattern: `https://github.com/kooshapari/${repoName}/edit/main/docs/:path`,
      text: 'Edit this page on GitHub'
    },

    outline: {
      level: [2, 3],
      label: 'On this page'
    },

    externalLinkIcon: true,
    breadcrumb: true
  },

  overrides: {
    themeConfig: {
      logo: '/logo.svg',
      breadcrumb: true,
    },
    markdown: {
      anchorLinks: true,
    },
  },
})
