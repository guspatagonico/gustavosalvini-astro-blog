import { defineConfig } from "astro/config";
import { unified } from "@astrojs/markdown-remark";
import tailwindcss from "@tailwindcss/vite";
import sitemap from "@astrojs/sitemap";
import mdx from "@astrojs/mdx";
import remarkToc from "remark-toc";
import remarkCollapse from "remark-collapse";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import rehypeMermaid from "rehype-mermaid";
import rehypeModifyMermaidGraphs from "./src/utils/rehype/rehype-modifyMermaidGraphs";
import remarkLocalizeToc from "./src/utils/remark/remark-localize-toc";

import { SITE } from "./src/config";
import { targetBlank } from "./src/utils/rehype/rehype-targetBlank";

// https://astro.build/config
export default defineConfig({
  site: SITE.website,
  base: SITE.base,
  integrations: [
    mdx(),
    sitemap({
      filter: page => SITE.showArchives || !page.endsWith("/archives"),
    }),
  ],

  markdown: {
    processor: unified({
      remarkPlugins: [
        remarkMath,
        remarkToc,
        // El encabezado de la tabla de contenidos es un marcador que nunca se
        // renderiza: remarkLocalizeToc lo reescribe con el `lang` del frontmatter,
        // igual que el resumen colapsado que arma collapse.
        [remarkCollapse, { test: "toc|(table[ -]of[ -])?contents?" }],
        remarkLocalizeToc,
      ],
      rehypePlugins: [
        [targetBlank, { domain: "gustavosalvini.com.ar" }],
        rehypeKatex,
        [
          rehypeMermaid,
          { strategy: "img-svg", dark: true, colorScheme: "forest" },
        ],
        rehypeModifyMermaidGraphs,
      ],
    }),

    syntaxHighlight: {
      type: "shiki",
      excludeLangs: ["mermaid", "math"],
    },

    shikiConfig: {
      // For more themes, visit https://shiki.style/themes
      // themes: { light: "min-light", dark: "night-owl" },
      themes: { light: "min-light", dark: "dark-plus" },
      wrap: true,
    },
  },

  vite: {
    plugins: [tailwindcss()],
    optimizeDeps: {
      exclude: ["@resvg/resvg-js"],
    },
  },
  image: {
    // Used for all Markdown images; not configurable per-image
    // Used for all `<Image />` and `<Picture />` components unless overridden with a prop
    // experimentalLayout: "responsive",
    // experimentalLayout: "full-width",
  },
  experimental: {
    // svg: true,
    // responsiveImages: true,
  },
});
