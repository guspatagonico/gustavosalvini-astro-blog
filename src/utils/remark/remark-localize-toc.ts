import { getUI } from "../../i18n";

/**
 * Localiza la tabla de contenidos con el idioma del post.
 *
 * `remark-toc` busca un encabezado que matchee su patrón por defecto
 * (`(table[ -]of[ -])?contents?|toc`) y arma la lista; `remark-collapse` lo envuelve
 * en un `<details>` con el resumen `"Open " + texto del encabezado`. Los dos toman el
 * idioma de la nada: el encabezado es nomás un marcador que nunca se renderiza.
 *
 * Este plugin corre después de los dos y reescribe, con el `lang` del frontmatter:
 * el texto del encabezado y el del resumen. Así el marcador puede quedar en inglés
 * (o en "toc") en el fuente y cada post lo muestra en su idioma.
 *
 * El `lang` llega por `file.data.astro.frontmatter`, que es donde Astro expone el
 * frontmatter a los plugins de remark. Si no está, `getUI` cae al idioma por defecto.
 */

const TOC_HEADING = /^(toc|(table[ -]of[ -])?contents?)$/i;

interface Node {
  type?: string;
  depth?: number;
  value?: string;
  children?: Node[];
}

function headingText(node: Node): string {
  if (typeof node.value === "string") return node.value;
  return (node.children ?? []).map(headingText).join("");
}

export default function remarkLocalizeToc() {
  return (tree: Node, file: { data?: Record<string, any> }) => {
    const ui = getUI(file?.data?.astro?.frontmatter?.lang);

    const walk = (node: Node) => {
      const children = node.children;
      if (!Array.isArray(children)) return;

      for (let i = 0; i < children.length; i++) {
        const child = children[i];

        // El encabezado marcador de la tabla de contenidos.
        if (
          child.type === "heading" &&
          child.depth === 2 &&
          TOC_HEADING.test(headingText(child).trim())
        ) {
          child.children = [{ type: "text", value: ui.toc }];
          continue;
        }

        // El resumen del desplegable: el texto que sigue al `<summary>` de collapse.
        if (child.type === "html" && child.value === "<summary>") {
          const next = children[i + 1];
          if (next && next.type === "text") next.value = ui.openToc;
          continue;
        }

        walk(child);
      }
    };

    walk(tree);
  };
}
