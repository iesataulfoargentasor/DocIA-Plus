# DocIA+ · Unidad de bases de datos vectoriales

Material de aula del Curso de Especialización en Inteligencia Artificial y Big Data del IES Ataúlfo Argenta, para los módulos **SBD** (Sistemas de Big Data) y **BDA** (Big Data Aplicado). El proyecto de innovación DocIA+ ya está concedido. Esta unidad es su primer paso técnico: **entender la base de datos donde se guardará la documentación del centro, antes de construirla.**

No hace falta saber nada de inteligencia artificial para seguirla. Cada tema empieza desde cero, trabaja con números que se pueden comprobar a mano y usa siempre el mismo ejemplo.

## Qué es DocIA+

DocIA+ es un asistente para consultar la documentación oficial del IES. Una familia, un alumno o un docente escribe una pregunta con sus palabras y recibe una respuesta que **cita el documento de donde sale**.

La pregunta que usaremos en toda la unidad es esta:

> ¿Cómo me matriculo?

Y el documento que la responde dice:

> Procedimiento de formalización de matrícula.

## El problema: buscar por palabras no basta

Una base de datos de las que ya conocéis busca por letras. Con SQL:

```sql
SELECT texto FROM fragmentos WHERE LOWER(texto) LIKE '%matriculo%';
```

No devuelve **ninguna fila**. «Matriculo» no es un trozo de «matrícula»: cambian la tilde y la última letra. Para una persona las dos frases hablan de lo mismo, pero `LIKE` no mira el significado, solo las letras.

La **búsqueda semántica** («del significado») compara de qué habla cada texto. Con los cuatro textos del ejemplo, el resultado es este:

| Puesto | Texto | Parecido con «¿Cómo me matriculo?» (de 0 a 1) |
| --- | --- | --- |
| 1 | Procedimiento de formalización de matrícula | 0,997 |
| 2 | Plazo de inscripción en el ciclo | 0,970 |
| 3 | Menú diario de la cafetería | 0,471 |
| 4 | Precio del bocadillo | 0,243 |

Los dos textos que responden salen primero, sin repetir ninguna palabra de la pregunta. Estos números son de juguete: en el [tema 1](01-bases-vectoriales/01-busqueda-literal-y-semantica.md) se ve de dónde salen y en el [tema 3](01-bases-vectoriales/03-geometria-y-similitud.md) se calculan a mano.

## Dónde entra la base de datos vectorial

Para comparar significados, un modelo convierte cada texto en una lista de números, llamada **vector** o **embedding**. Los textos que hablan de lo mismo reciben listas parecidas. Una **base de datos vectorial** guarda esas listas junto con su texto y, dada la lista de una pregunta, devuelve deprisa las más parecidas.

![Seis pasos: la pregunta, su conversión en números, la búsqueda en ChromaDB, los fragmentos más cercanos, la comprobación de si están lo bastante cerca y la redacción de la respuesta.](assets/esquemas/00-pipeline.svg)

En DocIA+ esa base es **ChromaDB**, y el modelo que convierte texto en números es **Amazon Titan Embeddings v2**, que da 1024 números por texto. Los documentos no se guardan enteros: se cortan en **fragmentos** de unos pocos párrafos, y cada fragmento tiene su vector.

Esta unidad se ocupa de los pasos 3 y 4: que ChromaDB tenga fragmentos buenos y los devuelva bien. También enseña a medir el paso 5. La redacción de la respuesta, el paso 6, corresponde más adelante a PIA (Programación de Inteligencia Artificial).

## Qué tiene que conseguir la base

El proyecto fija un objetivo que se puede comprobar:

- al menos **80 documentos** del centro indexados;
- ante cada pregunta, devolver los **3 a 5 fragmentos** más relevantes;
- que el fragmento correcto esté entre ellos en **más del 80 %** de las preguntas de prueba.

Los documentos se organizan en cinco categorías, una por grupo de trabajo, que dentro de la base se escriben `g1` a `g5`: programaciones, proyecto educativo, planes y programas, oferta educativa y horarios o actividades. Se explican en [Qué vamos a construir](00-proyecto/que-vamos-a-construir.md).

## Un ejemplo que recorre los diez temas

Cada tema añade una pieza al mismo caso, «¿Cómo me matriculo?»:

| Tema | Qué le pasa a la pregunta |
| --- | --- |
| [1. Búsqueda literal y semántica](01-bases-vectoriales/01-busqueda-literal-y-semantica.md) | `LIKE` no la encuentra. Buscar por significado sí |
| [2. Embeddings](01-bases-vectoriales/02-embeddings.md) | La pregunta y el documento se convierten en 1024 números cada uno |
| [3. Geometría y similitud](01-bases-vectoriales/03-geometria-y-similitud.md) | Se calcula cuánto se parecen: coseno 0,997 |
| [4. Búsqueda e índices](01-bases-vectoriales/04-busqueda-e-indices.md) | Se encuentra el más parecido sin comparar con todos los fragmentos |
| [5. Anatomía](01-bases-vectoriales/05-anatomia-bd-vectorial.md) | El fragmento se guarda como un registro: `oferta-iabd-2026_000`, con texto, vector y metadatos |
| [6. Metadatos y filtros](01-bases-vectoriales/06-metadatos-y-filtros.md) | Un filtro por curso deja fuera la versión de 2023, que se parece igual |
| [7. Del documento al vector](01-bases-vectoriales/07-chunking-y-ciclo-de-indexacion.md) | El PDF de la oferta se corta por secciones antes de convertirlo |
| [8. Operaciones de gestión](01-bases-vectoriales/08-operaciones-de-gestion.md) | Si el documento cambia, se actualiza sin dejar fragmentos viejos |
| [9. Calidad y fallos](01-bases-vectoriales/09-calidad-y-fallos.md) | Se mide si sale entre los 5 primeros y cuándo decir «no lo sé» |
| [10. ChromaDB en DocIA+](01-bases-vectoriales/10-chromadb-en-docia.md) | Todo junto: de la web a la respuesta, con medidas reales |

## Cómo está organizada

| Bloque | Para qué sirve |
| --- | --- |
| [Qué vamos a construir](00-proyecto/que-vamos-a-construir.md) | El producto, las cinco categorías documentales y el sitio de la base vectorial |
| [El encargo de SBD y BDA](00-proyecto/encargo-sbd-bda.md) | Qué parte del currículo cubre este trabajo y qué no |
| [Cómo seguir la unidad](01-bases-vectoriales/index.md) | El mapa de temas, una secuencia de siete sesiones y el vocabulario común |
| [Sesión 1](01-bases-vectoriales/sesion-01.md) | Primer contacto: del dato al vector y ChromaDB en Colab, con un modelo real |
| [Temas 1 a 10](01-bases-vectoriales/01-busqueda-literal-y-semantica.md) | Las bases de datos vectoriales, con DocIA+ como hilo |
| [Laboratorio local](https://github.com/iesataulfoargentasor/DocIA-Plus/blob/main/laboratorio/README.md) | Dos scripts con vectores escritos a mano, sin cuenta de AWS |
| [Ejercicios](01-bases-vectoriales/ejercicios.md) | Diez ejercicios en papel, cada uno en la sesión de su tema |

## Orden de lectura

1. El proyecto: [Qué vamos a construir](00-proyecto/que-vamos-a-construir.md) y [El encargo de SBD y BDA](00-proyecto/encargo-sbd-bda.md).
2. [Sesión 1](01-bases-vectoriales/sesion-01.md), en Colab.
3. [Por qué existen](01-bases-vectoriales/00-por-que-existen.md) las bases vectoriales.
4. Temas 1 a 4: por qué hace falta un vector, qué es, cómo se comparan dos y cómo se busca entre muchos.
5. Laboratorio de geometría, [`01_geometria_similitud.py`](https://github.com/iesataulfoargentasor/DocIA-Plus/blob/main/laboratorio/01_geometria_similitud.py), después del tema 3.
6. Temas 5 a 8: qué se guarda, cómo se filtra, cómo entra un documento y cómo se mantiene.
7. Laboratorio de ChromaDB, [`02_chromadb_coleccion.py`](https://github.com/iesataulfoargentasor/DocIA-Plus/blob/main/laboratorio/02_chromadb_coleccion.py), después de los temas 7 y 8.
8. Temas 9 y 10: cómo se mide si la base funciona y cómo encaja todo en el proyecto.
9. [Ejercicios](01-bases-vectoriales/ejercicios.md). Cada uno se hace en la sesión de su tema, según la [secuencia de aula](01-bases-vectoriales/index.md#secuencia-de-aula). Al final de la unidad se repasan juntos.

Una advertencia para no confundirse: el primer cuaderno de Colab mide la diferencia entre dos vectores restando sus listas. El laboratorio y los temas usan la **distancia coseno** de ChromaDB, que es 1 menos el parecido (tema 3). Son números distintos y no se comparan entre sí.

## Cómo leer cada tema

- **Empieza desde cero.** Cada palabra nueva se explica la primera vez que aparece.
- **Trabaja con un ejemplo con números.** Casi siempre, el de la matrícula.
- **Tiene esquemas** para ver la idea antes de leer la explicación.
- **Lo que dice de ChromaDB está comprobado** con la versión 1.1.0, la del laboratorio.
- **Termina con «Comprueba que lo has entendido»**: preguntas con la respuesta plegada. Intenta contestar antes de abrirla.

## Seis palabras que vas a leer mucho

| Palabra | Qué significa en DocIA+ |
| --- | --- |
| Documento | El fichero original: un PDF, un DOCX o una página web |
| Fragmento | Un trozo de ese documento, de unos pocos párrafos, que se convierte en un solo vector |
| Vector o embedding | La lista de números que representa de qué habla un fragmento o una pregunta |
| Colección | El conjunto de fragmentos guardados en ChromaDB. Es lo parecido a una tabla |
| Metadatos | Datos que acompañan a cada fragmento, como su categoría o su curso, y que sirven para filtrar |
| Distancia | El número que devuelve ChromaDB para ordenar resultados. Cuanto más pequeña, más parecido |
