# Ejercicios

Se resuelven en papel o con el laboratorio. No hace falta AWS. Las soluciones están en el material de docente, para corregir después de la puesta en común.

## 1. Dos búsquedas

El documento dice: «Procedimiento de formalización de matrícula del curso de especialización».

La pregunta es: «¿Cómo me matriculo en el ciclo de IA?».

1. Explica por qué una búsqueda literal puede no devolver ese documento.
2. Explica qué tiene que coincidir entre la indexación y la consulta para que una búsqueda semántica tenga sentido.
3. Di una pregunta para la que, al revés, la búsqueda literal sería la herramienta correcta.

## 2. Coseno a mano

Vectores sin normalizar:

```text
a = (2, 0)
b = (1, 1)
c = (0, 3)
```

1. Calcula la norma de `a`, de `b` y de `c`.
2. Calcula el coseno de `a` con `b` y el de `a` con `c`.
3. Ordénalos de mayor a menor similitud respecto de `a`.
4. Calcula el producto escalar de `a` con `b`. ¿Por qué no coincide con el coseno?

## 3. Vectores ya normalizados

Alguien configura Titan con normalización y obtiene, redondeando:

```text
q = (0,6, 0,8)
d1 = (0,6, 0,8)
d2 = (0,8, 0,6)
```

1. Comprueba que la norma de `q` es 1.
2. Calcula la similitud del coseno de `q` con `d1` y con `d2` usando el producto escalar.
3. ¿Cuál devolvería primero una colección en espacio coseno, y qué distancia esperas para `d1` si la distancia es «1 menos el coseno»? Trata esta última regla como hipótesis de lectura: `laboratorio/02_chromadb_coleccion.py` muestra la distancia real que devuelve la versión de ChromaDB fijada en el repositorio. No es la resta de listas del cuaderno de la sesión 1.

## 4. Una colección que no se puede mezclar

Un grupo indexó 40 documentos con Titan a 1024 dimensiones. Otro quiere «probar rápido» consultando con vectores de 256 dimensiones del mismo modelo, porque ocupa menos.

1. ¿Por qué la consulta no es válida?
2. ¿Qué habría que hacer para pasar toda la colección a 256 dimensiones?
3. ¿Por qué no vale con recortar las últimas coordenadas del vector de 1024?

## 5. Estructura de un registro

Documento `plan-igualdad-2026.pdf`, categoría G3, curso 2026-2027, título «Plan de igualdad», sección «Medidas», fragmento número 2 (el tercero, si se numera desde 0). El texto del fragmento es el párrafo de las medidas.

1. Propón el identificador.
2. Lista los metadatos mínimos según el esquema de la unidad.
3. Di dos campos que no deben guardarse, aunque resulte cómodo para depurar.

## 6. Actualizar sin dejar huérfanos

El documento `calendario-2026` tenía 4 fragmentos indexados, con identificadores `_000` a `_003`. La versión nueva, ya fragmentada, solo produce `_000` y `_001`. El hash de `_000` coincide con el almacenado. El de `_001` ha cambiado.

Describe, en orden, las operaciones sobre la colección: qué no se envía a Titan, qué se hace `upsert` y qué se borra.

## 7. Recall@5

Ocho preguntas de prueba. En el top 5, el documento esperado aparece en las preguntas 1, 2, 3, 5 y 7. En la 4 el documento esperado está en la posición 8. En la 6 y la 8 no aparece.

1. Calcula el recall@5.
2. ¿Se cumple el objetivo del proyecto?
3. ¿Cambiaría la respuesta del apartado 2 si el objetivo se midiera con k = 10 y la pregunta 4 pasara a contarse como acierto? Razona si esa forma de medir respetaría lo escrito en el proyecto.

## 8. El filtro que llega tarde

La colección tiene programaciones y oferta educativa. La consulta pide los 5 más cercanos y, **después**, en Python, se descartan los que no son `g4`. Los cinco más cercanos eran de `g1`. El fragmento correcto de `g4` era el octavo en la lista global.

1. ¿Qué devuelve ese procedimiento?
2. ¿Cómo tiene que pedirse la consulta para que no ocurra?
3. Relaciónalo con una de las preguntas de ejemplo del proyecto, que mezcla horas de un módulo y acceso con grado medio.

## 9. Escala del IES

Estimas 1.500 fragmentos de dimensión 1024.

1. Argumenta si hace falta un índice aproximado para cumplir una latencia de búsqueda de décimas de segundo.
2. Aun así, ¿qué parámetro mirarías si el top 5 de ChromaDB no coincide con un barrido exacto escrito en Python?
3. ¿Qué no tocarías todavía?

## 10. Cambio de modelo en la fase local

En la fase final del proyecto, Titan puede sustituirse por un modelo ejecutado en el servidor del centro.

1. ¿Se pueden dejar los vectores antiguos y solo cambiar la consulta?
2. ¿Qué se conserva de cada registro para no depender de Titan en esa reconstrucción?
3. ¿Qué medida hay que repetir antes de dar por válida la sustitución?
