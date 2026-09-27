# DocIA+

Repositorio de trabajo del proyecto de innovación **DocIA+** (modalidad Tecno-Innova+, convocatoria Innova+ Activa 2026-2027) del IES Ataúlfo Argenta, Castro Urdiales.

La carpeta local se llama `DocIA+`. En GitHub el repositorio es [iesataulfoargentasor/DocIA-Plus](https://github.com/iesataulfoargentasor/DocIA-Plus): el carácter `+` no está permitido en el nombre de un repositorio.

DocIA+ es un asistente de consulta sobre la documentación oficial del centro. El alumnado del Curso de Especialización en Inteligencia Artificial y Big Data construye un sistema RAG: los documentos se dividen en fragmentos, cada fragmento se convierte en un embedding y esos vectores se guardan en **ChromaDB** para recuperar, ante una pregunta, los fragmentos más cercanos en significado.

Este repositorio empieza por ahí. Antes de implementar el almacenamiento, hay que entender qué es una base de datos vectorial y qué se le va a pedir en este proyecto.

## Para quién es este material

- **SBD (Sistemas de Big Data, 5074).** Preparar el corpus y definir metadatos, categorías y estructura de la base vectorial.
- **BDA (Big Data Aplicado, 5075).** Diseñar el pipeline que genera embeddings y los almacena en ChromaDB.

Programación de Inteligencia Artificial (PIA) construye después la API y la lógica de recuperación. Esta primera unidad deja el terreno común de los tres módulos.

## Cómo leerlo

La unidad didáctica está en [`docs/`](docs/index.md). El orden recomendado es el de esa página de inicio.

El sitio publicado para el alumnado está en [https://iesataulfoargentasor.github.io/DocIA-Plus/](https://iesataulfoargentasor.github.io/DocIA-Plus/). Las soluciones de los ejercicios no van en esa web: siguen en `docs/docente/` del repositorio.

Para verla en local:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-docs.txt
mkdocs serve
```

La primera práctica es la sesión 1, con dos cuadernos de Colab en [`laboratorio/colab/`](laboratorio/colab/). El laboratorio local, sin AWS y sin modelos de pago, está en [`laboratorio/`](laboratorio/README.md).

## Qué hay y qué no hay todavía

Hay explicación, un esquema de metadatos propuesto para discutir en clase, la sesión 1 (mapa, vector a la vista y ChromaDB en Colab) y dos prácticas locales que enseñan la geometría y las operaciones de ChromaDB con vectores escritos a mano.

No hay todavía pipeline de indexación, cuenta de AWS, Amazon Titan ni API FastAPI. Eso viene cuando esta unidad esté asentada y concretemos el trabajo sobre la base vectorial del proyecto.

## Licencia

Código y material didáctico de este repositorio: [MIT](LICENSE).
