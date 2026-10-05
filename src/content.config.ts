import { defineCollection } from "astro:content";
import { z } from "astro/zod";
import { glob } from "astro/loaders";
import { SITE } from "@/config";

export const BLOG_PATH = "src/data/blog";

const blog = defineCollection({
  // loader: glob({ pattern: "**/[^_]*.md", base: `./${BLOG_PATH}` }),
  loader: glob({ pattern: "**/[^_]*{.md,.mdx}", base: `./${BLOG_PATH}` }),
  schema: ({ image }) =>
    z.object({
      author: z.string().default(SITE.author),
      pubDatetime: z.date(),
      modDatetime: z.date().optional().nullable(),
      title: z.string(),
      // Idioma del post: maneja las cadenas del tema (tabla de contenidos, fechas,
      // botones) y el `lang` del <html>. Mismo campo que ya usan las páginas en
      // src/pages/*.md. Obligatorio a propósito: un post sin idioma no debe compilar.
      lang: z.enum(["es", "it", "en"]),
      // Vínculo entre traducciones: el slug del post original del que este es una
      // traducción. Opcional, porque la mayoría de los posts no tiene hermanos. El
      // original no lo lleva: el vínculo va en un solo sentido y el sitio calcula
      // el grupo al revés, sumando los posts que apuntan al mismo original.
      translationOf: z.string().optional(),
      featured: z.boolean().optional(),
      draft: z.boolean().optional(),
      tags: z.array(z.string()).default(["others"]),
      ogImage: image().or(z.string()).optional(),
      description: z.string(),
      canonicalURL: z.string().optional(),
      hideEditPost: z.boolean().optional(),
      timezone: z.string().optional(),
    }),
});

export const collections = { blog };
