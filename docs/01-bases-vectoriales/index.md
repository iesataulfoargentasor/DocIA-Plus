# Bases de datos vectoriales

Unidad previa a la implementación del almacén de embeddings de DocIA+. Si el grupo no ha visto nunca una base vectorial, se empieza por la [sesión 1](sesion-01.md). Los temas 1 a 10 vienen después. Cada tema cierra con la consecuencia práctica para ChromaDB.

## Mapa

| Tema | Pregunta que responde |
| --- | --- |
| [Sesión 1. Ver la base vectorial](sesion-01.md) | Del dato en bruto al vector, ver esa lista y las primeras operaciones en ChromaDB |
| [Por qué existen](00-por-que-existen.md) | Cuándo aparecen y por qué no nacieron para el RAG |
| [1. Búsqueda literal y semántica](01-busqueda-literal-y-semantica.md) | Por qué una base SQL o un `grep` no bastan |
| [2. Embeddings](02-embeddings.md) | Qué es el vector y qué modelo lo produce en DocIA+ |
| [3. Geometría y similitud](03-geometria-y-similitud.md) | Cómo se decide que dos textos «se parecen» |
| [4. Búsqueda e índices](04-busqueda-e-indices.md) | Cómo se encuentra el vecino más cercano sin mirar todo, y cuándo sí se puede mirar todo |
| [5. Anatomía](05-anatomia-bd-vectorial.md) | Qué objetos existen dentro de la base |
| [6. Metadatos y filtros](06-metadatos-y-filtros.md) | Cómo conviven las cinco categorías en una sola colección |
| [7. Del documento al vector](07-chunking-y-ciclo-de-indexacion.md) | Qué se indexa exactamente y en qué orden |
| [8. Operaciones de gestión](08-operaciones-de-gestion.md) | Altas, consultas, cambios, bajas y copias |
| [9. Calidad y fallos](09-calidad-y-fallos.md) | Cómo mediremos el 80 % y qué errores son típicos |
| [10. ChromaDB en DocIA+](10-chromadb-en-docia.md) | Cómo encajan todas las piezas en el proyecto, con medidas reales |

## Secuencia de aula sugerida

Pensada para unas siete sesiones compartidas o repartidas entre SBD y BDA. La primera recorre el camino del dato al vector: no da por sabido el embedding. Se puede comprimir el resto si el grupo ya ha visto similitud en otro módulo.

| Sesión | Trabajo | Encargo dominante |
| --- | --- | --- |
| 1 | [Sesión 1](sesion-01.md): del dato al vector, la lista a la vista y ChromaDB en Colab | Los dos |
| 2 | Por qué existen, y temas 1 y 2, con los dos vídeos de CodelyTV | Los dos |
| 3 | Tema 3 y laboratorio de geometría | Los dos |
| 4 | Tema 4 | Los dos, con más peso conceptual en BDA |
| 5 | Temas 5 y 6, y el esquema de metadatos | SBD |
| 6 | Temas 7 y 8, y ChromaDB local con vectores escritos a mano | BDA, con SBD revisando metadatos |
| 7 | Temas 9 y 10, y ejercicios | Los dos |

## Convenios de vocabulario

En el aula usaremos estas palabras con un solo significado:

| Palabra | Significado en DocIA+ |
| --- | --- |
| Documento | Fichero de origen: un PDF, un DOCX o una página |
| Fragmento o *chunk* | Trozo de ese documento que se convierte en un solo vector |
| Embedding | El vector de números que representa el significado del fragmento o de la pregunta |
| Colección | El conjunto de fragmentos dentro de ChromaDB. En DocIA+ habrá una colección principal |
| Consulta | El vector de la pregunta del usuario, más los filtros de metadatos |
| Distancia | El número que ChromaDB devuelve para ordenar resultados. No es la similitud: hay que saber en qué espacio está calculada |

«Indexar» significa dejar el fragmento escrito en la colección, con su vector y sus metadatos, listo para ser recuperado.
