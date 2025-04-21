import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";
import sitemap from "@astrojs/sitemap";
import mdx from "@astrojs/mdx";
import remarkToc from "remark-toc";
import remarkCollapse from "remark-collapse";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import rehypeMermaid from "rehype-mermaid";
import rehypeModifyMermaidGraphs from "./src/utils/rehype/rehype-modifyMermaidGraphs";

import { SITE } from "./src/config";
import { targetBlank } from "./src/utils/rehype/rehype-targetBlank";

// https://astro.build/config
export default defineConfig({
  site: SITE.website,
  integrations: [
    mdx(),
    sitemap({
      filter: page => SITE.showArchives || !page.endsWith("/archives"),
    }),
  ],

  markdown: {
    remarkPlugins: [
      remarkMath,
      remarkToc,
      [remarkCollapse, { test: "Table of contents" }],
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
    experimentalLayout: "responsive",
  },
  experimental: {
    // svg: true,
    responsiveImages: true,
    preserveScriptOrder: true,
  },
});
