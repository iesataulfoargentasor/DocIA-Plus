# 9. Calidad, fallos y qué mediremos

El proyecto pide una precisión de recuperación superior al 80 % en pruebas controladas, devolviendo de 3 a 5 fragmentos. Esta página convierte esa frase en una medida que se puede calcular, y en una lista de fallos que mueven esa medida sin que «el modelo se haya vuelto tonto».

## Dos precisiones que no se mezclan

| Medida | Pregunta que contesta | Quién la mira |
| --- | --- | --- |
| Recuperación | ¿El fragmento que contiene la respuesta está entre los k devueltos? | SBD y BDA, sobre la base vectorial |
| Respuesta redactada | ¿El texto final es fiel a esos fragmentos y cita la fuente? | PIA, sobre el sistema completo |

Se puede recuperar bien y redactar mal, y al revés es raro: si el fragmento correcto no está, el redactor cita otra cosa o inventa. **Esta unidad solo mide recuperación.**

## El conjunto de pruebas

Hace falta una lista escrita antes de tocar parámetros. Cada fila la elabora quien conoce el documento, no el propio buscador.

| Campo | Ejemplo |
| --- | --- |
| Pregunta, con palabras distintas a las del documento | ¿Puedo acceder con un grado medio de informática? |
| `doc_id` que debe aparecer | `oferta-iabd-2026` |
| Fragmento o sección que debe aparecer | Acceso |
| Categoría | `g4` |

Veinte preguntas, cuatro por categoría, ya permiten discutir. Ochenta, cuando el corpus esté cerrado, dan una cifra presentable. Menos de diez no distinguen un sistema bueno de una casualidad.

Una pregunta solo entra en el conjunto si la respuesta **está** en el corpus. «¿Hay beca de transporte este año?» no sirve como prueba de recuperación si ningún documento lo dice: el resultado correcto es no recuperar nada suficientemente cercano, y eso se anota como caso negativo, aparte.

## Recall@k de recuperación

Para cada pregunta, se mira si el `doc_id` esperado está entre los k identificadores devueltos.

```text
recall@k = preguntas en las que el doc_id esperado aparece en el top k
           / preguntas del conjunto
```

![En el ejemplo del ejercicio, cinco de ocho preguntas aciertan en el top 5: un 62,5 %, por debajo del 80 % que pide el proyecto.](../assets/esquemas/09-recall.svg)

Con k = 5, el objetivo del proyecto se lee así: en más del 80 % de las preguntas controladas, el documento correcto está entre los cinco primeros fragmentos.

Es un recall sobre documentos, no sobre el índice HNSW. Si se quiere afinar, se exige también la sección. Al empezar, el `doc_id` basta para no bloquear la medida en discusiones de paginación.

k se reporta siempre junto a la cifra. Un 80 % con k = 20 no es el objetivo. El objetivo habla de 3 a 5.

## El umbral

Además del top-k se observa la distancia del primer resultado. En las preguntas negativas —las que no tienen documento— esa distancia debe quedar peor que en las positivas. El hueco entre los dos grupos es el sitio donde se coloca el umbral. Si los dos grupos se solapan, el problema no es el umbral: es el fragmentado, la limpieza o el modelo.

El número del umbral se anota en la documentación del pipeline cuando exista la colección real. No se inventa en esta unidad, porque depende de cómo ChromaDB exprese la distancia coseno en la versión que fijemos.

## Fallos típicos

Cada fallo tiene un síntoma en la medida y un sitio donde se corrige.

| Síntoma | Causa frecuente | Dónde se corrige |
| --- | --- | --- |
| El top-5 son pies de página, índices o portadas | Se ha embebido el ruido del PDF | Limpieza, SBD |
| Sale un párrafo de otro año | No hay filtro de `curso`, o conviven vigencias | Metadatos y borrado de la vigencia vieja |
| La cita es el documento correcto pero el párrafo no responde | Fragmento demasiado largo, mezcla de apartados | Corte, SBD |
| Tres resultados son el mismo párrafo | Solape alto y no se agrupa por `doc_id` al presentar | Fragmentación y presentación |
| Ayer funcionaba y hoy las distancias son absurdas | Se ha consultado con otro modelo, otra dimensión u otra normalización | Pipeline de BDA; hay que reindexar |
| Un documento corregido sigue citando el texto viejo | No se borraron los fragmentos huérfanos | Procedimiento de actualización |
| El índice HNSW no devuelve lo que devuelve un barrido en Python | `search_ef` corto | Parámetro del índice, no el texto |
| Dos grupos no se integran | Metadatos distintos para la misma idea | Esquema único del tema 6 |

Ninguno de estos fallos se arregla «pidiendo el vector otra vez» sin cambiar el texto o la configuración. El modelo es determinista a efectos prácticos: el mismo texto, el mismo modelo y las mismas opciones producen el mismo vector.

## Qué se enseña con un fallo

Cuando la medida baje, el orden de revisión es fijo:

1. El texto guardado en el registro, con un `get` por `doc_id`. ¿Es texto citable o basura de extracción?
2. Los metadatos. ¿Categoría, curso y hash son los esperados?
3. La llamada de embeddings. ¿Mismo modelo, misma dimensión, norma cercana a 1?
4. La consulta. ¿El `where` y k son los de la prueba?
5. Solo entonces, el índice aproximado, comparándolo con un barrido exacto.

Ese orden evita pasar una tarde cambiando parámetros de HNSW cuando el PDF se leyó al revés.
