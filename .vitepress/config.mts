import { defineConfig } from 'vitepress'

// Environment-based configuration for GitHub Pages compatibility
const isPagesBuild = process.env.GITHUB_ACTIONS === 'true' || process.env.GITHUB_PAGES === 'true'
const repoName = process.env.GITHUB_REPOSITORY?.split('/')[1] || 'phenodocs'
const docsBase = isPagesBuild ? `/${repoName}/` : '/'

export default defineConfig({
  title: 'PhenoDocs',
  description: 'Federation hub for multi-project documentation',
  lang: 'en-US',
  srcDir: 'docs',
  base: docsBase,
  lastUpdated: true,
  cleanUrls: true,

  head: [
    ['link', { rel: 'icon', href: `${docsBase}favicon.ico` }],
  ],

  themeConfig: {
    logo: '/logo.svg',
    siteTitle: 'PhenoDocs',

    nav: [
      { text: 'Guide', link: '/guide/getting-started' },
      { text: 'Architecture', link: '/guide/architecture' },
      { text: 'API', link: '/reference/api' },
      { text: 'Governance', link: '/governance/overview' },
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
            { text: 'Full-turn delivery', link: '/guides/full-turn-delivery' },
            { text: 'Toolchains (Bun, uv)', link: '/guides/tooling' }
          ]
        }
      ],
      '/reference/': [
        {
          text: 'Reference',
          items: [
            { text: 'API', link: '/reference/api' }
          ]
        }
      ],
      '/governance/': [
        {
          text: 'Governance',
          items: [
            { text: 'Overview', link: '/governance/overview' },
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
            { text: 'Full-turn Next 50 (DAG)', link: '/planning/full-turn-next50-20260326' },
            { text: 'Full-turn Next 24 (legacy)', link: '/planning/full-turn-next24-20260326' }
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
      { icon: 'github', link: `https://github.com/KooshaPari/${repoName}` }
    ],

    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2024 Kush Team'
    },

    search: {
      provider: 'local'
    },

    editLink: {
      pattern: `https://github.com/KooshaPari/${repoName}/edit/main/docs/:path`,
      text: 'Edit this page on GitHub'
    },

    outline: {
      level: [2, 3],
      label: 'On this page'
    },

    externalLinkIcon: true,
    breadcrumb: true
  },

  markdown: {
    lineNumbers: true,
    theme: {
      light: 'github-light',
      dark: 'github-dark'
    },
    anchorLinks: true
  },
  ignoreDeadLinks: true
})
