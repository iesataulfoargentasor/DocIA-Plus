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
                """# Cuaderno de la sesión 1. Ver el vector antes de guardarlo

En este cuaderno no hay base de datos. El objetivo es obtener un vector y mirarlo.

Un modelo de embeddings ya entrenado convierte una frase en una lista de números. Esa lista es el vector: la posición de la frase en un mapa de muchas dimensiones. No es un resumen y no es una traducción. No se lee número a número.

El modelo de esta sesión es gratuito y entiende español (`paraphrase-multilingual-MiniLM-L12-v2`). Devuelve **384** números porque así se construyó. En DocIA+ el modelo del proyecto será Amazon Titan y devolverá **1024**. Son dos mapas distintos. No se mezclan.

Las frases son de ejercicio y ya son cortas: cada una es el trozo. No son documentos oficiales del IES.

La primera ejecución descarga el modelo, unos 450 MB. Puede tardar un par de minutos. No lo estamos entrenando; lo estamos usando.
"""
            ),
            md(
                """## Instalar

Python no trae un modelo de embeddings. Esta línea descarga la librería que sabe cargar uno.

`sentence-transformers` es el programa. El modelo, `paraphrase-multilingual-MiniLM-L12-v2`, se bajará en la celda siguiente, la primera vez que se use. Sin esta librería no hay función que convierta texto en números.
"""
            ),
            code(
                """!pip install sentence-transformers -q
print("Librería instalada")
"""
            ),
            md(
                """## Convertir una frase en una lista de números

`SentenceTransformer(...)` carga el modelo en memoria. `encode` es el embedding: entra la frase y sale la lista.

`normalize_embeddings=True` pide que la lista tenga **longitud 1**. Es lo mismo que hará Titan en DocIA+, y en el tema 3 se ve por qué conviene. Lo usaremos en todas las llamadas.

Imprimimos el texto, cuántos números tiene, su longitud y solo los diez primeros. Tienen que salir 384 números y longitud 1,0. Los diez primeros bastan para ver que son decimales, no palabras. El número 7, solo, no significa nada. El significado aparece al comparar la lista completa con otra lista del mismo modelo.

El modelo no redacta y no contesta a la frase. Solo la coloca en el mapa.
"""
            ),
            code(
                """import numpy as np
from sentence_transformers import SentenceTransformer

modelo = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

frase = "Procedimiento de formalización de matrícula en el curso de especialización."
vector = modelo.encode(frase, normalize_embeddings=True)

print("Texto:")
print(frase)
print()
print("Cuántos números tiene el vector:", len(vector))
print("Longitud del vector:", round(float(np.linalg.norm(vector)), 4))
print("Los 10 primeros:")
print(vector[:10])
"""
            ),
            md(
                """## Medir quién está cerca

La cercanía es una propiedad de los vectores. No hace falta una base de datos para verla.

Se convierten tres frases con el mismo modelo. Python resta dos listas y mide lo larga que queda esa resta. Eso es una distancia. Número más pequeño, más cerca.

Esta cuenta es la longitud de la resta entre dos listas. No es el número que imprime ChromaDB en el cuaderno siguiente. Allí, con el espacio coseno, la distancia es 1 menos el coseno. Las dos se leen igual (más pequeña, más cerca), pero tienen escalas distintas y no se comparan entre sí.

Tiene que quedar más cerca «matrícula» de «inscripción» (alrededor de 0,83) que de «cafetería» (alrededor de 1,38). Las dos primeras hablan del mismo trámite con otras palabras. La tercera no. Si saliera al revés, las tres frases no se habrían codificado con el mismo modelo.
"""
            ),
            code(
                """frases = {
    "matrícula": "Procedimiento de formalización de matrícula en el curso de especialización.",
    "inscripción": "Instrucciones para inscribirse en el curso.",
    "cafetería": "Menú diario de la cafetería del instituto.",
}
vectores = {nombre: modelo.encode(texto, normalize_embeddings=True) for nombre, texto in frases.items()}

cerca = np.linalg.norm(vectores["matrícula"] - vectores["inscripción"])
lejos = np.linalg.norm(vectores["matrícula"] - vectores["cafetería"])

print(f"Distancia matrícula - inscripción: {cerca:.4f}")
print(f"Distancia matrícula - cafetería:   {lejos:.4f}")
print()
if cerca < lejos:
    print("La inscripción queda más cerca de la matrícula que la cafetería.")
else:
    print("El resultado no cuadra: revisa que las tres frases se han codificado con el mismo modelo.")
"""
            ),
        ]
    )

    nb2 = nb(
        [
            md(
                '<a href="https://colab.research.google.com/github/iesataulfoargentasor/DocIA-Plus/blob/main/laboratorio/colab/02_chromadb_paso_a_paso.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>'
            ),
            md(
                """# Cuaderno de la sesión 1. ChromaDB con el modelo

En el cuaderno anterior el vector vivía en una variable y se perdía al cerrar la sesión. Una base de datos lo guarda para poder buscarlo después.

Este cuaderno no es el laboratorio de vectores escritos a mano. Aquel viene después, en la carpeta `laboratorio/`, y no descarga un modelo.

ChromaDB es la base que usaremos en DocIA+. Aquí trabaja dentro de Colab. Primero en memoria, y al final en una carpeta.

Cada registro guarda cuatro cosas, y cada una tiene un motivo:

- `ids`: identificador único, para actualizar o borrar ese registro y no otro
- `documents`: el texto del trozo, porque el vector no se puede leer ni citar
- `embeddings`: la lista de números, calculada por nosotros con el mismo modelo de antes
- `metadatas`: datos para filtrar, por ejemplo la categoría. No forman parte del vector

Si solo pasáis el texto y no el vector, ChromaDB llama a un modelo que no veis. Puede no ser el de 384 números. En este cuaderno no se hace así.

Las frases siguen siendo de ejercicio.
"""
            ),
            md(
                """## Instalar y cargar el mismo modelo

Hace falta la librería de la base (`chromadb`) y otra vez el modelo del cuaderno anterior.

Se imprime la dimensión. Tiene que salir 384. Si no sale 384, este cuaderno y el anterior no están en el mismo mapa y las distancias no significan nada.
"""
            ),
            code(
                """!pip install chromadb sentence-transformers -q

from sentence_transformers import SentenceTransformer

modelo = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
print("Modelo listo. Dimensiones:", modelo.get_sentence_embedding_dimension())
"""
            ),
            md(
                """## Crear la colección

En SQL, antes de insertar filas se crea la tabla. Aquí se crea la colección: el sitio donde vivirán los registros.

`EphemeralClient` la guarda solo en memoria. Al cerrar el cuaderno desaparece. Más adelante veréis la que se escribe en disco.

`hnsw:space = cosine` le dice cómo medir. Hoy basta con esto: en esta colección, una distancia más pequeña significa más parecido. El coseno se calcula a mano en el tema 3.

Si la colección ya existía de una ejecución anterior, se borra y se crea vacía. Así no se mezclan pruebas viejas.
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
print("Colección creada:", coleccion.name)
"""
            ),
            md(
                """## Guardar cinco frases

Este es el paso de cargar la base. Cada frase ya es un trozo, así que no hay que partirla.

Primero `encode` calcula las cinco listas con el modelo que acabamos de cargar, con longitud 1 como en el cuaderno anterior. Después `add` las guarda. El orden importa: el vector que entra es el nuestro. La base no lo inventa.

La categoría es un metadato. Sirve para filtrar, como un `WHERE`. No cambia los números del vector.

Usamos los mismos códigos que el proyecto: `g4` oferta educativa, `g5` horarios y actividades del centro, `g3` planes. El texto de la frase no es la categoría. «Secretaría» puede aparecer en el texto y el código seguir siendo `g4`.
"""
            ),
            code(
                """frases = [
    "Procedimiento de formalización de matrícula en el curso de especialización.",
    "Para matricularse hay que presentar la solicitud en secretaría.",
    "El horario de la cafetería del centro es de 8:00 a 14:00.",
    "Las pruebas de acceso a ciclos formativos se realizan en junio.",
    "El plan de orientación ayuda al alumnado a elegir estudios.",
]
categorias = [
    {"categoria": "g4", "fuente": "ejemplo-oferta"},
    {"categoria": "g4", "fuente": "ejemplo-acceso"},
    {"categoria": "g5", "fuente": "ejemplo-horarios"},
    {"categoria": "g4", "fuente": "ejemplo-acceso"},
    {"categoria": "g3", "fuente": "ejemplo-orientacion"},
]
ids = ["doc1", "doc2", "doc3", "doc4", "doc5"]
vectores = modelo.encode(frases, normalize_embeddings=True).tolist()

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

Antes de preguntar, se comprueba que la base ha guardado lo que le hemos dado.

Pedimos el registro `doc1` con su texto y su vector. La longitud tiene que ser 384, la misma del cuaderno anterior. Si la base hubiera llamado a otro modelo a escondidas, esta comprobación fallaría.
"""
            ),
            code(
                """interno = coleccion.get(ids=["doc1"], include=["embeddings", "documents"])
texto = interno["documents"][0]
vector = interno["embeddings"][0]
print("Texto:", texto)
print("Dimensiones:", len(vector))
print("Diez primeros números:", [round(float(x), 4) for x in vector[:10]])
"""
            ),
            md(
                """## Preguntar con otras palabras

La pregunta también es un dato. Hay que convertirla en vector con el mismo modelo y comparar esa lista con las que están guardadas. `query_embeddings` hace la comparación. `n_results=2` pide solo los dos vecinos más cercanos.

La frase no contiene «formalización» ni «matrícula». Un `LIKE` no encontraría la primera frase. La base vectorial sí puede, porque no busca las letras: busca el punto más cercano.

Tienen que salir primero las dos frases de matrícula: `doc1`, a una distancia de unos 0,37, y `doc2`, a unos 0,48.

La distancia que imprime ChromaDB en esta colección es 1 menos el coseno: más pequeña cuanto más se parecen, y 0 si los vectores son iguales. No es la resta de listas del cuaderno anterior. No compares este 0,37 con el 0,83 de aquella cuenta: son escalas distintas.
"""
            ),
            code(
                """pregunta = "¿Cómo me inscribo en el curso?"
vector_pregunta = modelo.encode([pregunta], normalize_embeddings=True).tolist()
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

La cercanía y el filtro no son la misma cosa.

La pregunta es amplia. Sin filtro podrían salir textos de varias categorías. `where` obliga a que la categoría sea `g4` (oferta educativa), igual que un `WHERE` en SQL. Eso no crea otro vector: quita registros y, entre los que quedan, ordena por cercanía.

Si el filtro se aplicara después de pedir los dos más cercanos, se podría perder un texto de oferta que iba en el puesto 3. Por eso va dentro de la misma consulta.

Tienen que salir solo frases `g4`: la de matricularse en secretaría y la de las pruebas de acceso.
"""
            ),
            code(
                """pregunta = "¿Cuándo hay que hacer los trámites?"
vector_pregunta = modelo.encode([pregunta], normalize_embeddings=True).tolist()
filtrados = coleccion.query(
    query_embeddings=vector_pregunta,
    n_results=2,
    where={"categoria": "g4"},
)
print("Pregunta:", pregunta)
print("Filtro: categoria = g4")
print()
for doc, meta in zip(filtrados["documents"][0], filtrados["metadatas"][0]):
    print("-", doc, f"({meta['categoria']})")
"""
            ),
            md(
                """## Memoria y disco

La colección de arriba es un cálculo en memoria. Al cerrar Colab desaparece. Una base de datos tiene que seguir ahí mañana.

`PersistentClient` escribe una carpeta. Se guardan los mismos cinco registros, se cierra el cliente y se abre otro apuntando a la misma carpeta. Si el recuento sigue siendo 5, los vectores han sobrevivido fuera de la variable.

En Colab, esta carpeta pertenece al disco temporal del entorno. Puede desaparecer cuando Colab elimina la máquina. Descargar el .ipynb no descarga la base: hay que conservar los originales y el código de reconstrucción, o exportar una copia consistente fuera del entorno. Abrir otro cliente sobre la misma carpeta solo demuestra persistencia en ese disco.

En el proyecto la carpeta no estará en Colab: estará en el servidor. La idea es la misma.
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

1. Añade el texto «El centro dispone de aparcamiento para bicicletas.» con el id `doc6` y la categoría `g5`.
2. Calcula tú el vector con `modelo.encode(..., normalize_embeddings=True)`. No dejes que ChromaDB lo invente.
3. Pregunta «¿Dónde puedo dejar la bicicleta?» y pide un solo resultado.
4. Imprime el texto y la distancia.

Tiene que salir la frase de las bicicletas, categoría `g5`, a una distancia de unos 0,37. La siguiente frase queda por encima de 0,88.
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
