"""Genera los esquemas SVG de la unidad de bases de datos vectoriales.

Las cifras son las de los apuntes y del laboratorio: no son medidas de un
corpus real. Ejecutar desde cualquier sitio; escribe en docs/assets/esquemas.
"""

from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "docs" / "assets" / "esquemas"

INK = "#1c2340"
MUTED = "#5c657a"
INDIGO = "#3949ab"
INDIGO_SOFT = "#e8eaf6"
GREEN = "#2e7d32"
GREEN_SOFT = "#e8f5e9"
RED = "#b71c1c"
RED_SOFT = "#fdecea"
TEAL = "#00796b"
ORANGE = "#ef6c00"
LINE = "#d5daf0"
CARD = "#ffffff"
BG = "#f4f6fb"


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def save(name: str, body: str, title: str, desc: str, width: int, height: int) -> None:
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img">
  <title>{esc(title)}</title>
  <desc>{esc(desc)}</desc>
  <rect width="{width}" height="{height}" rx="18" fill="{BG}"/>
  <defs>
    <marker id="flecha" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 9 5 L 0 9 z" fill="{INDIGO}"/>
    </marker>
    <marker id="flecha-roja" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 1 L 9 5 L 0 9 z" fill="{RED}"/>
    </marker>
  </defs>
  {body}
</svg>
"""
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(svg, encoding="utf-8")


def text(x, y, content, size=16, fill=INK, weight=400, anchor="start"):
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{fill}" '
        f'font-family="Segoe UI, sans-serif" font-size="{size}" font-weight="{weight}">{esc(content)}</text>'
    )


def rect(x, y, w, h, fill=CARD, stroke=LINE, rx=12, sw=1.5):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
    )


def pipeline() -> None:
    steps = [
        ("1", "Pregunta", "¿Cómo me matriculo?", False),
        ("2", "Mismo modelo de embeddings", "Titan v2, 1024, normalizado", False),
        ("3", "ChromaDB", "Busca los fragmentos más cercanos", True),
        ("4", "Fragmentos recuperados", "Los 3 a 5 más relevantes, con su texto", False),
        ("5", "Modelo de lenguaje", "Redacta usando solo esos fragmentos", False),
        ("6", "Respuesta con cita", "El usuario puede abrir el documento", False),
    ]
    parts = [text(36, 42, "Dónde está la base vectorial en DocIA+", 20, INK, 650)]
    y = 64
    for number, title, detail, here in steps:
        fill = INDIGO_SOFT if here else CARD
        stroke = INDIGO if here else LINE
        parts.append(rect(36, y, 448, 64, fill, stroke, 14, 2 if here else 1.5))
        parts.append(rect(52, y + 14, 36, 36, INDIGO if here else INDIGO_SOFT, INDIGO, 10, 0))
        parts.append(text(70, y + 38, number, 16, "#ffffff" if here else INDIGO, 700, "middle"))
        parts.append(text(102, y + 28, title, 16, INK, 650))
        parts.append(text(102, y + 48, detail, 13, MUTED))
        if here:
            parts.append(text(468, y + 38, "esta unidad", 13, INDIGO, 650, "end"))
        y += 76
    save(
        "00-pipeline.svg",
        "\n".join(parts),
        "Recorrido de una pregunta en DocIA+",
        "La pregunta se convierte en vector, ChromaDB devuelve fragmentos y otro modelo redacta la respuesta citando la fuente.",
        520,
        y + 8,
    )


def modulos() -> None:
    cols = [
        (36, "SBD", "Prepara el corpus", ["Texto limpio", "Categorías g1–g5", "Metadatos del fragmento"]),
        (262, "BDA", "Llena la colección", ["Corta en fragmentos", "Llama a Titan v2", "upsert en ChromaDB"]),
        (488, "PIA", "Consulta después", ["API de la pregunta", "Recupera fragmentos", "Redacta y cita"]),
    ]
    parts = []
    for x, name, subtitle, items in cols:
        parts.append(rect(x, 24, 210, 268, CARD, LINE, 16))
        parts.append(rect(x, 24, 210, 48, INDIGO, INDIGO, 16))
        parts.append(rect(x, 56, 210, 16, INDIGO, INDIGO, 0))
        parts.append(text(x + 105, 54, name, 20, "#ffffff", 700, "middle"))
        parts.append(text(x + 105, 96, subtitle, 14, INDIGO, 650, "middle"))
        yy = 118
        for item in items:
            parts.append(rect(x + 16, yy, 178, 36, INDIGO_SOFT, INDIGO_SOFT, 8, 0))
            parts.append(text(x + 105, yy + 23, item, 14, INK, 500, "middle"))
            yy += 46
    parts.append(text(367, 322, "SBD entrega el texto · BDA entrega la colección", 14, MUTED, 500, "middle"))
    save(
        "00-modulos.svg",
        "\n".join(parts),
        "Qué hace cada módulo con la base vectorial",
        "SBD prepara texto y metadatos, BDA escribe los vectores en ChromaDB y PIA consulta esa colección.",
        734,
        348,
    )


def categorias() -> None:
    groups = [
        ("g1", "Programaciones"),
        ("g2", "Proyecto educativo"),
        ("g3", "Planes y programas"),
        ("g4", "Oferta educativa"),
        ("g5", "Actividades y horarios"),
    ]
    parts = [text(36, 40, "Cinco categorías, una sola colección", 20, INK, 650)]
    y = 64
    for code, name in groups:
        parts.append(rect(36, y, 250, 48, CARD, LINE, 12))
        parts.append(rect(48, y + 10, 44, 28, INDIGO, INDIGO, 8, 0))
        parts.append(text(70, y + 29, code, 13, "#ffffff", 700, "middle"))
        parts.append(text(104, y + 30, name, 15, INK, 500))
        parts.append(f'<line x1="286" y1="{y+24}" x2="360" y2="176" stroke="{LINE}" stroke-width="2"/>')
        y += 58
    parts.append(rect(360, 120, 250, 112, INDIGO_SOFT, INDIGO, 16, 2))
    parts.append(text(485, 168, "ChromaDB", 20, INDIGO, 700, "middle"))
    parts.append(text(485, 194, "Una colección", 15, INK, 500, "middle"))
    parts.append(text(485, 214, "la categoría es un filtro", 13, MUTED, 400, "middle"))
    save(
        "00-categorias.svg",
        "\n".join(parts),
        "Las cinco categorías entran en una colección",
        "Cada grupo documenta una categoría, y todas se guardan en la misma colección de ChromaDB.",
        646,
        370,
    )


def literal() -> None:
    parts = []
    parts.append(rect(24, 24, 330, 300, RED_SOFT, "#f5c6c2", 16))
    parts.append(text(40, 56, "Búsqueda literal", 18, RED, 700))
    parts.append(rect(40, 76, 298, 44, CARD, LINE, 22))
    parts.append(text(52, 104, "¿cómo me matriculo?", 15, INK, 500))
    parts.append(rect(40, 140, 298, 88, CARD, LINE, 12))
    parts.append(text(52, 168, "En el documento dice:", 13, MUTED))
    parts.append(text(52, 192, "formalización de matrícula", 14, INK, 650))
    parts.append(text(52, 212, "Esas palabras no están", 13, RED, 500))
    parts.append(text(189, 280, "No lo encuentra", 18, RED, 700, "middle"))

    parts.append(rect(370, 24, 330, 300, GREEN_SOFT, "#b7dfb9", 16))
    parts.append(text(386, 56, "Búsqueda semántica", 18, GREEN, 700))
    parts.append(rect(386, 76, 298, 44, CARD, LINE, 22))
    parts.append(text(398, 104, "¿cómo me matriculo?", 15, INK, 500))
    # two close points
    parts.append(f'<circle cx="470" cy="190" r="14" fill="{INDIGO}"/>')
    parts.append(f'<circle cx="520" cy="168" r="14" fill="{TEAL}"/>')
    parts.append(text(492, 240, "Pregunta y documento", 14, INK, 650, "middle"))
    parts.append(text(492, 260, "quedan cerca", 14, INK, 500, "middle"))
    parts.append(text(535, 280, "Sí lo recupera", 18, GREEN, 700, "middle"))
    save(
        "01-literal-vs-semantica.svg",
        "\n".join(parts),
        "La búsqueda literal no encuentra el documento y la semántica sí",
        "La pregunta cómo me matriculo no contiene las palabras formalización de matrícula. En el espacio vectorial los dos textos quedan próximos.",
        724,
        348,
    )


def embedding_io() -> None:
    parts = []
    parts.append(rect(24, 36, 200, 70, CARD, LINE, 14))
    parts.append(text(124, 66, "Fragmento", 16, INK, 650, "middle"))
    parts.append(text(124, 88, "texto del documento", 13, MUTED, 400, "middle"))
    parts.append(rect(24, 150, 200, 70, CARD, LINE, 14))
    parts.append(text(124, 180, "Pregunta", 16, INK, 650, "middle"))
    parts.append(text(124, 202, "texto del usuario", 13, MUTED, 400, "middle"))
    parts.append(f'<line x1="224" y1="71" x2="286" y2="128" stroke="{INDIGO}" stroke-width="2" marker-end="url(#flecha)"/>')
    parts.append(f'<line x1="224" y1="185" x2="286" y2="148" stroke="{INDIGO}" stroke-width="2" marker-end="url(#flecha)"/>')
    parts.append(rect(286, 78, 210, 120, INDIGO, INDIGO, 16, 0))
    parts.append(text(391, 118, "Un solo modelo", 16, "#ffffff", 700, "middle"))
    parts.append(text(391, 144, "Titan Embeddings v2", 14, "#e8eaf6", 500, "middle"))
    parts.append(text(391, 168, "1024 · normalizado", 14, "#e8eaf6", 500, "middle"))
    parts.append(f'<line x1="496" y1="120" x2="548" y2="78" stroke="{INDIGO}" stroke-width="2" marker-end="url(#flecha)"/>')
    parts.append(f'<line x1="496" y1="156" x2="548" y2="198" stroke="{INDIGO}" stroke-width="2" marker-end="url(#flecha)"/>')
    parts.append(rect(548, 36, 200, 78, INDIGO_SOFT, INDIGO, 14))
    parts.append(text(648, 66, "Vector del fragmento", 14, INK, 650, "middle"))
    parts.append(text(648, 90, "se guarda", 13, MUTED, 400, "middle"))
    parts.append(rect(548, 156, 200, 78, CARD, LINE, 14))
    parts.append(text(648, 186, "Vector de la pregunta", 14, INK, 650, "middle"))
    parts.append(text(648, 210, "no se guarda", 13, MUTED, 400, "middle"))
    save(
        "02-mismo-modelo.svg",
        "\n".join(parts),
        "El fragmento y la pregunta pasan por el mismo modelo",
        "Indexar y consultar usan Titan Embeddings v2 con 1024 dimensiones y normalización. El vector de la pregunta no se almacena.",
        772,
        270,
    )


def dimensiones() -> None:
    parts = []
    parts.append(rect(24, 24, 340, 180, GREEN_SOFT, "#b7dfb9", 16))
    parts.append(text(194, 58, "Válido", 18, GREEN, 700, "middle"))
    parts.append(rect(48, 80, 120, 64, CARD, GREEN, 12, 2))
    parts.append(text(108, 108, "1024", 22, GREEN, 700, "middle"))
    parts.append(text(108, 130, "indexado", 13, MUTED, 400, "middle"))
    parts.append(text(194, 118, "=", 28, GREEN, 700, "middle"))
    parts.append(rect(220, 80, 120, 64, CARD, GREEN, 12, 2))
    parts.append(text(280, 108, "1024", 22, GREEN, 700, "middle"))
    parts.append(text(280, 130, "consulta", 13, MUTED, 400, "middle"))
    parts.append(text(194, 176, "misma dimensión y norma", 14, GREEN, 500, "middle"))

    parts.append(rect(384, 24, 340, 180, RED_SOFT, "#f5c6c2", 16))
    parts.append(text(554, 58, "No válido", 18, RED, 700, "middle"))
    parts.append(rect(408, 80, 120, 64, CARD, RED, 12, 2))
    parts.append(text(468, 108, "1024", 22, RED, 700, "middle"))
    parts.append(text(468, 130, "indexado", 13, MUTED, 400, "middle"))
    parts.append(text(554, 118, "≠", 28, RED, 700, "middle"))
    parts.append(rect(580, 80, 120, 64, CARD, RED, 12, 2))
    parts.append(text(640, 108, "256", 22, RED, 700, "middle"))
    parts.append(text(640, 130, "consulta", 13, MUTED, 400, "middle"))
    parts.append(text(554, 176, "hay que reindexar todo", 14, RED, 500, "middle"))
    save(
        "02-dimensiones.svg",
        "\n".join(parts),
        "No se puede consultar en 256 una colección indexada en 1024",
        "Los dos vectores tienen que salir del mismo modelo, con la misma dimensión y la misma normalización.",
        748,
        228,
    )


def perfiles() -> None:
    rows = [
        ("Formalización de matrícula", (0.90, 0.10, 0.00), False),
        ("Cómo me matriculo", (0.85, 0.20, 0.05), False),
        ("Pregunta: ¿cómo me matriculo?", (0.88, 0.15, 0.02), True),
        ("Horas del módulo", (0.05, 0.95, 0.00), False),
        ("Plan de convivencia", (0.00, 0.05, 0.90), False),
    ]
    colors = (INDIGO, TEAL, ORANGE)
    names = ("Matrícula", "Horas", "Convivencia")
    parts = [text(24, 36, "Perfil de los vectores de ejemplo", 20, INK, 650)]
    parts.append(text(24, 60, "Ejes inventados para ver la cuenta. En Titan no se pueden etiquetar.", 13, MUTED))
    x = 24
    for color, name in zip(colors, names):
        parts.append(rect(x, 78, 14, 14, color, color, 3, 0))
        parts.append(text(x + 20, 90, name, 14, INK, 500))
        x += 150
    y = 112
    max_w = 280
    for label, values, query in rows:
        if query:
            parts.append(rect(16, y - 8, 728, 78, INDIGO_SOFT, INDIGO, 12, 1.5))
        parts.append(text(28, y + 22, label, 15, INK, 650))
        bx = 300
        for value, color in zip(values, colors):
            width = max(3, round(value * max_w))
            parts.append(rect(bx, y + 8, width, 16, color, color, 4, 0))
            parts.append(text(bx + width + 8, y + 21, f"{value:.2f}".replace(".", ","), 13, MUTED, 500))
            bx += 0
            y_bar = y
            # stacked vertically inside the row: redraw properly below
        y += 84
    # The loop above placed all three bars on the same y. Rebuild cleanly.
    parts = [text(24, 36, "Perfil de los vectores de ejemplo", 20, INK, 650)]
    parts.append(text(24, 58, "Ejes inventados para la clase. Un embedding real no se etiqueta así.", 13, MUTED))
    x = 24
    for color, name in zip(colors, names):
        parts.append(rect(x, 74, 14, 14, color, color, 3, 0))
        parts.append(text(x + 20, 86, name, 14, INK, 500))
        x += 160
    y = 108
    for label, values, query in rows:
        if query:
            parts.append(rect(16, y - 6, 760, 86, INDIGO_SOFT, INDIGO, 12, 1.5))
        parts.append(text(32, y + 28, label, 15, INK, 650))
        for index, (value, color) in enumerate(zip(values, colors)):
            bar_y = y + 40 + index * 0
            # three bars side by side under the label would be wide; stack them to the right
        bar_x = 340
        bar_y = y + 8
        for value, color in zip(values, colors):
            width = max(4, round(value * 300))
            parts.append(rect(bar_x, bar_y, width, 18, color, color, 5, 0))
            parts.append(text(bar_x + width + 8, bar_y + 14, f"{value:.2f}".replace(".", ","), 13, INK, 500))
            bar_y += 24
        y += 96
    save(
        "03-perfiles.svg",
        "\n".join(parts),
        "Perfil de los cinco vectores de ejemplo",
        "La pregunta se parece al trámite de matrícula. Horas y convivencia tienen otro perfil. Los números son los del tema, con ejes didácticos.",
        792,
        y + 4,
    )


def coseno() -> None:
    # Three panels with arrows drawn as lines.
    panels = [
        (24, "Misma dirección", "coseno = 1", GREEN, ((40, 110), (150, 70), (40, 110), (150, 70))),
        (262, "Ángulo pequeño", "coseno alto", INDIGO, ((40, 120), (150, 78), (40, 120), (120, 48))),
        (500, "Perpendiculares", "coseno = 0", ORANGE, ((40, 130), (160, 130), (40, 130), (40, 50))),
    ]
    parts = []
    for x, title, caption, color, lines in panels:
        parts.append(rect(x, 20, 220, 210, CARD, LINE, 16))
        parts.append(text(x + 110, 50, title, 15, INK, 650, "middle"))
        x1, y1, x2, y2, x3, y3, x4, y4 = (*lines[0], *lines[1], *lines[2], *lines[3]) if False else (0, 0, 0, 0, 0, 0, 0, 0)
    # draw explicitly for control
    parts = []
    specs = [
        (24, "Misma dirección", "coseno = 1", GREEN, [(70, 150, 190, 90)]),
        (262, "Ángulo pequeño", "coseno alto", INDIGO, [(70, 160, 200, 150), (70, 160, 160, 70)]),
        (500, "Perpendiculares", "coseno = 0", ORANGE, [(70, 160, 200, 160), (70, 160, 70, 70)]),
    ]
    for x, title, caption, color, arrows in specs:
        parts.append(rect(x, 16, 220, 230, CARD, LINE, 16))
        parts.append(text(x + 110, 46, title, 15, INK, 650, "middle"))
        for x1, y1, x2, y2 in arrows:
            parts.append(
                f'<line x1="{x+x1-40}" y1="{y1}" x2="{x+x2-40}" y2="{y2}" stroke="{color}" stroke-width="3" marker-end="url(#flecha)"/>'
            )
        # marker is indigo; for non-indigo panels draw a circle at the tip instead of relying on color
        parts.append(text(x + 110, 214, caption, 16, color, 700, "middle"))
    save(
        "03-coseno.svg",
        "\n".join(parts),
        "El coseno mide el ángulo, no la longitud",
        "Si los vectores están normalizados, mirar al mismo sitio da coseno 1. Un ángulo recto da coseno 0.",
        744,
        262,
    )


def mapa_significado() -> None:
    ox, oy, k = 70, 330, 52

    def px(x):
        return ox + x * k

    def py(y):
        return oy - y * k

    puntos = [
        ("P", "Pregunta: ¿cómo me matriculo?", (4, 1), INDIGO),
        ("F", "Procedimiento de formalización de matrícula", (3, 1), TEAL),
        ("I", "Plazo de inscripción en el ciclo", (5, 0), GREEN),
        ("C", "Menú diario de la cafetería", (1, 4), ORANGE),
        ("B", "Precio del bocadillo", (0, 3), RED),
    ]
    parts = [text(24, 34, "Un mapa de significado con dos ejes inventados", 18, INK, 650)]
    parts.append(
        f'<ellipse cx="{px(4)}" cy="{py(0.6)}" rx="{1.75 * k}" ry="{1.0 * k}" fill="{INDIGO_SOFT}" '
        f'stroke="{INDIGO}" stroke-width="1.5" stroke-dasharray="6 5"/>'
    )
    parts.append(
        f'<ellipse cx="{px(0.6)}" cy="{py(3.5)}" rx="{1.2 * k}" ry="{1.3 * k}" fill="{GREEN_SOFT}" '
        f'stroke="{GREEN}" stroke-width="1.5" stroke-dasharray="6 5"/>'
    )
    parts.append(f'<line x1="{ox}" y1="{oy}" x2="{px(6.2)}" y2="{oy}" stroke="{INK}" stroke-width="1.5"/>')
    parts.append(f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{py(4.7)}" stroke="{INK}" stroke-width="1.5"/>')
    for i in range(1, 6):
        parts.append(f'<line x1="{px(i)}" y1="{oy}" x2="{px(i)}" y2="{oy + 5}" stroke="{MUTED}" stroke-width="1"/>')
        parts.append(text(px(i), oy + 20, str(i), 12, MUTED, 500, "middle"))
    for j in range(1, 5):
        parts.append(f'<line x1="{ox - 5}" y1="{py(j)}" x2="{ox}" y2="{py(j)}" stroke="{MUTED}" stroke-width="1"/>')
        parts.append(text(ox - 12, py(j) + 4, str(j), 12, MUTED, 500, "end"))
    parts.append(text(px(3.1), oy + 44, "eje 1: cuánto habla de matrícula  →", 13, MUTED, 500, "middle"))
    parts.append(
        f'<text x="24" y="{py(2.4)}" text-anchor="middle" fill="{MUTED}" font-family="Segoe UI, sans-serif" '
        f'font-size="13" font-weight="500" transform="rotate(-90 24 {py(2.4)})">eje 2: cuánto habla de cafetería  →</text>'
    )
    for key, _, (x, y), color in puntos:
        parts.append(f'<circle cx="{px(x)}" cy="{py(y)}" r="8" fill="{color}"/>')
        parts.append(text(px(x), py(y) - 14, key, 16, color, 800, "middle"))
    parts.append(text(px(4), py(1.85), "textos de matrícula", 13, INDIGO, 700, "middle"))
    parts.append(text(px(0.65), py(2.05), "textos de cafetería", 13, GREEN, 700, "middle"))
    parts.append(rect(452, 70, 236, 214, CARD, LINE, 14))
    lines = [
        ("Cada texto es un punto.", INK, 650),
        ("Los que hablan de lo mismo", MUTED, 400),
        ("quedan juntos.", MUTED, 400),
        ("", INK, 400),
        ("La pregunta P cae en el grupo", MUTED, 400),
        ("de matrícula, aunque no repita", MUTED, 400),
        ("las palabras de F ni de I.", MUTED, 400),
        ("", INK, 400),
        ("Buscar es mirar qué hay cerca.", INK, 650),
    ]
    y = 98
    for content, color, weight in lines:
        if content:
            parts.append(text(468, y, content, 14, color, weight))
        y += 20
    parts.append(rect(24, 400, 664, 116, CARD, LINE, 12))
    for index, (key, label, (x, y), color) in enumerate(puntos):
        parts.append(text(40, 426 + index * 20, f"{key}  {label}  ({x}, {y})", 13, color, 700))
    save(
        "02-mapa-significado.svg",
        "\n".join(parts),
        "Un mapa de significado con dos ejes",
        "Cinco textos colocados según cuánto hablan de matrícula y de cafetería. Los textos de matrícula quedan juntos, incluida la pregunta, y los de cafetería en otra zona.",
        712,
        536,
    )


def texto_a_vector() -> None:
    parts = [text(24, 34, "Qué pasa dentro de la llamada al modelo", 18, INK, 650)]
    boxes = [
        (24, "1. Texto", INDIGO_SOFT, INDIGO, ["«¿Cómo me", "matriculo?»"], "lo que enviamos"),
        (214, "2. Tokens", CARD, LINE, ["¿ · Cómo · me", "· matric · ulo · ?"], "trozos pequeños"),
        (404, "3. Modelo", CARD, LINE, ["red neuronal", "ya entrenada"], "no la entrenamos"),
        (594, "4. Vector", GREEN_SOFT, GREEN, ["[0,021  −0,087", "0,154  … ]"], "1024 números"),
    ]
    for x, title, fill, stroke, lines, caption in boxes:
        parts.append(rect(x, 64, 162, 130, fill, stroke, 14, 1.8))
        parts.append(text(x + 81, 92, title, 16, INK, 700, "middle"))
        for i, content in enumerate(lines):
            parts.append(text(x + 81, 126 + i * 24, content, 14, INK, 500, "middle"))
        parts.append(text(x + 81, 218, caption, 13, MUTED, 500, "middle"))
    for x in (186, 376, 566):
        parts.append(
            f'<line x1="{x + 2}" y1="129" x2="{x + 26}" y2="129" stroke="{INDIGO}" stroke-width="2.5" marker-end="url(#flecha)"/>'
        )
    parts.append(text(24, 258, "Los tokens y los números de la figura son ilustrativos: el corte real y los valores dependen del modelo.", 13, MUTED))
    parts.append(text(24, 280, "Lo importante es que siempre entra un texto de cualquier largo y sale una lista de longitud fija.", 13, MUTED))
    save(
        "02-texto-a-vector.svg",
        "\n".join(parts),
        "Del texto al vector en cuatro pasos",
        "El texto se parte en tokens, el modelo los procesa y devuelve una lista de números de longitud fija.",
        780,
        302,
    )


GEO_PUNTOS = [
    ("P", "Pregunta: ¿cómo me matriculo?", (4, 1), INDIGO),
    ("F", "Formalización de matrícula", (3, 1), TEAL),
    ("C", "Menú de la cafetería", (1, 4), ORANGE),
    ("G", "Guía larga de matrícula", (12, 3), GREEN),
]


def flechas_2d() -> None:
    ox, oy = 70, 330

    def px(x):
        return ox + x * 44

    def py(y):
        return oy - y * 55

    parts = [text(24, 34, "Cuatro textos como flechas en dos ejes", 18, INK, 650)]
    parts.append(f'<line x1="{ox}" y1="{oy}" x2="{px(13.2)}" y2="{oy}" stroke="{INK}" stroke-width="1.5"/>')
    parts.append(f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{py(4.9)}" stroke="{INK}" stroke-width="1.5"/>')
    for i in range(1, 13):
        parts.append(f'<line x1="{px(i)}" y1="{oy}" x2="{px(i)}" y2="{oy + 5}" stroke="{MUTED}" stroke-width="1"/>')
        if i in (1, 3, 4, 12):
            parts.append(text(px(i), oy + 20, str(i), 12, MUTED, 500, "middle"))
    for j in range(1, 5):
        parts.append(f'<line x1="{ox - 5}" y1="{py(j)}" x2="{ox}" y2="{py(j)}" stroke="{MUTED}" stroke-width="1"/>')
        parts.append(text(ox - 12, py(j) + 4, str(j), 12, MUTED, 500, "end"))
    parts.append(text(px(6.5), oy + 42, "eje 1: habla de matrícula  →", 13, MUTED, 500, "middle"))
    parts.append(
        f'<text x="26" y="{py(2.4)}" text-anchor="middle" fill="{MUTED}" font-family="Segoe UI, sans-serif" '
        f'font-size="13" font-weight="500" transform="rotate(-90 26 {py(2.4)})">eje 2: habla de cafetería  →</text>'
    )
    for key, label, (x, y), color in sorted(GEO_PUNTOS, key=lambda item: -abs(complex(*item[2]))):
        parts.append(
            f'<line x1="{ox}" y1="{oy}" x2="{px(x)}" y2="{py(y)}" stroke="{color}" stroke-width="{5 if key == "P" else 3}"/>'
        )
        parts.append(f'<circle cx="{px(x)}" cy="{py(y)}" r="6" fill="{color}"/>')
    p = GEO_PUNTOS[0][2]
    parts.append(
        f'<line x1="{px(p[0])}" y1="{py(p[1])}" x2="{px(1)}" y2="{py(4)}" '
        f'stroke="{RED}" stroke-width="1.8" stroke-dasharray="6 5"/>'
    )
    parts.append(text((px(4) + px(1)) / 2 + 14, (py(1) + py(4)) / 2, "P a C: 4,24", 13, RED, 700))
    sx, sy = 5, 15
    parts.append(
        f'<line x1="{px(4) + sx}" y1="{py(1) + sy}" x2="{px(12) + sx}" y2="{py(3) + sy}" '
        f'stroke="{RED}" stroke-width="1.8" stroke-dasharray="6 5"/>'
    )
    parts.append(text((px(4) + px(12)) / 2 + 20, (py(1) + py(3)) / 2 + 36, "P a G: 8,25", 13, RED, 700, "middle"))
    labels = {
        "P": (px(4) - 2, py(1) + 24, "middle"),
        "F": (px(3) - 4, py(1) - 12, "middle"),
        "C": (px(1) + 12, py(4) - 6, "start"),
        "G": (px(12), py(3) - 14, "middle"),
    }
    for key, _, _, color in GEO_PUNTOS:
        lx, ly, anchor = labels[key]
        parts.append(text(lx, ly, key, 16, color, 800, anchor))
    parts.append(rect(24, 388, 632, 64, CARD, LINE, 12))
    for index, (key, label, (x, y), color) in enumerate(GEO_PUNTOS):
        col, row = index % 2, index // 2
        parts.append(text(40 + col * 316, 414 + row * 24, f"{key}  {label}  ({x}, {y})", 13, color, 700))
    parts.append(text(24, 480, "La guía G apunta al mismo sitio que la pregunta P, pero es tres veces más larga.", 14, MUTED))
    parts.append(text(24, 502, "En línea recta queda más lejos que la cafetería. La distancia euclídea se equivoca.", 14, MUTED))
    save(
        "03-flechas.svg",
        "\n".join(parts),
        "Cuatro textos como flechas en dos ejes",
        "P, F y G apuntan hacia matrícula; C hacia cafetería. G es tres veces más larga que P. En línea recta, P queda a 8,25 de G y a 4,24 de C.",
        680,
        522,
    )


def normalizar_2d() -> None:
    ox, oy, radio = 70, 320, 250
    parts = [text(24, 34, "Normalizar: todas las flechas a longitud 1", 18, INK, 650)]
    parts.append(
        f'<path d="M {ox + radio} {oy} A {radio} {radio} 0 0 0 {ox} {oy - radio}" fill="none" '
        f'stroke="{LINE}" stroke-width="2" stroke-dasharray="5 5"/>'
    )
    parts.append(f'<line x1="{ox}" y1="{oy}" x2="{ox + radio + 20}" y2="{oy}" stroke="{INK}" stroke-width="1.5"/>')
    parts.append(f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{oy - radio - 20}" stroke="{INK}" stroke-width="1.5"/>')
    parts.append(text(ox + radio, oy + 20, "1", 12, MUTED, 500, "middle"))
    parts.append(text(ox - 12, oy - radio + 4, "1", 12, MUTED, 500, "end"))
    unit = []
    for key, label, (x, y), color in GEO_PUNTOS:
        n = (x * x + y * y) ** 0.5
        unit.append((key, color, x / n, y / n))
    for key, color, ux, uy in unit:
        if key == "G":
            continue
        tx, ty = ox + ux * radio, oy - uy * radio
        parts.append(f'<line x1="{ox}" y1="{oy}" x2="{tx:.1f}" y2="{ty:.1f}" stroke="{color}" stroke-width="3"/>')
        parts.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="6" fill="{color}"/>')
    p_tip = (ox + unit[0][2] * radio, oy - unit[0][3] * radio)
    f_tip = (ox + unit[1][2] * radio, oy - unit[1][3] * radio)
    c_tip = (ox + unit[2][2] * radio, oy - unit[2][3] * radio)
    parts.append(f'<circle cx="{p_tip[0]:.1f}" cy="{p_tip[1]:.1f}" r="11" fill="none" stroke="{GREEN}" stroke-width="2.5"/>')
    parts.append(text(p_tip[0] - 30, p_tip[1] + 38, "P y G, en el mismo punto", 13, INDIGO, 700))
    parts.append(text(f_tip[0] + 16, f_tip[1] - 6, "F, muy cerca", 13, TEAL, 700))
    parts.append(text(c_tip[0] + 14, c_tip[1] + 2, "C, lejos", 13, ORANGE, 700))
    parts.append(rect(456, 70, 248, 214, CARD, LINE, 14))
    lines = [
        ("Se divide cada flecha", INK, 650),
        ("por su longitud.", INK, 650),
        ("", INK, 400),
        ("La dirección no cambia.", MUTED, 400),
        ("La longitud pasa a ser 1.", MUTED, 400),
        ("", INK, 400),
        ("Ahora la línea recta y el", MUTED, 400),
        ("ángulo dan el mismo orden:", MUTED, 400),
        ("G, F y después C.", INK, 650),
    ]
    y = 100
    for content, color, weight in lines:
        if content:
            parts.append(text(474, y, content, 14, color, weight))
        y += 21
    parts.append(text(24, 364, "Titan normaliza en la propia llamada. Por eso en DocIA+ la longitud del texto no manda.", 14, MUTED))
    save(
        "03-normalizar.svg",
        "\n".join(parts),
        "Normalizar deja todas las flechas con longitud 1",
        "Tras dividir por la longitud, la pregunta y la guía larga caen en el mismo punto del arco. La formalización queda muy cerca y la cafetería, lejos.",
        720,
        384,
    )


def indices() -> None:
    parts = []
    parts.append(rect(20, 20, 340, 320, CARD, LINE, 16))
    parts.append(text(190, 52, "Búsqueda exacta", 18, INK, 700, "middle"))
    parts.append(text(190, 74, "Mira todos los fragmentos", 13, MUTED, 400, "middle"))
    # star query
    qx, qy = 190, 230
    parts.append(f'<circle cx="{qx}" cy="{qy}" r="9" fill="{ORANGE}"/>')
    dots = [(70, 120), (120, 140), (250, 130), (300, 170), (80, 190), (140, 210), (260, 200), (310, 240), (100, 260), (230, 270)]
    for dx, dy in dots:
        parts.append(f'<line x1="{qx}" y1="{qy}" x2="{dx}" y2="{dy}" stroke="#f3c7a5" stroke-width="1.5"/>')
        parts.append(f'<circle cx="{dx}" cy="{dy}" r="6" fill="{INDIGO}"/>')
    parts.append(f'<circle cx="{qx}" cy="{qy}" r="9" fill="{ORANGE}"/>')
    parts.append(text(190, 296, "Unos 1.200 fragmentos", 13, MUTED, 400, "middle"))
    parts.append(text(190, 314, "caben en milisegundos", 13, MUTED, 400, "middle"))

    parts.append(rect(380, 20, 340, 320, CARD, LINE, 16))
    parts.append(text(550, 52, "Índice HNSW", 18, INK, 700, "middle"))
    parts.append(text(550, 74, "Salta por un grafo de vecinos", 13, MUTED, 400, "middle"))
    nodes = {
        "a": (470, 120),
        "b": (560, 110),
        "c": (640, 130),
        "d": (500, 180),
        "e": (590, 175),
        "f": (450, 240),
        "g": (540, 230),
        "h": (650, 220),
        "q": (600, 270),
    }
    edges = [("a", "b"), ("b", "c"), ("a", "d"), ("b", "e"), ("d", "e"), ("d", "f"), ("e", "g"), ("c", "h"), ("g", "h"), ("f", "g"), ("g", "q"), ("e", "q")]
    path = {("e", "q"), ("b", "e"), ("a", "b")}
    for u, v in edges:
        color = ORANGE if (u, v) in path or (v, u) in path else LINE
        width = 3 if color == ORANGE else 1.5
        x1, y1 = nodes[u]
        x2, y2 = nodes[v]
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"/>')
    for key, (nx, ny) in nodes.items():
        fill = ORANGE if key == "q" else INDIGO
        parts.append(f'<circle cx="{nx}" cy="{ny}" r="8" fill="{fill}"/>')
    parts.append(text(550, 308, "Si ef es bajo, puede perder el vecino", 13, MUTED, 400, "middle"))
    save(
        "04-exacta-vs-hnsw.svg",
        "\n".join(parts),
        "Búsqueda exacta frente al índice HNSW",
        "La búsqueda exacta compara la pregunta con todos los fragmentos. HNSW recorre un grafo y puede no devolver el vecino exacto si el ancho de búsqueda es corto.",
        740,
        360,
    )


def registro() -> None:
    rows = [
        ("Identificador", "oferta-iabd-2026_000", "Único y estable"),
        ("Vector", "1024 números, norma 1", "Sirve para ordenar"),
        ("Texto", "Procedimiento de formalización…", "Es lo que se cita"),
        ("Metadatos", "g4 · 2026-2027 · página 2", "Sirven para filtrar"),
    ]
    parts = [text(28, 40, "Un fragmento dentro de la colección", 20, INK, 650)]
    y = 60
    for title, value, why in rows:
        parts.append(rect(24, y, 640, 58, CARD, LINE, 12))
        parts.append(rect(24, y, 150, 58, INDIGO_SOFT, INDIGO_SOFT, 12, 0))
        parts.append(rect(160, y, 14, 58, INDIGO_SOFT, INDIGO_SOFT, 0, 0))
        parts.append(text(36, y + 35, title, 15, INDIGO, 650))
        parts.append(text(190, y + 26, value, 15, INK, 650))
        parts.append(text(190, y + 46, why, 13, MUTED))
        y += 70
    save(
        "05-registro.svg",
        "\n".join(parts),
        "Las cuatro piezas de un registro",
        "Cada fragmento guarda identificador, vector, texto citable y metadatos.",
        688,
        y + 8,
    )


def filtro() -> None:
    cats = [
        ("g1", "Programaciones", False),
        ("g2", "Proyecto educativo", False),
        ("g3", "Planes", False),
        ("g4", "Oferta educativa", True),
        ("g5", "Horarios", False),
    ]
    parts = [text(24, 36, "El filtro actúa antes de quedarse con los 5", 18, INK, 650)]
    parts.append(rect(24, 56, 300, 44, CARD, LINE, 22))
    parts.append(text(40, 84, "¿Puedo acceder con un grado medio?", 14, INK, 500))
    parts.append(text(24, 126, "where categoria = g4", 14, INDIGO, 650))
    y = 150
    for code, name, keep in cats:
        fill = GREEN_SOFT if keep else "#eef0f6"
        stroke = GREEN if keep else LINE
        ink = INK if keep else "#8b93a7"
        parts.append(rect(24, y, 250, 36, fill, stroke, 10))
        parts.append(text(40, y + 24, f"{code}  {name}", 14, ink, 650 if keep else 400))
        if not keep:
            parts.append(text(250, y + 24, "fuera", 13, MUTED, 500, "end"))
        else:
            parts.append(text(250, y + 24, "entra", 13, GREEN, 700, "end"))
        y += 44
    parts.append(rect(340, 168, 250, 150, GREEN_SOFT, GREEN, 16, 2))
    parts.append(text(465, 210, "Top 5", 20, GREEN, 700, "middle"))
    parts.append(text(465, 238, "ya son de oferta", 15, INK, 500, "middle"))
    parts.append(text(465, 262, "educativa", 15, INK, 500, "middle"))
    parts.append(text(465, 290, "k cuenta solo estos", 13, MUTED, 400, "middle"))
    parts.append(f'<line x1="274" y1="330" x2="340" y2="250" stroke="{GREEN}" stroke-width="2" marker-end="url(#flecha)"/>')
    save(
        "06-filtro.svg",
        "\n".join(parts),
        "El filtro de categoría entra en la consulta",
        "Si se piden cinco resultados y luego se tiran los que no son g4, el fragmento correcto puede quedar fuera. El where va dentro de la consulta.",
        620,
        400,
    )


def chunking() -> None:
    parts = [text(24, 36, "Un documento, varios fragmentos con solape", 18, INK, 650)]
    parts.append(rect(24, 52, 700, 36, "#eef0f6", LINE, 8))
    parts.append(text(36, 75, "PDF entero: acceso + contenidos + evaluación + bibliografía", 14, MUTED))
    chunks = [
        (24, INDIGO, "Fragmento 0", "Acceso"),
        (268, TEAL, "Fragmento 1", "Contenidos"),
        (512, ORANGE, "Fragmento 2", "Evaluación"),
    ]
    for x, color, title, detail in chunks:
        parts.append(rect(x, 128, 190, 72, CARD, color, 12, 2))
        parts.append(text(x + 95, 158, title, 15, INK, 650, "middle"))
        parts.append(text(x + 95, 180, detail, 14, MUTED, 400, "middle"))
        parts.append(
            f'<line x1="{x+95}" y1="200" x2="{x+95}" y2="236" stroke="{color}" stroke-width="2" marker-end="url(#flecha)"/>'
        )
        parts.append(f'<circle cx="{x+95}" cy="254" r="10" fill="{color}"/>')
    for bridge in (214, 458):
        parts.append(rect(bridge, 146, 54, 36, "#fff8e1", ORANGE, 8, 1.5))
        parts.append(text(bridge + 27, 169, "solape", 12, ORANGE, 700, "middle"))
    parts.append(text(24, 292, "Cada círculo es un vector. El solape repite un trozo", 14, MUTED))
    parts.append(text(24, 314, "para no cortar la frase que responde a la pregunta.", 14, MUTED))
    save(
        "07-fragmentos.svg",
        "\n".join(parts),
        "El documento se parte en fragmentos que se solapan",
        "Cada fragmento tiene su propio vector. El solape repite un trozo para no partir la frase que responde a la pregunta.",
        748,
        340,
    )


def actualizacion() -> None:
    parts = [text(24, 34, "Actualizar calendario-2026 sin dejar huérfanos", 18, INK, 650)]
    parts.append(text(24, 58, "Antes: cuatro fragmentos", 14, MUTED))
    old = [
        (24, "_000", "igual", GREEN_SOFT, GREEN),
        (180, "_001", "ha cambiado", "#fff8e1", ORANGE),
        (336, "_002", "ya no está", RED_SOFT, RED),
        (492, "_003", "ya no está", RED_SOFT, RED),
    ]
    for x, name, state, fill, stroke in old:
        parts.append(rect(x, 76, 144, 64, fill, stroke, 12, 2))
        parts.append(text(x + 72, 104, name, 16, INK, 700, "middle"))
        parts.append(text(x + 72, 124, state, 13, stroke, 500, "middle"))
    parts.append(text(24, 176, "Después", 14, MUTED))
    parts.append(rect(24, 192, 200, 78, GREEN_SOFT, GREEN, 12, 2))
    parts.append(text(124, 222, "_000 se queda", 15, GREEN, 700, "middle"))
    parts.append(text(124, 244, "el hash coincide: no hay llamada", 12, MUTED, 400, "middle"))
    parts.append(rect(244, 192, 200, 78, "#fff8e1", ORANGE, 12, 2))
    parts.append(text(344, 222, "_001 upsert", 15, ORANGE, 700, "middle"))
    parts.append(text(344, 244, "mismo id, vector nuevo", 12, MUTED, 400, "middle"))
    parts.append(rect(464, 192, 200, 78, RED_SOFT, RED, 12, 2))
    parts.append(text(564, 222, "_002 y _003", 15, RED, 700, "middle"))
    parts.append(text(564, 244, "delete", 12, RED, 500, "middle"))
    save(
        "08-actualizacion.svg",
        "\n".join(parts),
        "Qué ocurre al reindexar un documento más corto",
        "El fragmento igual no vuelve a pasar por Titan. El que cambió se sustituye. Los que sobran se borran.",
        688,
        294,
    )


def recall() -> None:
    # Exercise 7: hits on 1,2,3,5,7. Miss 4 (rank 8), 6, 8.
    rows = [
        ("1", True, "dentro del top 5"),
        ("2", True, "dentro del top 5"),
        ("3", True, "dentro del top 5"),
        ("4", False, "sale en el puesto 8"),
        ("5", True, "dentro del top 5"),
        ("6", False, "no aparece"),
        ("7", True, "dentro del top 5"),
        ("8", False, "no aparece"),
    ]
    parts = [text(24, 34, "Ejemplo de recall@5: 5 de 8", 18, INK, 650)]
    parts.append(text(24, 56, "Es el ejercicio 7, no una medida del corpus del IES.", 13, MUTED))
    y = 74
    for number, hit, detail in rows:
        fill = GREEN_SOFT if hit else RED_SOFT
        color = GREEN if hit else RED
        mark = "sí" if hit else "no"
        parts.append(rect(24, y, 420, 32, fill, fill, 8, 0))
        parts.append(text(40, y + 22, f"Pregunta {number}", 14, INK, 650))
        parts.append(text(160, y + 22, mark, 14, color, 700))
        parts.append(text(210, y + 22, detail, 14, MUTED))
        y += 38
    parts.append(rect(460, 74, 200, 120, CARD, LINE, 16))
    parts.append(text(560, 112, "62,5 %", 28, RED, 700, "middle"))
    parts.append(text(560, 140, "objetivo: más del 80 %", 13, MUTED, 400, "middle"))
    parts.append(text(560, 164, "con k entre 3 y 5", 13, MUTED, 400, "middle"))
    save(
        "09-recall.svg",
        "\n".join(parts),
        "Recall en cinco de ocho preguntas de ejemplo",
        "Cinco preguntas tienen el documento esperado entre los cinco primeros fragmentos. Eso es un 62,5 por ciento, por debajo del objetivo del proyecto.",
        684,
        y + 8,
    )


def arquitectura() -> None:
    boxes = [
        (24, 64, 210, "Comunidad educativa", "pregunta en la web", CARD, LINE, INK),
        (280, 64, 180, "API", "solo ella consulta", CARD, LINE, INK),
        (510, 28, 220, "ChromaDB", "colección privada", INDIGO_SOFT, INDIGO, INDIGO),
        (510, 140, 220, "Titan v2", "vector de la pregunta", CARD, LINE, INK),
        (280, 200, 180, "S3", "originales y copias", CARD, LINE, INK),
    ]
    parts = [text(24, 22, "ChromaDB no se abre a internet", 18, INK, 650)]
    for x, y, w, title, detail, fill, stroke, color in boxes:
        parts.append(rect(x, y, w, 78, fill, stroke, 14, 2 if stroke == INDIGO else 1.5))
        parts.append(text(x + w / 2, y + 34, title, 16, color, 700, "middle"))
        parts.append(text(x + w / 2, y + 56, detail, 13, MUTED, 400, "middle"))
    parts.append(f'<line x1="234" y1="103" x2="276" y2="103" stroke="{INDIGO}" stroke-width="2" marker-end="url(#flecha)"/>')
    parts.append(f'<line x1="460" y1="86" x2="506" y2="67" stroke="{INDIGO}" stroke-width="2" marker-end="url(#flecha)"/>')
    parts.append(f'<line x1="460" y1="120" x2="506" y2="160" stroke="{INDIGO}" stroke-width="2" marker-end="url(#flecha)"/>')
    parts.append(text(24, 308, "La web habla con la API. La API habla con la base.", 14, MUTED))
    save(
        "10-arquitectura.svg",
        "\n".join(parts),
        "La web no consulta ChromaDB directamente",
        "Quien busca en la colección es la API. Los documentos originales y las copias viven aparte.",
        754,
        336,
    )


def origen_orden() -> None:
    parts = []
    parts.append(rect(20, 20, 330, 280, RED_SOFT, "#f5c6c2", 16))
    parts.append(text(185, 52, "Lo que parece", 18, RED, 700, "middle"))
    parts.append(rect(48, 76, 274, 52, CARD, LINE, 12))
    parts.append(text(185, 108, "Primero el chatbot RAG", 15, INK, 650, "middle"))
    parts.append(f'<line x1="185" y1="128" x2="185" y2="158" stroke="{RED}" stroke-width="2" marker-end="url(#flecha-roja)"/>')
    parts.append(rect(48, 162, 274, 52, CARD, LINE, 12))
    parts.append(text(185, 194, "Luego se inventa la base", 15, INK, 650, "middle"))
    parts.append(text(185, 268, "Ese orden es al revés", 16, RED, 700, "middle"))

    parts.append(rect(370, 20, 330, 280, GREEN_SOFT, "#b7dfb9", 16))
    parts.append(text(535, 52, "Lo que ocurrió", 18, GREEN, 700, "middle"))
    hechos = ["Fotos y música parecidas", "Un índice para millones", "La base de datos, 2019", "El RAG la usa, 2020"]
    y = 72
    for hecho in hechos:
        parts.append(rect(394, y, 282, 36, CARD, LINE, 10))
        parts.append(text(535, y + 24, hecho, 14, INK, 650, "middle"))
        y += 42
    parts.append(text(535, 268, "La base ya existía", 16, GREEN, 700, "middle"))
    save(
        "00-origen-orden.svg",
        "\n".join(parts),
        "La base vectorial no se inventó para el chatbot",
        "El orden real es búsqueda de parecidos, índice, base de datos en 2019 y RAG en 2020.",
        720,
        320,
    )


def origen_linea() -> None:
    steps = [
        ("1975", "La idea", "Un documento ya podía ser un vector"),
        ("2017", "El índice", "Faiss busca parecidos entre millones de fotos"),
        ("2019", "La base de datos", "Milvus guarda, filtra y borra vectores"),
        ("2020", "El RAG", "Recupera texto y después redacta"),
        ("2023", "Se hace famosa", "Los chatbots la usan. Ahí entra DocIA+"),
    ]
    parts = [text(28, 36, "Cinco fechas, en orden", 20, INK, 650)]
    y = 56
    for year, title, detail in steps:
        here = year == "2019"
        fill = INDIGO_SOFT if here else CARD
        stroke = INDIGO if here else LINE
        parts.append(rect(24, y, 520, 72, fill, stroke, 14, 2 if here else 1.5))
        parts.append(rect(40, y + 16, 72, 40, INDIGO if here else INDIGO_SOFT, INDIGO, 10, 0))
        parts.append(text(76, y + 42, year, 14, "#ffffff" if here else INDIGO, 700, "middle"))
        parts.append(text(128, y + 32, title, 16, INK, 650))
        parts.append(text(128, y + 54, detail, 14, MUTED))
        y += 84
    save(
        "00-origen-linea.svg",
        "\n".join(parts),
        "Línea de tiempo de las bases de datos vectoriales",
        "La idea es de 1975, el índice de 2017, el producto de 2019 y el RAG de 2020. DocIA+ está en el uso famoso de 2023.",
        568,
        y + 8,
    )


def origen_libreria() -> None:
    parts = []
    parts.append(rect(20, 24, 300, 250, CARD, LINE, 16))
    parts.append(rect(20, 24, 300, 52, "#eceff1", "#eceff1", 16, 0))
    parts.append(rect(20, 60, 300, 16, "#eceff1", "#eceff1", 0, 0))
    parts.append(text(170, 56, "Faiss, 2017", 18, INK, 700, "middle"))
    parts.append(text(170, 96, "Una librería", 14, MUTED, 500, "middle"))
    for i, item in enumerate(["Busca vectores cercanos", "Aguanta millones", "No guarda el texto", "No filtra ni borra"]):
        parts.append(text(48, 136 + i * 30, item, 15, INK, 500))
    parts.append(rect(340, 24, 300, 250, INDIGO_SOFT, INDIGO, 16, 2))
    parts.append(rect(340, 24, 300, 52, INDIGO, INDIGO, 16, 0))
    parts.append(rect(340, 60, 300, 16, INDIGO, INDIGO, 0, 0))
    parts.append(text(490, 56, "ChromaDB", 18, "#ffffff", 700, "middle"))
    parts.append(text(490, 96, "Una base de datos", 14, INDIGO, 650, "middle"))
    for i, item in enumerate(["Busca vectores cercanos", "Guarda el texto citable", "Filtra por categoría", "Actualiza, borra y copia"]):
        parts.append(text(368, 136 + i * 30, item, 15, INK, 500))
    save(
        "00-origen-libreria.svg",
        "\n".join(parts),
        "Un índice no es todavía una base de datos",
        "Faiss busca parecidos. ChromaDB además guarda el texto, filtra, actualiza y borra.",
        660,
        298,
    )


def mapa_2d() -> None:
    def px(x):
        return 70 + x * 460

    def py(y):
        return 390 - y * 300

    parts = [text(24, 32, "Un mapa de dos ejes, solo para verlo", 18, INK, 650)]
    parts.append(f'<line x1="70" y1="390" x2="560" y2="390" stroke="{INK}" stroke-width="1.5"/>')
    parts.append(f'<line x1="70" y1="390" x2="70" y2="70" stroke="{INK}" stroke-width="1.5"/>')
    parts.append(text(300, 418, "más formal  →", 13, MUTED, 500, "middle"))
    parts.append(
        f'<text x="22" y="230" text-anchor="middle" fill="{MUTED}" font-family="Segoe UI, sans-serif" font-size="13" font-weight="500" transform="rotate(-90 22 230)">más trámite de estudios  →</text>'
    )
    points = [
        (0.85, 0.90, "Matrícula en el ciclo", INDIGO),
        (0.83, 0.88, "Inscripción en el curso", TEAL),
        (0.10, 0.20, "Horario de cafetería", ORANGE),
    ]
    # halo around the two close points
    cx = (px(0.85) + px(0.83)) / 2
    cy = (py(0.90) + py(0.88)) / 2
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="46" fill="{INDIGO_SOFT}" stroke="{INDIGO}" stroke-dasharray="4 4"/>')
    for x, y, label, color in points:
        parts.append(f'<circle cx="{px(x)}" cy="{py(y)}" r="8" fill="{color}"/>')
    parts.append(text(px(0.85) + 16, py(0.90) - 8, "Matrícula en el ciclo", 14, INK, 650))
    parts.append(text(px(0.83) + 16, py(0.88) + 18, "Inscripción en el curso", 14, INK, 650))
    parts.append(text(px(0.10) + 14, py(0.20) + 4, "Horario de cafetería", 14, INK, 650))
    parts.append(text(24, 448, "Las dos de matrícula quedan juntas. La cafetería, no.", 14, MUTED))
    parts.append(text(24, 470, "Un embedding real usa 384 o 1024 ejes. Este dibujo solo tiene 2.", 14, MUTED))
    save(
        "00-mapa-2d.svg",
        "\n".join(parts),
        "Mapa de dos ejes con tres frases del centro",
        "Matrícula e inscripción quedan juntas. El horario de cafetería queda lejos. Los ejes son didácticos.",
        760,
        496,
    )


def sql_vs_mapa() -> None:
    parts = []
    parts.append(rect(16, 16, 300, 250, RED_SOFT, "#f5c6c2", 16))
    parts.append(text(166, 48, "MySQL", 18, RED, 700, "middle"))
    parts.append(rect(32, 68, 268, 64, CARD, LINE, 10))
    parts.append(text(44, 92, "LIKE '%matricula%'", 14, INK, 650))
    parts.append(text(44, 114, "busca esa cadena", 13, MUTED))
    parts.append(rect(32, 148, 268, 64, CARD, LINE, 10))
    parts.append(text(44, 172, "El texto dice «inscripción»", 13, INK, 500))
    parts.append(text(44, 194, "0 filas", 16, RED, 700))
    parts.append(rect(332, 16, 300, 250, GREEN_SOFT, "#b7dfb9", 16))
    parts.append(text(482, 48, "Mapa de vectores", 18, GREEN, 700, "middle"))
    parts.append(f'<circle cx="400" cy="148" r="10" fill="{INDIGO}"/>')
    parts.append(f'<circle cx="448" cy="132" r="10" fill="{TEAL}"/>')
    parts.append(f'<circle cx="560" cy="188" r="10" fill="{ORANGE}"/>')
    parts.append(text(348, 128, "matrícula", 13, INK, 650))
    parts.append(text(462, 116, "inscripción", 13, INK, 650))
    parts.append(text(468, 168, "cafetería", 13, INK, 650))
    parts.append(text(482, 230, "Mide la distancia", 15, INK, 650, "middle"))
    parts.append(text(482, 252, "y encuentra las dos", 15, GREEN, 700, "middle"))
    save(
        "00-sql-vs-mapa.svg",
        "\n".join(parts),
        "MySQL busca la palabra y el mapa busca la cercanía",
        "LIKE matricula no encuentra un texto que dice inscripción. En el mapa las dos frases están juntas.",
        648,
        282,
    )


def main() -> None:
    mapa_2d()
    sql_vs_mapa()
    origen_orden()
    origen_linea()
    origen_libreria()
    pipeline()
    modulos()
    categorias()
    literal()
    embedding_io()
    dimensiones()
    perfiles()
    coseno()
    mapa_significado()
    texto_a_vector()
    flechas_2d()
    normalizar_2d()
    indices()
    registro()
    filtro()
    chunking()
    actualizacion()
    recall()
    arquitectura()
    print(f"Escritos en {OUT}")


if __name__ == "__main__":
    main()
