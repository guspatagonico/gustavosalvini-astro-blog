#!/usr/bin/env python3
"""Detecta cambios de contenido en el blog y re-dispara el build+sync del espejo.

Lo invoca gustavosalvini-blog-preview.timer cada 15 s. Compara una firma del
arbol seguido (rutas, tamanos y mtime en nanosegundos) contra la guardada y solo
compila cuando cambio de verdad.

Por que no `fs.watch`: el recursivo de Node se quedo sordo en silencio a los
pocos minutos (el proceso vivo, los eventos sin llegar), asi que el espejo
servia contenido viejo sin avisar. Un poll con firma no tiene ese modo de falla.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/gustavo/dev/gustavosalvini-astro-blog")
BUILD = REPO / "scripts" / "preview-thalamus.sh"
STATE = Path("/home/gustavo/.local/state/gustavosalvini-blog-preview/state.json")

# Lo que puede cambiar el sitio. Si el build escupe algo aca adentro, el poll
# entra en loop: `pagefind` y `astro build` escriben en dist-*, no en estos.
TRACKED = ["src", "public", "astro.config.ts", "package.json"]

IGNORE_PARTS = {"node_modules", ".astro", ".git"}
IGNORE_SUFFIXES = ("~", ".swp", ".tmp", ".pyc")


def tracked_files() -> list[Path]:
    files: list[Path] = []
    for entry in TRACKED:
        path = REPO / entry
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            for child in path.rglob("*"):
                if not child.is_file():
                    continue
                rel_parts = child.relative_to(REPO).parts
                if any(part in IGNORE_PARTS or part.startswith(".") for part in rel_parts):
                    continue
                if child.name.endswith(IGNORE_SUFFIXES):
                    continue
                files.append(child)
    return sorted(files)


def signature() -> str:
    hasher = hashlib.md5()
    for path in tracked_files():
        try:
            stat = path.stat()
        except FileNotFoundError:
            continue
        rel = path.relative_to(REPO)
        hasher.update(f"{rel}\0{stat.st_size}\0{stat.st_mtime_ns}\n".encode())
    return hasher.hexdigest()


def load_state() -> str | None:
    try:
        return json.loads(STATE.read_text())["signature"]
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return None


def save_state(sig: str) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps({"signature": sig}))


def main() -> int:
    current = signature()
    previous = load_state()

    if previous is None:
        print("[check] sin estado previo: compilo para fijar la linea base")
    elif current == previous:
        return 0  # nada cambio: la mayoria de los ticks terminan aca
    else:
        print("[check] cambio el contenido, recompilando el espejo")

    result = subprocess.run(
        ["/usr/bin/bash", str(BUILD)],
        cwd=REPO,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )
    if result.returncode != 0:
        # No guardamos el estado: el proximo tick reintenta.
        print(f"[check] el build fallo (codigo {result.returncode}), reintento en el proximo tick", file=sys.stderr)
        return 1

    save_state(current)
    return 0


if __name__ == "__main__":
    sys.exit(main())
