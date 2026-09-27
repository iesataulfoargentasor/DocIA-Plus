# Laboratorio

La primera toma de contacto no es esta carpeta. Es la [sesión 1](../docs/01-bases-vectoriales/sesion-01.md): un mapa en la pizarra y dos cuadernos de Colab en [`colab/`](colab/). Ahí el alumno ve una lista de números de verdad y luego la guarda en ChromaDB.

Las dos prácticas de esta página vienen después. No descargan un modelo. Los vectores están escritos en el código para calcular la geometría a mano. En un embedding real nadie asigna «el eje 1 es matrícula». Aquí sí, porque son tres números didácticos.

## Entorno

Desde la raíz del repositorio:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-lab.txt
```

La práctica 1 puede ejecutarse sin instalar ChromaDB.

## Práctica 1. Geometría

```powershell
python laboratorio/01_geometria_similitud.py
```

Qué tiene que observarse:

- Al preguntar «¿cómo me matriculo?», el primer texto es «Procedimiento de formalización de matrícula» (coseno cerca de 0,998), por delante de «Cómo me matriculo en el ciclo». El documento que no copia las palabras de la pregunta gana. Los dos quedan muy por encima de horas del módulo y de convivencia.
- La pregunta por las horas del módulo invierte el ranking y coloca primero el fragmento de las 190 horas.
- El producto escalar y el coseno no coinciden en los vectores sin normalizar que imprime la segunda parte del script (`2` frente a `0,707`). Esa es la razón de pedir a Titan vectores de norma 1.

Si el ranking de matrícula no sale así, no se sigue a ChromaDB: el fallo está en la cuenta.

## Práctica 2. Colección en ChromaDB

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
