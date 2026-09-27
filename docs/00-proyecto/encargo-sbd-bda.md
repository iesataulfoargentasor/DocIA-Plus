# El encargo de SBD y BDA

DocIA+ se evalúa con los instrumentos ordinarios de cada módulo. Esta unidad prepara dos encargos concretos. No sustituye al resto de la programación.

## Sistemas de Big Data

En SBD el corpus del IES es un conjunto heterogéneo: PDF, Word y páginas web, de varios departamentos, con fechas y versiones distintas. El resultado de aprendizaje que el proyecto ancla aquí es el de gestionar y explotar datos de naturaleza diversa.

Sobre la base vectorial, el trabajo de SBD es:

- extraer el texto y limpiarlo (cabeceras repetidas, páginas en blanco, duplicados, documentos obsoletos);
- unificar fuentes distintas en un mismo formato de fragmento;
- **definir metadatos, categorías y la estructura de la colección**.

Esa última frase es el criterio de evaluación que esta unidad desmenuza. Una colección sin metadatos de categoría, fuente y posición no sirve para citar, ni para que cada grupo trabaje su documentación, ni para borrar solo lo que ha caducado.

## Big Data Aplicado

En BDA el encargo es un pipeline de procesamiento sobre el sistema donde viven los datos: transformar documentos en vectores semánticos y dejarlos almacenados en ChromaDB. El cuadro de mando de analítica (consultas frecuentes, latencia, casos sin contexto suficiente) es la otra mitad del módulo dentro del proyecto, y se aborda cuando la base ya recibe datos reales.

En esta unidad BDA tiene que salir sabiendo:

- qué entra y qué sale de un modelo de embeddings;
- por qué el vector de la pregunta y el vector del documento tienen que salir del **mismo** modelo, con la **misma** dimensión y la **misma** normalización;
- qué operaciones de escritura, consulta, actualización y borrado va a implementar el pipeline;
- qué se rompe si se reindexa mal (identificadores inestables, vectores de otro modelo, fragmentos huérfanos).

## Lo que queda fuera de estos dos módulos

| Pieza | Módulo que la lidera | Por qué no es el primer paso |
| --- | --- | --- |
| Arquitectura RAG, estrategia fina de recuperación y API FastAPI | PIA | Pregunta a una colección que todavía hay que entender |
| Widget en la web del IES | PIA, con revisión de la empresa colaboradora | Depende de la API |
| Amazon Bedrock como redactor de respuestas | PIA | No interviene en cómo se guardan los vectores |
| Servidor local del centro, fase final | Coordinación técnica | Llega cuando el sistema cloud ya funciona |

## Criterio de «esto ya se entiende»

La unidad está asentada cuando un grupo puede explicar, sin leer los apuntes, estas seis decisiones:

1. Guardamos **fragmentos**, no documentos enteros.
2. Cada fragmento es un registro con identificador, texto, vector y metadatos.
3. La búsqueda ordena por **similitud del coseno** en el espacio de Titan Embeddings v2 (vectores normalizados).
4. La categoría documental es un **filtro**, no un vector más.
5. Actualizar un documento es un `upsert` de sus fragmentos y un borrado de los fragmentos que ya no existen.
6. Cambiar de modelo de embeddings obliga a **reconstruir la colección**.

El [laboratorio](../../laboratorio/README.md) comprueba la geometría y las operaciones con vectores escritos a mano, para no mezclar todavía el aprendizaje de la base de datos con el de la cuenta de AWS.
