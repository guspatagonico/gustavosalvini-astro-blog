#!/usr/bin/env python3
"""Verifica el vinculo entre traducciones del blog.

Corre sobre los frontmatter y sobre el sitio construido, asi que se corre despues
de `pnpm build`. Sale con 1 si encuentra algo inconsistente.

    /usr/bin/python3 scripts/verificar-traducciones.py

Chequea:

  1. Que cada `translationOf` apunte a un slug que existe.
  2. Que ningun post se apunte a si mismo.
  3. Que no haya dos originales distintos para el mismo hermano, ni cadenas.
  4. Que no haya dos versiones del mismo idioma en un grupo.
  5. Que cada pagina con hermanos tenga su `hreflang` por idioma del grupo, mas
     el `x-default`, y que las paginas sin hermanos no tengan ninguno.
  6. Que las URLs del `hreflang` sean del dominio publico, nunca del espejo.
"""

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BLOG = RAIZ / "src/data/blog"
DIST = RAIZ / "dist/posts"
DOMINIO = "https://gustavosalvini.com.ar"

errores: list[str] = []
avisos: list[str] = []


def frontmatter(texto: str) -> dict[str, str]:
    """Campo -> valor de las lineas simples del frontmatter (los que nos importan)."""
    if not texto.startswith("---"):
        return {}
    fin = texto.find("\n---", 3)
    campos = {}
    for linea in texto[3:fin].splitlines():
        m = re.match(r"^([A-Za-z][A-Za-z0-9_]*):\s*(.*)$", linea)
        if m:
            campos[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return campos


# ---------- 1. leer los posts ----------
posts: dict[str, dict[str, str]] = {}
for archivo in sorted(BLOG.rglob("*.md*")):
    if any(part.startswith("_") for part in archivo.relative_to(BLOG).parts):
        continue
    campos = frontmatter(archivo.read_text(encoding="utf-8"))
    if not campos.get("lang"):
        continue  # un post sin lang no lo carga la coleccion
    slug = campos.get("slug") or archivo.stem
    if slug in posts:
        avisos.append(
            f"dos posts declaran el mismo slug `{slug}`: {posts[slug]['archivo']} y {archivo.name}. "
            "No rompe mientras sean borradores, pero uno de los dos no va a tener ruta."
        )
    posts[slug] = {
        "lang": campos["lang"],
        "translationOf": campos.get("translationOf", ""),
        "draft": campos.get("draft", ""),
        "archivo": archivo.name,
    }

# ---------- 2. los cuatro chequeos del vinculo ----------
for slug, post in sorted(posts.items()):
    original = post["translationOf"]
    if not original:
        continue
    if original == slug:
        errores.append(f"{slug}: se apunta a si mismo")
        continue
    if original not in posts:
        errores.append(f"{slug}: translationOf apunta a `{original}`, que no existe")
        continue
    if posts[original]["translationOf"]:
        errores.append(
            f"{slug} -> {original}, pero {original} tambien declara translationOf "
            f"({posts[original]['translationOf']}): el vinculo tiene que ser en un solo sentido"
        )

grupos: dict[str, list[str]] = {}
for slug, post in posts.items():
    raiz = post["translationOf"] or slug
    grupos.setdefault(raiz, []).append(slug)

for raiz, miembros in sorted(grupos.items()):
    idiomas = [posts[m]["lang"] for m in miembros]
    repetidos = {i for i in idiomas if idiomas.count(i) > 1}
    if repetidos:
        errores.append(f"grupo {raiz}: dos versiones del mismo idioma {sorted(repetidos)}")
    if raiz not in miembros:
        errores.append(f"grupo {raiz}: el original no esta entre sus miembros")

# ---------- 3. el hreflang del sitio construido ----------
if not DIST.is_dir():
    avisos.append("no hay dist/: corre `pnpm build` para chequear el hreflang del HTML")
else:
    for raiz, miembros in sorted(grupos.items()):
        # Los grupos de un solo idioma no llevan hreflang: no hay a donde mandar.
        if len(miembros) < 2:
            continue
        esperados = {posts[m]["lang"]: m for m in miembros}
        for slug in miembros:
            pagina = DIST / slug / "index.html"
            if not pagina.is_file():
                if posts[slug].get("draft", "").lower() != "true":
                    errores.append(f"{slug}: es un post publicado y no esta en dist/")
                continue
            html = pagina.read_text(encoding="utf-8")
            links = [
                (lang, href)
                for lang, href in re.findall(
                    r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"\s*/?>', html
                )
                if lang != "x-default"
            ]
            dichos = {lang: href for lang, href in links}
            for lang, otro in esperados.items():
                if lang not in dichos:
                    errores.append(f"{slug}: falta el hreflang de `{lang}`")
                elif not dichos[lang].startswith(DOMINIO):
                    errores.append(
                        f"{slug}: el hreflang de `{lang}` no usa el dominio publico ({dichos[lang]})"
                    )
                elif f"/posts/{otro}/" != dichos[lang][len(DOMINIO):]:
                    errores.append(
                        f"{slug}: el hreflang de `{lang}` apunta a {dichos[lang]} y esperaba /posts/{otro}/"
                    )
            if len(links) > len(esperados):
                errores.append(f"{slug}: tiene {len(links)} hreflang y el grupo tiene {len(esperados)} idiomas")
            if "x-default" not in html:
                errores.append(f"{slug}: sin x-default")

    for slug in sorted(posts):
        if grupos.get(posts[slug]["translationOf"] or slug, []).__len__() > 1:
            continue
        pagina = DIST / slug / "index.html"
        if pagina.is_file() and 'hreflang=' in pagina.read_text(encoding="utf-8"):
            errores.append(f"{slug}: no tiene traducciones y sin embargo declara hreflang")

# ---------- 4. informe ----------
con_translation = sum(1 for p in posts.values() if p["translationOf"])
con_hermanos = {r: m for r, m in grupos.items() if len(m) > 1}
print(f"  posts con `lang`: {len(posts)}")
print(f"  posts traducidos (declaran translationOf): {con_translation}")
print(f"  grupos con mas de una version: {len(con_hermanos)}")
for raiz, miembros in sorted(con_hermanos.items()):
    detalle = ", ".join(f"{posts[m]['lang']}:{m}" for m in sorted(miembros, key=lambda x: posts[x]["lang"]))
    print(f"    {raiz}: {detalle}")
for a in avisos:
    print(f"  aviso: {a}")
if errores:
    print()
    for e in errores:
        print(f"  ERROR: {e}")
    sys.exit(1)
print("  todo consistente.")
