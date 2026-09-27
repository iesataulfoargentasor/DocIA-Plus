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


def main() -> None:
    pipeline()
    modulos()
    categorias()
    literal()
    embedding_io()
    dimensiones()
    perfiles()
    coseno()
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
