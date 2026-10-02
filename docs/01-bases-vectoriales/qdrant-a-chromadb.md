# De Qdrant a ChromaDB

Qdrant nos permite observar colecciones, vectores y metadatos en una consola. ChromaDB será la base del proyecto. Aprendemos primero las operaciones comunes y después comprobamos qué cambia entre ambas herramientas.

## El recorrido de clase

1. En la [sesión 1](sesion-01.md), hacer el mapa y el cuaderno **Ver el vector**. Reservar el segundo cuaderno, de ChromaDB, para la transición.
2. Trabajar la [introducción comentada a Qdrant](https://colab.research.google.com/drive/1Xq0OPU6QwyTMVoBjcTGVH5oyakT0MkAk?usp=sharing), por partes: película, paráfrasis y filtro.
3. Resolver el [reto de recursos educativos](https://colab.research.google.com/drive/1dJyARi0sBpsZrfcPSTY_DHkKI-Euk-P4?usp=sharing). Reservar unas dos horas y tiempo para explicar los resultados.
4. Trasladar el catálogo a ChromaDB con el segundo cuaderno de la sesión 1 como referencia.
5. Sustituir el catálogo por documentos del centro, según los temas 7 a 10.

La versión comentada desarrolla el mismo código del cuaderno original: no es necesario realizar ambos. Los Colab enlazados son materiales externos; las indicaciones de esta página no modifican sus celdas.

## Preparar las prácticas de Qdrant

- Usar `getpass` o los secretos de Colab para las credenciales. No copiar claves a celdas o salidas compartidas.
- El cuaderno comentado conserva borrados de colecciones con nombres fijos. Trabajar en una colección propia y revisar los borrados antes de ejecutar. El reto usa memoria por defecto y crea un nombre único.
- Los Colab usan `all-MiniLM-L6-v2`. Compararlo con el modelo multilingüe de la web usando las mismas consultas; no atribuir automáticamente a la base los errores de recuperación en español.
- Al cambiar el modelo, crear otra colección, recalcular todos los vectores y comprobar su dimensión. No mezclar espacios aunque tengan el mismo tamaño.
- Interpretar «Filtros híbridos» como **búsqueda vectorial con filtros de metadatos**. No hay combinación de búsqueda léxica y vectorial en esa práctica.
- Registrar las versiones utilizadas. Una demostración con cinco registros no demuestra rendimiento con datos masivos.

## Qué cambia entre las bases

| Idea | Qdrant | ChromaDB |
| --- | --- | --- |
| Registro | Punto: ID, vector y payload | ID, embedding, documento y metadatos |
| Texto | Un campo del payload en estas prácticas | `documents` |
| Buscar | `query_points` | `query` |
| Filtrar | `query_filter` | `where` |
| Coseno | Score mayor: más similar | Distancia menor: más próximo |
| Identificador | Entero o UUID | Cadena |
| Actualizar metadatos | `set_payload` | `update` con `metadatas` |

La dimensión sale del modelo. En ambas bases, el filtro restringe los candidatos y la similitud los ordena. Para la configuración coseno, distancia = 1 − similitud; no trasladamos umbrales entre modelos.

## Práctica de transición

**BDA (3 horas).** Exportar los ocho recursos del reto, conservar sus embeddings y convertir los IDs a cadenas. Crear una colección de ChromaDB en espacio coseno con los mismos vectores, textos y metadatos. Repetir tres consultas, incluida una ajena al catálogo, con y sin filtro. Comparar IDs y orden, teniendo en cuenta posibles empates y aproximaciones numéricas.

**SBD (2 horas).** Revisar qué campo se vectoriza, qué texto se puede citar y qué campos permiten filtrar. Proponer el registro de un documento real del grupo: fuente, categoría, curso, sección e identificador. Detectar campos ausentes y datos de vigencia dudosa.

**Entrega:** tabla de resultados, explicación de similitud frente a distancia y un registro documental validado. No basta una captura de una búsqueda que parece funcionar.

El modelo permanece fijo durante esta comparación. El salto a Titan se realiza después en una colección nueva; así se distingue el cambio de base del cambio de representación.

??? question "¿Puede ChromaDB devolver números distintos y el mismo orden que Qdrant?"
    Sí. Con los mismos vectores y coseno, Qdrant presenta similitud y ChromaDB distancia. Una similitud de 0,8 corresponde a una distancia de 0,2. Ninguna es una probabilidad de respuesta correcta.

??? question "¿Un filtro por categoría mejora el embedding?"
    No. Selecciona qué registros pueden participar. Puede excluir un fragmento relevante si la categoría elegida es incorrecta.
