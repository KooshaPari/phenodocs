// Edited 2026-05-30 (base-path fix):
//   Add PHENOTYPE_CUSTOM_DOMAIN env-var support. When set to "true" in a
//   consumer deploy workflow, base is forced to '/' regardless of GITHUB_PAGES,
//   preventing the /<repo>/ prefix from being baked into asset URLs for sites
//   served from a custom domain root. Consumers on github.io/<repo>/ should NOT
//   set this flag — they need the /<repo>/ base.
//
// Edited 2026-05-04 (frontend-engineer task):
//   Fix shared VitePress asset handling so favicon/logo do not 404 on
//   GitHub Pages deployments where `base` is `/<repo>/`.
//   Changes:
//     1. Normalize `base` to always end with `/` before composing asset URLs.
//     2. Switch favicon from `.ico` to `favicon.svg`.
//     3. `themeConfig.logo` is left as a root-relative path ('/logo.svg').
//     4. `head` entries ARE prefixed with normalized base.
import { defineConfig } from 'vitepress'
import type { ConfigOptions } from '../types/index.ts'
import { deepMerge } from '../utils/config-merger.ts'

/**
 * Create a VitePress config pre-loaded with the Phenotype keycap theme defaults.
 *
 * Consumers call this in their `.vitepress/config.mts`:
 * ```ts
 * import { createPhenotypeConfig } from '@phenotype/docs/config'
 * export default createPhenotypeConfig({ title: 'My Project', description: '...' })
 * ```
 */
export function createPhenotypeConfig(options: ConfigOptions) {
  const {
    title,
    description,
    base = '/',
    srcDir = 'docs',
    githubOrg = 'KooshaPari',
    githubRepo,
    nav = [],
    sidebar = {},
    overrides = {},
  } = options

  const repoSlug = githubRepo ?? title.toLowerCase().replace(/\s+/g, '-')

  // If PHENOTYPE_CUSTOM_DOMAIN is set (e.g. by a consumer deploy workflow that has
  // a CNAME / is served from a custom domain root), override base to '/'.
  // This prevents the /<repo>/ prefix being baked into every asset URL, which
  // causes blank/unstyled pages when assets 404 at the sub-path.
  const effectiveBase =
    process.env.PHENOTYPE_CUSTOM_DOMAIN === 'true' ? '/' : base

  // Normalize base: VitePress requires leading + trailing slash. Without trailing
  // slash, `${base}favicon.svg` produces a malformed URL (e.g. `/repofavicon.svg`).
  const normalizedBase = effectiveBase.endsWith('/') ? effectiveBase : `${effectiveBase}/`

  const baseConfig = defineConfig({
    title,
    description,
    lang: 'en-US',
    srcDir,
    base: normalizedBase,
    lastUpdated: true,
    cleanUrls: true,

    head: [
      // SVG favicon. Phenodocs ships placeholder at `docs/public/favicon.svg`
      // (VitePress resolves `public/` relative to `srcDir`, not repo root).
      // Each consumer must ship its own under `<srcDir>/public/` to override.
      ['link', { rel: 'icon', type: 'image/svg+xml', href: `${normalizedBase}favicon.svg` }],
      ['link', { rel: 'apple-touch-icon', href: `${normalizedBase}favicon.svg` }],
    ],

    themeConfig: {
      siteTitle: title,

      nav,

      sidebar,

      socialLinks: [
        { icon: 'github', link: `https://github.com/${githubOrg}/${repoSlug}` },
      ],

      footer: {
        message: 'Released under the MIT License.',
        copyright: `Copyright \u00a9 ${new Date().getFullYear()} Phenotype`,
      },

      search: {
        provider: 'local',
      },

      editLink: {
        pattern: `https://github.com/${githubOrg}/${repoSlug}/edit/main/${srcDir}/:path`,
        text: 'Edit this page on GitHub',
      },

      outline: {
        level: [2, 3],
        label: 'On this page',
      },

      externalLinkIcon: true,
    },

    markdown: {
      lineNumbers: true,
      theme: {
        light: 'github-light',
        dark: 'github-dark',
      },
    },

    ignoreDeadLinks: true,
  })

  // Deep-merge consumer overrides on top of base config
  return deepMerge(baseConfig, overrides) as ReturnType<typeof defineConfig>
}
