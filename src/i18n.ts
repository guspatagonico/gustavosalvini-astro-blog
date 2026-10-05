/**
 * Cadenas de la interfaz del blog, por idioma.
 *
 * El idioma de cada post sale del campo `lang` de su frontmatter, que valida el
 * schema de la colección en `src/content.config.ts`. Acá viven las cadenas que el
 * tema cableaba en inglés: la tabla de contenidos, las fechas, los botones de la
 * página de post y los enlaces de compartir.
 *
 * Al agregar un idioma: sumalo a LANGS, agregá su entrada acá y el código ISO a
 * los locales de dayjs que importa `src/components/Datetime.astro`.
 */

export const LANGS = ["es", "it", "en"] as const;

export type Lang = (typeof LANGS)[number];

export const DEFAULT_LANG: Lang = "en";

export interface UIStrings {
  /** Encabezado de la tabla de contenidos que genera remark-toc. */
  toc: string;
  /** Texto del desplegable que la colapsa (remark-collapse). */
  openToc: string;
  shareOn: string;
  published: string;
  updated: string;
  at: string;
  goBack: string;
  backToTop: string;
  prevPost: string;
  nextPost: string;
  copy: string;
  copied: string;
  editPost: string;
  /** Formato de fecha de dayjs, por idioma. */
  dateFormat: string;
  /** Formato de hora de dayjs: 24 h en español e italiano, 12 h en inglés. */
  timeFormat: string;
  /** Código de locale de dayjs. */
  dayjsLocale: string;
}

const UI: Record<Lang, UIStrings> = {
  es: {
    toc: "Tabla de contenidos",
    openToc: "Abrir la tabla de contenidos",
    shareOn: "Compartir este post en:",
    published: "Publicado:",
    updated: "Actualizado:",
    at: "a las",
    goBack: "Volver",
    backToTop: "Volver arriba",
    prevPost: "Post anterior",
    nextPost: "Post siguiente",
    copy: "Copiar",
    copied: "Copiado",
    editPost: "Editar esta página",
    dateFormat: "D MMM, YYYY",
    timeFormat: "HH:mm",
    dayjsLocale: "es",
  },
  it: {
    toc: "Indice dei contenuti",
    openToc: "Apri l'indice dei contenuti",
    shareOn: "Condividi questo post su:",
    published: "Pubblicato:",
    updated: "Aggiornato:",
    at: "alle",
    goBack: "Torna indietro",
    backToTop: "Torna su",
    prevPost: "Post precedente",
    nextPost: "Post successivo",
    copy: "Copia",
    copied: "Copiato",
    editPost: "Modifica questa pagina",
    dateFormat: "D MMM, YYYY",
    timeFormat: "HH:mm",
    dayjsLocale: "it",
  },
  en: {
    toc: "Table of contents",
    openToc: "Open the table of contents",
    shareOn: "Share this post on:",
    published: "Published:",
    updated: "Updated:",
    at: "at",
    goBack: "Go back",
    backToTop: "Back to Top",
    prevPost: "Previous Post",
    nextPost: "Next Post",
    copy: "Copy",
    copied: "Copied",
    editPost: "Edit page",
    dateFormat: "MMM D, YYYY",
    timeFormat: "hh:mm A",
    dayjsLocale: "en",
  },
};

export function isLang(value: unknown): value is Lang {
  return (
    typeof value === "string" && (LANGS as readonly string[]).includes(value)
  );
}

/**
 * Cadenas del idioma pedido. Si el valor no es un idioma conocido (por ejemplo un
 * post viejo sin `lang`), cae al idioma por defecto en lugar de romper el build.
 */
export function getUI(lang?: string | null): UIStrings {
  return isLang(lang) ? UI[lang] : UI[DEFAULT_LANG];
}
