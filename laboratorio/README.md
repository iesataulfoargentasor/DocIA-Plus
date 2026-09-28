# Laboratorio local

Estos dos scripts no son los cuadernos de la sesión 1. Los cuadernos están en [`colab/`](colab/) y descargan un modelo. Aquí los vectores están escritos en el código, para calcular la geometría y las operaciones de la base sin confundirlas con el modelo.

El orden es este: primero la [sesión 1](../docs/01-bases-vectoriales/sesion-01.md), después la geometría de esta página, y al llegar a los temas 7 y 8 el script de ChromaDB. En un embedding real nadie asigna «el eje 1 es matrícula». Aquí sí, porque son tres números didácticos.

La distancia de este ChromaDB es 1 menos el coseno. No es la resta de listas del cuaderno «ver el vector». Las categorías son `g1` a `g5`, las mismas que en el proyecto y en el cuaderno de Colab.

## Entorno

Desde la raíz del repositorio:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-lab.txt
```

La geometría puede ejecutarse sin instalar ChromaDB.

## Geometría, con vectores escritos a mano

```powershell
python laboratorio/01_geometria_similitud.py
```

Qué tiene que observarse:

- Al preguntar «¿cómo me matriculo?», el primer texto es «Procedimiento de formalización de matrícula» (coseno cerca de 0,998), por delante de «Cómo me matriculo en el ciclo». El documento que no copia las palabras de la pregunta gana. Los dos quedan muy por encima de horas del módulo y de convivencia.
- La pregunta por las horas del módulo invierte el ranking y coloca primero el fragmento de las 190 horas.
- El producto escalar y el coseno no coinciden en los vectores sin normalizar que imprime la segunda parte del script (`2` frente a `0,707`). Esa es la razón de pedir a Titan vectores de norma 1.

Si el ranking de matrícula no sale así, no se sigue al script de ChromaDB local: el fallo está en la cuenta.

## ChromaDB local, con vectores escritos a mano

```powershell
python laboratorio/02_chromadb_coleccion.py
```

Crea `laboratorio/data/`, ignorado por git. Se puede borrar entero para repetir la práctica.

Qué tiene que observarse, en este orden:

1. Dos vectores idénticos dan distancia 0.
2. En esta versión (ChromaDB 1.1.0, espacio `cosine`) la distancia es **1 menos el coseno**. El fragmento de matrícula, con coseno cerca de 0,998, sale con distancia cerca de 0,002.
3. La consulta «¿cómo me matriculo?» devuelve primero el fragmento de formalización de matrícula, categoría `g4`.
4. La misma consulta filtrada con `categoria = g2` solo devuelve el plan de convivencia, con una distancia mucho mayor. El filtro gana a la similitud.
5. Tras simular una versión nueva del calendario, los fragmentos `_002` y `_003` desaparecen y `_001` queda con el texto nuevo.
6. `get` por `doc_id` lista esos fragmentos sin vector de consulta.

Esa distancia es la que se interpreta en clase con esta versión de la librería. No se copia un umbral de otro proyecto.

## Qué no demuestra este laboratorio

No demuestra que Titan entienda los documentos del IES. Los vectores están puestos para que la geometría sea obvia. Cuando el vector lo calcule un modelo, el ranking dejará de ser perfecto y entrará en juego la medida del tema 9.
