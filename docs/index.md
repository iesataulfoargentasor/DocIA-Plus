# DocIA+ · Unidad de bases de datos vectoriales

Material de aula para el Curso de Especialización en Inteligencia Artificial y Big Data del IES Ataúlfo Argenta. El proyecto de innovación DocIA+ ya está concedido. Esta unidad es el primer paso técnico de **SBD** y **BDA**: comprender la base de datos donde vivirán los embeddings, antes de construirla.

## El sistema, en una frase

Una persona escribe una pregunta sobre la documentación del IES. El sistema busca los fragmentos de documento cuyo **significado** se parece a esa pregunta y, con esos fragmentos delante, un modelo de lenguaje redacta la respuesta citando la fuente.

La pieza que hace posible la búsqueda por significado es la **base de datos vectorial**.

![Recorrido de una pregunta en DocIA+. El paso 3, ChromaDB, es la base vectorial de esta unidad.](assets/esquemas/00-pipeline.svg)

En esta unidad nos quedamos en el paso 3: que ChromaDB tenga fragmentos buenos. La redacción de la respuesta corresponde más adelante a PIA.

## Cómo está organizada

| Bloque | Para qué sirve |
| --- | --- |
| [Qué vamos a construir](00-proyecto/que-vamos-a-construir.md) | El producto, las cinco categorías documentales y el sitio de la base vectorial |
| [El encargo de SBD y BDA](00-proyecto/encargo-sbd-bda.md) | Qué parte del currículo cubre este trabajo y qué no |
| [Sesión 1](01-bases-vectoriales/sesion-01.md) | Del dato al vector, un vector impreso y ChromaDB en Colab |
| [Unidad 1 a 10](01-bases-vectoriales/index.md) | Las bases de datos vectoriales, con el caso DocIA+ como hilo |
| [Laboratorio local](https://github.com/iesataulfoargentasor/DocIA-Plus/blob/main/laboratorio/README.md) | Geometría y ChromaDB con vectores escritos a mano, sin cuenta de AWS |

## Orden de lectura

1. Contexto del proyecto.
2. [Sesión 1](01-bases-vectoriales/sesion-01.md): del dato al vector, la lista de números y ChromaDB en Colab, con los códigos `g1` a `g5`.
3. [Por qué existen](01-bases-vectoriales/00-por-que-existen.md) las bases vectoriales.
4. Temas 1 a 4: por qué un vector, cómo se compara y cómo se busca entre muchos.
5. Geometría a mano, en [`laboratorio/01_geometria_similitud.py`](https://github.com/iesataulfoargentasor/DocIA-Plus/blob/main/laboratorio/01_geometria_similitud.py). No es el cuaderno de Colab.
6. Temas 5 a 8: qué se guarda, cómo se filtra por categoría y cómo entra y sale un documento.
7. ChromaDB local con vectores escritos a mano, en [`laboratorio/02_chromadb_coleccion.py`](https://github.com/iesataulfoargentasor/DocIA-Plus/blob/main/laboratorio/02_chromadb_coleccion.py). Aquí la distancia es 1 menos el coseno y la categoría es `g4`, no la resta de listas de la sesión 1.
8. Temas 9 y 10: cómo sabremos si la base está bien y qué decisión de diseño ya está tomada en el proyecto.

Los [ejercicios](01-bases-vectoriales/ejercicios.md) cierran la unidad.
