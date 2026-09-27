"""Crea los cuadernos de la sesión 1. No forma parte de la clase."""

import json
from pathlib import Path


def nb(cells):
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
            "colab": {"provenance": []},
        },
        "cells": cells,
    }


def md(source: str):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source.splitlines(keepends=True),
    }


def code(source: str):
    return {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


def main() -> None:
    out = Path(__file__).resolve().parents[1] / "laboratorio" / "colab"
    out.mkdir(parents=True, exist_ok=True)

    nb1 = nb(
        [
            md(
                """# Práctica 1. Ver el vector antes de guardarlo

En esta práctica no hay base de datos. Un modelo convierte frases en listas de números. Esa lista es el embedding: la posición de la frase en el mapa.

El modelo de esta sesión es pequeño y gratuito (`all-MiniLM-L6-v2`). Devuelve **384** números. En DocIA+ el modelo del proyecto será Amazon Titan y devolverá **1024**. Son dos mapas distintos. No se mezclan.

Las frases son de ejercicio. No son documentos oficiales del IES.

La primera ejecución descarga el modelo. Puede tardar un minuto.
"""
            ),
            md("## Instalar\n"),
            code(
                """!pip install sentence-transformers -q
print("Libreria instalada")
"""
            ),
            md(
                """## Convertir una frase en una lista de números

El modelo no redacta. Solo coloca la frase en el mapa.
"""
            ),
            code(
                """from sentence_transformers import SentenceTransformer

modelo = SentenceTransformer("all-MiniLM-L6-v2")

frase = "Procedimiento de formalizacion de matricula en el curso de especializacion."
vector = modelo.encode(frase)

print("Texto:")
print(frase)
print()
print("Cuantos numeros tiene el vector:", len(vector))
print("Los 10 primeros:")
print(vector[:10])
"""
            ),
            md(
                """## Medir quién está cerca

Número más pequeño significa más cerca. Todavía no hay ChromaDB: la cuenta la hace Python.
"""
            ),
            code(
                """import numpy as np

frases = {
    "matricula": "Procedimiento de formalizacion de matricula en el curso de especializacion.",
    "inscripcion": "Instrucciones para inscribirse en el curso.",
    "cafeteria": "Menu diario de la cafeteria del instituto.",
}
vectores = {nombre: modelo.encode(texto) for nombre, texto in frases.items()}

cerca = np.linalg.norm(vectores["matricula"] - vectores["inscripcion"])
lejos = np.linalg.norm(vectores["matricula"] - vectores["cafeteria"])

print(f"Distancia matricula - inscripcion: {cerca:.4f}")
print(f"Distancia matricula - cafeteria:   {lejos:.4f}")
print()
if cerca < lejos:
    print("La inscripcion queda mas cerca de la matricula que la cafeteria.")
else:
    print("El resultado no cuadra: revisa que las tres frases se han codificado con el mismo modelo.")
"""
            ),
        ]
    )

    nb2 = nb(
        [
            md(
                """# Práctica 2. ChromaDB paso a paso

Ya habéis visto un vector en la práctica 1. Ahora ese vector entra en una base de datos.

ChromaDB es la base del proyecto DocIA+. Aquí trabaja en memoria, dentro de Colab. Al final veréis una colección que sí se escribe en disco.

Cada registro guarda cuatro cosas:

- `ids`: identificador único
- `documents`: el texto que se podría citar
- `embeddings`: la lista de números, calculada por nosotros
- `metadatas`: la categoría, para filtrar

Si solo pasáis el texto y no el vector, ChromaDB llama a un modelo que no veis. En este cuaderno no se hace así.

Las frases siguen siendo de ejercicio.
"""
            ),
            md("## Instalar y cargar el mismo modelo\n"),
            code(
                """!pip install chromadb sentence-transformers -q

from sentence_transformers import SentenceTransformer

modelo = SentenceTransformer("all-MiniLM-L6-v2")
print("Modelo listo. Dimensiones:", modelo.get_sentence_embedding_dimension())
"""
            ),
            md(
                """## Crear la colección

En SQL esto sería una tabla. Aquí se llama colección. El espacio es el coseno: más adelante veréis por qué. Hoy basta con saber que una distancia más pequeña significa más parecido.
"""
            ),
            code(
                """import chromadb

cliente = chromadb.EphemeralClient()
existentes = [c.name for c in cliente.list_collections()]
if "documentacion_ies" in existentes:
    cliente.delete_collection("documentacion_ies")

coleccion = cliente.create_collection(
    name="documentacion_ies",
    metadata={"hnsw:space": "cosine"},
)
print("Coleccion creada:", coleccion.name)
"""
            ),
            md(
                """## Guardar cinco frases

Primero se calcula el vector. Después se guarda, junto con el texto y la categoría.
"""
            ),
            code(
                """frases = [
    "Procedimiento de formalizacion de matricula en el curso de especializacion.",
    "Para matricularse hay que presentar la solicitud en secretaria.",
    "El horario de la cafeteria del centro es de 8:00 a 14:00.",
    "Las pruebas de acceso a ciclos formativos se realizan en junio.",
    "El plan de orientacion ayuda al alumnado a elegir estudios.",
]
categorias = [
    {"categoria": "Oferta Educativa", "fuente": "ejemplo-oferta"},
    {"categoria": "Secretaria", "fuente": "ejemplo-acceso"},
    {"categoria": "Servicios", "fuente": "ejemplo-horarios"},
    {"categoria": "Secretaria", "fuente": "ejemplo-acceso"},
    {"categoria": "Orientacion", "fuente": "ejemplo-orientacion"},
]
ids = ["doc1", "doc2", "doc3", "doc4", "doc5"]
vectores = modelo.encode(frases).tolist()

coleccion.add(
    ids=ids,
    documents=frases,
    embeddings=vectores,
    metadatas=categorias,
)
print("Registros guardados:", coleccion.count())
"""
            ),
            md(
                """## Mirar el vector que quedó dentro

Tiene que salir 384, los mismos que en la práctica 1.
"""
            ),
            code(
                """interno = coleccion.get(ids=["doc1"], include=["embeddings", "documents"])
texto = interno["documents"][0]
vector = interno["embeddings"][0]
print("Texto:", texto)
print("Dimensiones:", len(vector))
print("Diez primeros numeros:", list(vector[:10]))
"""
            ),
            md(
                """## Preguntar con otras palabras

La pregunta no contiene «formalizacion» ni «matricula». El vector de la pregunta se calcula con el mismo modelo y se compara con los que están guardados.
"""
            ),
            code(
                """pregunta = "Como me inscribo en el curso?"
vector_pregunta = modelo.encode([pregunta]).tolist()
resultados = coleccion.query(query_embeddings=vector_pregunta, n_results=2)

print("Pregunta:", pregunta)
print()
for i, doc in enumerate(resultados["documents"][0]):
    distancia = resultados["distances"][0][i]
    categoria = resultados["metadatas"][0][i]["categoria"]
    print(f"{i + 1}. distancia={distancia:.4f}  categoria={categoria}")
    print(f"   {doc}")
    print()
"""
            ),
            md(
                """## Filtrar por categoría

La cercanía y el filtro no son la misma cosa. Aquí la pregunta es amplia, pero solo pueden salir textos de `Secretaria`.
"""
            ),
            code(
                """pregunta = "Cuando hay que hacer los tramites?"
vector_pregunta = modelo.encode([pregunta]).tolist()
filtrados = coleccion.query(
    query_embeddings=vector_pregunta,
    n_results=2,
    where={"categoria": "Secretaria"},
)
print("Pregunta:", pregunta)
print("Filtro: categoria = Secretaria")
print()
for doc, meta in zip(filtrados["documents"][0], filtrados["metadatas"][0]):
    print("-", doc, f"({meta['categoria']})")
"""
            ),
            md(
                """## Memoria y disco

La colección de arriba desaparece al cerrar el cuaderno. Una base de datos también tiene que seguir ahí mañana. `PersistentClient` escribe una carpeta.
"""
            ),
            code(
                """from pathlib import Path

ruta = Path("/content/chroma_ies")
cliente_disco = chromadb.PersistentClient(path=str(ruta))
if "documentacion_ies" in [c.name for c in cliente_disco.list_collections()]:
    cliente_disco.delete_collection("documentacion_ies")

en_disco = cliente_disco.create_collection(
    name="documentacion_ies",
    metadata={"hnsw:space": "cosine"},
)
en_disco.add(ids=ids, documents=frases, embeddings=vectores, metadatas=categorias)

otro = chromadb.PersistentClient(path=str(ruta))
abierta = otro.get_collection("documentacion_ies")
print("Registros al volver a abrir la carpeta:", abierta.count())
print("Carpeta:", ruta)
"""
            ),
            md(
                """## Ejercicio

1. Añade el texto «El centro dispone de aparcamiento para bicicletas.» con el id `doc6` y la categoría `Servicios`.
2. Calcula tú el vector con `modelo.encode`. No dejes que ChromaDB lo invente.
3. Pregunta «Donde puedo dejar la bicicleta?» y pide un solo resultado.
4. Imprime el texto y la distancia.

La distancia tiene que ser pequeña, y la categoría tiene que ser `Servicios`.
"""
            ),
            code(
                """# 1. Calcula el vector de la frase nueva.
# 2. coleccion.add(...) o en_disco.add(...)
# 3. Pregunta y muestra la distancia.
"""
            ),
        ]
    )

    (out / "01_ver_el_vector.ipynb").write_text(
        json.dumps(nb1, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    (out / "02_chromadb_paso_a_paso.ipynb").write_text(
        json.dumps(nb2, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print(out)


if __name__ == "__main__":
    main()
