import { visit } from "unist-util-visit";

const rehypeModifyMermaidGraphs = () => {
  return tree => {
    visit(tree, "element", node => {
      if (node.tagName === "picture") {
        // if has children <source> and <img> with a tag prefix of "mermaid-[index]"
        if (
          node.children.length === 2 &&
          node.children[0].tagName === "source" &&
          node.children[1].tagName === "img"
        ) {
          const sourceNode = node.children[0];
          const imgNode = node.children[1];

          // check the prefix
          const split = imgNode.properties.id.split("-");
          if (split.length !== 2) return;
          if (split[0] !== "mermaid") return;

          const mermaidIndex = parseInt(split[1]);
          const darkID = `mermaid-dark-${mermaidIndex}`;
          const ID = `mermaid-${mermaidIndex}`;

          // skip if the children IDs don't match
          if (
            sourceNode.properties.id !== darkID ||
            imgNode.properties.id !== ID
          ) {
            return;
          }

          // add mx-auto to both source and img
          sourceNode.properties.className =
            sourceNode.properties.className || [];
          sourceNode.properties.className.push("mx-auto");
          sourceNode.properties.className.push("mermaid-dark");

          imgNode.properties.className = imgNode.properties.className || [];
          imgNode.properties.className.push("mx-auto");
          imgNode.properties.className.push("mermaid");
        }
      }
    });
  };
};

export default rehypeModifyMermaidGraphs;
