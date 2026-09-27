"""Abre en una pestaña nueva los enlaces del texto de los apuntes."""

import re

_ENLACE = re.compile(r"<a\b([^>]*?)\bhref=(\"[^\"]*\"|'[^']*')([^>]*)>", re.IGNORECASE)


def _abrir_en_nueva_pestana(html: str) -> str:
    def sustituir(coincidencia: re.Match) -> str:
        antes, href_attr, despues = coincidencia.group(1), coincidencia.group(2), coincidencia.group(3)
        href = href_attr[1:-1].strip()
        if not href or href.startswith("#") or href.startswith("mailto:") or href.startswith("javascript:"):
            return coincidencia.group(0)
        atributos = f"{antes}{despues}"
        if re.search(r"\btarget\s*=", atributos, re.IGNORECASE):
            return coincidencia.group(0)
        rel = ""
        if not re.search(r"\brel\s*=", atributos, re.IGNORECASE):
            rel = ' rel="noopener"'
        return f"<a{antes}href={href_attr}{despues} target=\"_blank\"{rel}>"

    return _ENLACE.sub(sustituir, html)


def on_page_content(html, page, config, files):
    return _abrir_en_nueva_pestana(html)
