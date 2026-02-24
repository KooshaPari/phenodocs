import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'PhenoDocs',
  description: 'Federation hub for multi-project documentation',
  lang: 'en-US',
  lastUpdated: true,
  cleanUrls: true,

  themeConfig: {
    logo: '/logo.svg',
    siteTitle: 'PhenoDocs',

    nav: [
      { text: 'Guide', link: '/guide/getting-started' },
      { text: 'Architecture', link: '/guide/architecture' },
      { text: 'API', link: '/reference/api' },
      { text: 'Governance', link: '/governance/overview' }
    ],

    sidebar: {
      '/guide/': [
        {
          text: 'Getting Started',
          items: [
            { text: 'Introduction', link: '/guide/getting-started' },
            { text: 'Architecture', link: '/guide/architecture' }
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
            { text: 'Overview', link: '/governance/overview' }
          ]
        }
      ]
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/yourorg/phenodocs' }
    ],

    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2024 Kush Team'
    },

    search: {
      provider: 'local'
    },

    editLink: {
      pattern: 'https://github.com/yourorg/phenodocs/edit/main/docs/:path',
      text: 'Edit this page on GitHub'
    }
  },

  markdown: {
    lineNumbers: true,
    theme: {
      light: 'github-light',
      dark: 'github-dark'
    }
  }
})
