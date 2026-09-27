"""Operaciones de una colección ChromaDB, con vectores escritos a mano.

No descarga un modelo: los embeddings se pasan en cada llamada. El
directorio laboratorio/data se puede borrar para repetir la práctica.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import chromadb


RAIZ = Path(__file__).resolve().parent
DATOS = RAIZ / "data"

# Misma geometría que en 01_geometria_similitud.py
MATRICULA = [0.90, 0.10, 0.00]
COMO_MATRICULARSE = [0.85, 0.20, 0.05]
HORAS = [0.05, 0.95, 0.00]
CONVIVENCIA = [0.00, 0.05, 0.90]
PREGUNTA_MATRICULA = [0.88, 0.15, 0.02]


def preparar_coleccion() -> chromadb.Collection:
    if DATOS.exists():
        shutil.rmtree(DATOS)
    cliente = chromadb.PersistentClient(path=str(DATOS))
    return cliente.create_collection(
        name="docia_lab",
        metadata={"hnsw:space": "cosine"},
    )


def indexar(coleccion: chromadb.Collection) -> None:
    coleccion.upsert(
        ids=[
            "oferta-iabd-2026_000",
            "oferta-iabd-2026_001",
            "pec-2026_000",
            "calendario-2026_000",
            "calendario-2026_001",
            "calendario-2026_002",
            "calendario-2026_003",
        ],
        embeddings=[
            MATRICULA,
            HORAS,
            CONVIVENCIA,
            HORAS,
            HORAS,
            HORAS,
            HORAS,
        ],
        documents=[
            "Procedimiento de formalización de matrícula del curso de especialización.",
            "El módulo de Big Data Aplicado tiene una duración de 190 horas.",
            "El plan de convivencia regula la vida del centro.",
            "Calendario escolar, fragmento 0.",
            "Calendario escolar, fragmento 1, versión antigua.",
            "Calendario escolar, fragmento 2, que desaparecerá.",
            "Calendario escolar, fragmento 3, que desaparecerá.",
        ],
        metadatas=[
            {"categoria": "g4", "doc_id": "oferta-iabd-2026", "chunk": 0, "curso": "2026-2027"},
            {"categoria": "g4", "doc_id": "oferta-iabd-2026", "chunk": 1, "curso": "2026-2027"},
            {"categoria": "g2", "doc_id": "pec-2026", "chunk": 0, "curso": "2026-2027"},
            {"categoria": "g5", "doc_id": "calendario-2026", "chunk": 0, "curso": "2026-2027"},
            {"categoria": "g5", "doc_id": "calendario-2026", "chunk": 1, "curso": "2026-2027"},
            {"categoria": "g5", "doc_id": "calendario-2026", "chunk": 2, "curso": "2026-2027"},
            {"categoria": "g5", "doc_id": "calendario-2026", "chunk": 3, "curso": "2026-2027"},
        ],
    )


def mostrar(titulo: str, resultado: dict) -> None:
    print(f"\n{titulo}")
    documentos = resultado["documents"][0]
    distancias = resultado["distances"][0]
    metadatos = resultado["metadatas"][0]
    for documento, distancia, metadato in zip(documentos, distancias, metadatos):
        print(f"  distancia={distancia:0.4f}  categoria={metadato['categoria']}  {documento}")


def actualizar_calendario(coleccion: chromadb.Collection) -> None:
    """Simula el tema 8: el fragmento 1 cambia y los fragmentos 2 y 3 se retiran."""
    coleccion.upsert(
        ids=["calendario-2026_001"],
        embeddings=[CONVIVENCIA],
        documents=["Calendario escolar, fragmento 1, versión nueva."],
        metadatas=[
            {"categoria": "g5", "doc_id": "calendario-2026", "chunk": 1, "curso": "2026-2027"}
        ],
    )
    coleccion.delete(ids=["calendario-2026_002", "calendario-2026_003"])


def main() -> None:
    coleccion = preparar_coleccion()
    indexar(coleccion)

    identicos = coleccion.query(query_embeddings=[MATRICULA], n_results=1)
    distancia_identica = identicos["distances"][0][0]
    print(f"Distancia de un vector consigo mismo: {distancia_identica:0.4f}")
    if distancia_identica > 1e-6:
        raise SystemExit("En espacio coseno, un vector idéntico debería quedar a distancia 0")

    mostrar(
        "¿Cómo me matriculo? Sin filtro de categoría",
        coleccion.query(query_embeddings=[PREGUNTA_MATRICULA], n_results=3),
    )
    mostrar(
        "La misma pregunta, solo proyecto educativo (g2)",
        coleccion.query(
            query_embeddings=[PREGUNTA_MATRICULA],
            n_results=3,
            where={"categoria": "g2"},
        ),
    )

    actualizar_calendario(coleccion)
    restantes = coleccion.get(where={"doc_id": "calendario-2026"})
    print("\nFragmentos que quedan de calendario-2026:")
    for identificador, documento in zip(restantes["ids"], restantes["documents"]):
        print(f"  {identificador}  {documento}")

    ids = set(restantes["ids"])
    if ids != {"calendario-2026_000", "calendario-2026_001"}:
        raise SystemExit(f"Huérfanos mal borrados: {sorted(ids)}")
    texto = dict(zip(restantes["ids"], restantes["documents"]))
    if "versión nueva" not in texto["calendario-2026_001"]:
        raise SystemExit("El upsert no ha sustituido el fragmento 1")

    print("\nPráctica correcta: distancia nula, filtro por categoría y calendario sin huérfanos.")


if __name__ == "__main__":
    main()
