# AGENTS.md — gustavosalvini-astro-blog

## Stack

- Astro 6 static blog, forked from `satnaing/astro-paper`
- TypeScript (strict), Tailwind CSS v4 (Vite plugin), pnpm 10.9
- ESLint 9 flat config, Prettier 3, Playwright for e2e
- Commitizen (conventional commits) — use `pnpm commit`

## Commands

| Command             | What it does                                                                                                                    |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `pnpm dev`          | Dev server on :4321                                                                                                             |
| `pnpm build`        | `playwright install chromium` → `astro check` → `astro build` → `pagefind --site dist` → `cp -r dist/pagefind public/`          |
| `pnpm preview`      | Preview `dist/`                                                                                                                 |
| `pnpm sync`         | Generate `.astro/types.d.ts`                                                                                                    |
| `pnpm format:check` | Prettier check                                                                                                                  |
| `pnpm format`       | Prettier write                                                                                                                  |
| `pnpm lint`         | ESLint                                                                                                                          |
| `pnpm commit`       | Commitizen prompt                                                                                                               |

No standalone `typecheck` script — `astro check` is embedded in `build`.

## Architecture

- **Blog posts**: `src/data/blog/**/[^_]*.md` (collections schema: `src/content.config.ts`)
  - Files starting with `_` are excluded (subdirs like `_releases/` are for Front Matter CMS only)
  - Draft posts: `draft: true` in frontmatter
- **Content loader**: glob pattern `**/[^_]*{.md,.mdx}` (supports both md and mdx)
- **Site config**: `src/config.ts` → `SITE` (as const)
- **Social/share links**: `src/constants.ts`
- **Path alias**: `@/*` → `./src/*`
- **Integrations**: MDX, Sitemap (filters `/archives` based on `SITE.showArchives`)
- **Markdown plugins**: remark-math, remark-toc, remark-collapse ("Table of contents")
- **Rehype plugins**: rehype-targetBlank (custom, domain: gustavosalvini.com.ar), rehype-katex, rehype-mermaid (img-svg, dark, forest), rehype-modifyMermaidGraphs (custom)
- **Syntax highlighting**: Shiki (min-light/dark-plus), excludes mermaid & math
- **OG images**: Dynamic via Satori (`src/pages/og.png.ts`)

## Gotchas

- **Build copies pagefind to `public/`**: After `astro build`, pagefind runs on `dist/` then result is copied to `public/pagefind`. This means pagefind files in `public/pagefind` are gitignored but served locally in dev.
- **Prettier ignore uses whitelist**: `.prettierignore` ignores `/*` then whitelists `!/src`, `!/public`, etc. Adding new dirs that need formatting requires updating this file.
- **Playwright web server not configured**: The Playwright config has no `webServer` — you must start `pnpm dev` manually before running `pnpm exec playwright test`.
- **`@resvg/resvg-js` is excluded from Vite opt deps** (native addon workaround).
- **No console.log allowed**: ESLint rule `no-console: error`.
- **`.env` is gitignored**: Contains `PUBLIC_GOOGLE_SITE_VERIFICATION`. All public env vars must be prefixed with `PUBLIC_`.
- **Deploy branch is `github-pages`**: Not `main`. GitHub Actions in `.github/workflows/deploy.yml`.
- **Alternative SFTP deploy**: `.gsupload.json` config for deploying `dist/` to `ecim.tech`.
- **Timezone default**: `America/Argentina/Buenos_Aires` in both `src/config.ts` and frontmatter defaults.
- **Custom type declaration**: `remark-collapse.d.ts` for the untyped `remark-collapse` module.
- **Tailwind v4 uses Vite plugin**, not PostCSS — tailwind config is CSS-based.

## Blog post frontmatter

```yaml
author: Gustavo Adrián Salvini   # default
pubDatetime: 2025-01-01          # required (Date)
title: "Post Title"              # required
description: "..."               # required
tags: [tag1, tag2]               # default: ["others"]
draft: true/false                # optional
featured: true/false             # optional
modDatetime: ...                 # optional (Date)
ogImage: ...                     # optional (image or string)
canonicalURL: ...                # optional
hideEditPost: true               # default
timezone: America/Argentina/Buenos_Aires  # optional
```

## Content conventions

- Blog is multilingual (Spanish/English/Italian) — posts may have `.mdx` or `.md` extension
- `src/data/blog/examples/` — example/template posts
- `src/data/blog/_releases/` — release notes (excluded from content loader via `[^_]` prefix)
- `src/components/AboutMe.md` and `AboutMeIntro.md` — markdown components imported into layouts
