import { SITE } from "@/config";

export function getPagePath(path: string): string {
  const basePath = SITE.base ?? "";
  // Ensure path starts with / and doesn't duplicate if base already ends with /
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  return `${basePath}${normalizedPath}`;
}
