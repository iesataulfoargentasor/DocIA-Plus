# Soluciones de los ejercicios

Para corregir en el aula después de que el grupo haya intentado los ejercicios. No forma parte de la lectura previa del alumnado.

## 1. Dos búsquedas

1. Pregunta: cómo, me, matriculo, en, el, ciclo, de, IA. Fragmento: procedimiento, de, formalización, matrícula, del, curso, especialización. Solo coincide «de», que aparece en casi cualquier texto y no ayuda a encontrar nada. «matriculo» y «matrícula» son cadenas distintas.
2. `LIKE '%matriculo%'` busca esa cadena exacta y el fragmento no la contiene. Comparten la idea de matrícula, no las letras.
3. El mismo modelo, la misma dimensión y la misma normalización. Si no, la pregunta y el fragmento no están en el mismo mapa y la distancia no significa parecido.
4. Cualquier cadena que se escribe siempre igual: un código de módulo, un número de resolución, el nombre exacto de un fichero. Por ejemplo, localizar `oferta_iabd_2026.pdf`.

## 2. Coseno a mano

```text
‖a‖ = √(4 + 0) = 2
‖b‖ = √(1 + 1) = 1,414
‖c‖ = √(0 + 9) = 3

a · b = 2 × 1 + 0 × 1 = 2       cos(a, b) = 2 / (2 × 1,414) = 0,707
a · c = 2 × 0 + 0 × 3 = 0       cos(a, c) = 0 / (2 × 3)     = 0
```

3. Primero `b` (0,707) y después `c` (0). Cuadra: `b` habla a medias de matrícula y `c` nada.
4. El producto escalar vale 2 y el coseno 0,707 porque los vectores no miden 1. El producto escalar crece con la longitud; el coseno solo mira la dirección.
5. `a` normalizado es `(1, 0)` y `b` normalizado es `(0,707, 0,707)`. Su producto escalar es 0,707, igual que el coseno. Con longitud 1, producto escalar y coseno coinciden.
6. `b`: 1 − 0,707 = 0,293. `c`: 1 − 0 = 1.

## 3. Vectores ya normalizados

1. `‖q‖ = √(0,36 + 0,64) = √1 = 1`.
2. `q · d1 = 0,36 + 0,64 = 1`. `q · d2 = 0,48 + 0,48 = 0,96`. Los tres miden 1, así que el coseno divide entre `1 × 1` y el producto escalar ya es el coseno.
3. Primero `d1`, que apunta exactamente igual que la pregunta. Distancias: `d1` 1 − 1 = 0; `d2` 1 − 0,96 = 0,04.
4. `q − d2 = (−0,2, 0,2)`. Su longitud es `√(0,04 + 0,04) = √0,08 = 0,283`. Y `√(2 × 0,04) = √0,08 = 0,283`. Coinciden. Son dos escalas distintas del mismo parecido, por eso no se comparan números de una con números de la otra.
5. `q · d4 = 0,6 × 3 + 0,8 × 4 = 5`. Un coseno no pasa de 1, así que 5 no lo es: el producto escalar ha crecido con la longitud de `d4`, que es `√(9 + 16) = 5`. El coseno de verdad es `5 / (1 × 5) = 1`: `d4` apunta igual que `q`, solo es cinco veces más largo. Es el error que evita no mezclar vectores normalizados y sin normalizar.

## 4. Una colección que no se puede mezclar

1. Con 1024: 1.200 × 1024 × 4 bytes = 4.915.200 bytes, unos 5 MB. Con 256: 1.200 × 256 × 4 = 1.228.800 bytes, unos 1,2 MB. Se ahorran menos de 4 MB, que no importan en el servidor previsto.
2. Los vectores tienen distinta dimensión: no se pueden ni comparar. Además, el vector de 256 y el de 1024 son dos respuestas distintas del modelo, no dos trozos del mismo mapa.
3. Crear una colección nueva, volver a pedir a Titan **todos** los fragmentos con 256 dimensiones y repetir el acierto@5. Solo compensa si la calidad no baja.
4. Los números de un embedding no son características sueltas que se puedan recortar. Titan no documenta que su vector de 256 sea el principio del de 1024. Recortar a mano da un vector que el modelo nunca ha producido, que además ya no mide 1.

## 5. Estructura de un registro

1. `plan-igualdad-2026_002`.
2. Registro:

    ```python
    {
        "categoria": "g3",
        "doc_id":    "plan-igualdad-2026",
        "titulo":    "Plan de igualdad",
        "fuente":    "plan-igualdad-2026.pdf",
        "curso":     "2026-2027",
        "pagina":    4,
        "seccion":   "Medidas",
        "chunk":     2,
        "hash":      "…",
        "indexado":  20261115,
    }
    ```

    `pagina`, `chunk` e `indexado` son números. El resto, texto.

3. No se pone el campo. ChromaDB no admite `None` como valor.
4. Por ejemplo, el texto de la pregunta con la que se depuró, el nombre de quien la hizo o el vector repetido dentro de los metadatos. La colección no es un registro de consultas.

## 6. Actualizar sin dejar huérfanos

1. `_000`: el hash coincide, no se envía a Titan y el registro se deja como está. `_001`: ha cambiado, se pide su vector nuevo y se hace `upsert` con el mismo identificador. `_002` y `_003`: estaban antes y ya no se generan, se borran.
2. Una llamada a Titan (`_001`). Se ahorra una (`_000`).
3. Dos: `calendario-2026_000` y `calendario-2026_001`, este con el texto nuevo.
4. `_003` sigue en la colección con información antigua y se puede recuperar. DocIA+ respondería con una fecha que ya no vale.

## 7. Acierto@5

1. Cinco de ocho: 5 / 8 = 62,5 %.
2. No. El proyecto pide más del 80 % devolviendo de 3 a 5 fragmentos.
3. 6 / 8 = 75 %, que sigue sin llegar. Y aunque llegara, no valdría: el proyecto devuelve de 3 a 5 fragmentos. Subir k mejora la cifra y empeora lo que ve la persona, que recibe más ruido.
4. Primero la 6 y la 8, donde el documento no aparece. Se hace un `get` por su `doc_id`: ¿está indexado?, ¿el texto guardado se puede leer o es basura de la extracción?, ¿la categoría y el curso son los correctos? La 4 está cerca: suele ser un problema de troceado o de cómo está redactado el fragmento.

## 8. El filtro que llega tarde

1. Una lista vacía. Los cinco pedidos son de `g1` y se tiran todos. `oferta-iabd-2026_002` estaba en la posición 8 y nunca se pidió.
2. Con el filtro dentro:

    ```python
    coleccion.query(
        query_embeddings=[vector_de_la_pregunta],
        n_results=5,
        where={"categoria": "g4"},
    )
    ```

    Ahora son «los 5 más cercanos **de entre los g4**». `oferta-iabd-2026_002` sale el primero.

3. Nada. Está muy lejos, casi «nada que ver». Se aplica el umbral y DocIA+ contesta que no tiene documentación suficiente. La base siempre devuelve algo si hay registros que cumplen el filtro; decidir si sirve es trabajo del umbral.
4. `{"categoria": {"$in": ["g4", "g5"]}}`, o no filtrar por categoría. Forzar solo `g4` perdería el calendario. El filtro depende de la pregunta, no es un valor fijo del sistema.

## 9. Escala del IES

1. 1.200 × 1024 = 1.228.800, unos 1,2 millones de multiplicaciones: milisegundos. No hace falta un índice aproximado. El presupuesto de menos de 3 segundos de la API lo gastará la redacción de la respuesta.
2. 1.000.000 × 1024 = 1.024 millones por pregunta. Con muchas preguntas a la vez, ahí sí hace falta un índice aproximado. DocIA+ está lejos de ese tamaño.
3. `search_ef`, subiéndolo hasta que el top 5 coincida con el recorrido completo.
4. El modelo, el troceado y el espacio de la colección. Primero hay que demostrar que el índice devuelve los mismos vecinos que el recorrido completo.

## 10. Cambio de modelo en la fase local

1. No. Primero, la dimensión es distinta (1024 frente a 384) y no se pueden comparar. Segundo, aunque coincidiera, cada modelo tiene su propio mapa: mezclarlos da un orden sin significado.
2. El texto del fragmento y sus metadatos. Con el texto se pide el vector al modelo nuevo; los metadatos se copian igual. Los vectores de Titan se tiran.
3. El acierto@5, con el mismo conjunto de preguntas de prueba. Si baja, la sustitución no está validada, aunque el servidor ya responda.
4. No. El umbral depende del modelo y de la colección. Se vuelve a fijar con las preguntas negativas, buscando el hueco entre las que tienen respuesta y las que no.
