# 3. Geometría y similitud

Este tema es el que hay que saber calcular a mano con vectores pequeños. En DocIA+ los vectores tendrán 1024 componentes, pero las cuentas son las mismas que con 3.

El laboratorio [`01_geometria_similitud.py`](https://github.com/iesataulfoargentasor/DocIA-Plus/blob/main/laboratorio/01_geometria_similitud.py) reproduce los ejemplos.

## Vector, longitud y producto escalar

Un vector es una lista ordenada de números. Para dos vectores de la misma dimensión:

```text
a = (a1, a2, a3)
b = (b1, b2, b3)

producto escalar  a · b = a1*b1 + a2*b2 + a3*b3

longitud o norma  ||a|| = raíz cuadrada de (a · a)
```

La norma mide lo largo que es el vector, no lo cerca que está de otro.

## Tres maneras de decir «cerca»

| Medida | Idea | Cuándo encaja |
| --- | --- | --- |
| Distancia euclídea | Longitud de la recta que une los dos puntos | Vectores cuya magnitud importa |
| Producto escalar | Crece si apuntan al mismo sitio y si son largos | Vectores ya normalizados, o modelos que piden producto interno |
| Similitud del coseno | Coseno del ángulo entre ellos. No mira la longitud, solo la dirección | Texto, casi siempre |

La similitud del coseno:

```text
cos(a, b) = (a · b) / (||a|| * ||b||)
```

Vale 1 si apuntan al mismo sitio, 0 si son perpendiculares, y valores negativos si apuntan a sitios opuestos. En embeddings de texto normalizados, los valores útiles suelen estar entre 0 y 1: dos fragmentos de documentación rara vez son «opuestos» en el sentido geométrico; simplemente hablan de otra cosa y el coseno baja.

## Por qué Titan simplifica la cuenta

Si el modelo devuelve vectores de longitud 1, el denominador vale 1 y:

```text
cos(a, b) = a · b
```

Por eso el pipeline no debe mezclar vectores normalizados con vectores sin normalizar. Un vector el doble de largo tendría el doble de producto escalar sin parecerse más. La normalización quita ese efecto. Titan Embeddings v2 puede hacerlo en la propia llamada. El pipeline de BDA la dejará activada y no volverá a tocar la norma después, salvo una comprobación: la norma de un vector recién generado tiene que salir muy cerca de 1. Si no sale, la llamada está mal configurada.

## Un ejemplo con tres dimensiones inventadas

Para ver la geometría sin un modelo, asignamos a mano tres ejes que **sí** significan algo. Esto es didáctico. En un embedding real los ejes no se etiquetan.

Ejes: `(trámites de matrícula, horas y módulos, convivencia)`.

| Texto | Vector |
| --- | --- |
| Procedimiento de formalización de matrícula | (0,90, 0,10, 0,00) |
| Cómo me matriculo en el ciclo | (0,85, 0,20, 0,05) |
| El módulo tiene 190 horas | (0,05, 0,95, 0,00) |
| Plan de convivencia del centro | (0,00, 0,05, 0,90) |

La pregunta «¿cómo me matriculo?» la colocamos en `(0,88, 0,15, 0,02)`.

El coseno con el procedimiento de matrícula sale alto. El coseno con el plan de convivencia sale bajo. El orden de los cuatro textos es el ranking que devolvería una base vectorial. No ha hecho falta que la pregunta contenga la palabra «formalización».

Haz la cuenta en el laboratorio, no solo de lectura: cambia una coordenada y mira cómo se mueve el ranking. Esa sensibilidad es la misma que tendrá un mal fragmento en 1024 dimensiones, solo que allí no veremos el eje culpable.

## De la similitud al ranking

La base no responde «sí o no». Devuelve una lista ordenada. Hay dos políticas:

- **Top-k.** Pedir los k más cercanos. DocIA+ pide k entre 3 y 5 en el objetivo de búsqueda. k más alto recupera más contexto y también más ruido.
- **Umbral.** Quedarse solo con los que superan una similitud mínima. Protege contra contestar cuando no hay ningún fragmento decente. Un umbral mal calibrado deja la pregunta sin evidencia, que es mejor que citar un fragmento irrelevante, siempre que la interfaz diga «no hay documentación suficiente» en lugar de inventar.

En la práctica se combinan: top-k, y si el mejor no llega al umbral, no se redacta una respuesta factual. El umbral numérico **no se copia de otro proyecto**. Depende del modelo, de la normalización y de cómo ChromaDB exprese la distancia. Se fija con las preguntas de prueba del tema 9.

## Distancia no es similitud

ChromaDB ordena por **distancia**: un número donde **menor es más cerca**. La similitud del coseno va al revés: mayor es más cerca.

Según el espacio configurado en la colección, la distancia que verás en el resultado puede ser euclídea, producto interno o una distancia derivada del coseno. Hay que leerla con el espacio que se configuró al **crear** la colección. Ese espacio no se cambia después sin recrear el índice.

En el laboratorio de ChromaDB la colección usa espacio coseno. Con ChromaDB 1.1.0, que es la versión fijada en este repositorio, la distancia que devuelve `query` es **1 menos la similitud del coseno**: dos vectores idénticos salen a distancia 0, y un coseno de 0,998 sale a distancia de unos 0,002. Si en una prueba los números no cuadran con esa cuenta, lo primero que se comprueba es el espacio de la colección y la versión de la librería, no el texto.

## La dimensión alta, sin mito

Se dice a veces que en dimensión alta «todos los puntos quedan igual de lejos». Eso describe nubes de puntos aleatorios. Los embeddings de un modelo entrenado no son aleatorios: el modelo aprieta los textos parecidos y separa los que no lo son. La geometría es usable. Lo que sí ocurre es que no podemos dibujar 1024 ejes ni fiarnos de una impresión visual. Nos fiamos de la métrica y de un conjunto de preguntas con respuesta conocida.

Otra consecuencia práctica: no se recortan componentes a mano «para ahorrar» después de haber generado el vector de 1024. Si se quiere una dimensión menor, se pide en la llamada a Titan (256 o 512), que está entrenado para esa reducción, y se reindexa todo con esa opción. Amputar coordenadas por tu cuenta rompe el espacio.
