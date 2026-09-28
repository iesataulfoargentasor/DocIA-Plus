# Soluciones de los ejercicios

Para corregir en el aula después de que el grupo haya intentado los ejercicios. No forma parte de la lectura previa del alumnado.

## 1. Dos búsquedas

1. La cadena de la pregunta no aparece en el documento. Comparten la idea de matrícula, no los tokens. Un índice literal no tiene por qué devolverlo, salvo un sinónimo configurado a mano.
2. Tiene que ser el mismo modelo, la misma dimensión y la misma normalización. Si no, la distancia no significa parecido.
3. Cualquier identificador exacto: un código de módulo, un CVE, el nombre propio de un documento. Por ejemplo, localizar la cadena `CVE-2026-4540`.

## 2. Coseno a mano

Normas:

- `||a|| = raíz(4) = 2`
- `||b|| = raíz(2) ≈ 1,414`
- `||c|| = 3`

Cosenos con `a`:

- `a · b = 2`. Coseno = `2 / (2 * raíz(2)) = 1 / raíz(2) ≈ 0,707`
- `a · c = 0`. Coseno = 0

Orden: `b`, luego `c`.

El producto escalar de `a` con `b` vale 2 y el coseno vale unos 0,707 porque `a` y `b` no tienen norma 1. El producto escalar crece con la longitud. Por eso Titan se usa normalizado y no se compara un producto escalar de vectores sin normalizar como si fuera el coseno.

## 3. Vectores ya normalizados

1. `||q|| = raíz(0,36 + 0,64) = raíz(1) = 1`.
2. `q · d1 = 0,36 + 0,64 = 1`. `q · d2 = 0,48 + 0,48 = 0,96`. Como están normalizados, esos productos son los cosenos.
3. Primero `d1`, que es el mismo vector. En ChromaDB 1.1.0 con espacio coseno, la distancia es `1 - coseno`, así que `d1` sale a 0 y `d2` a 0,04. `laboratorio/02_chromadb_coleccion.py` lo imprime con otros vectores (un coseno de unos 0,998 sale a distancia de unos 0,002). Si una versión futura de la librería cambiara esa convención, manda la salida de ese script, no esta solución.

## 4. Una colección que no se puede mezclar

1. Los vectores no tienen la misma dimensión y, además, las 256 dimensiones de Titan son una compresión entrenada, no un prefijo de las 1024. No viven en el mismo espacio.
2. Crear una colección nueva, reenviar **todos** los fragmentos al modelo pidiendo 256, y repetir las pruebas de recall. No se convierten los vectores ya guardados.
3. Las coordenadas no son features sueltas que se puedan amputar. El modelo, cuando se le pide 256, construye otra representación. Cortar a mano deja un vector que ningún entrenamiento ha definido.

## 5. Estructura de un registro

1. `plan-igualdad-2026_002`
2. `categoria=g3`, `doc_id=plan-igualdad-2026`, `titulo=Plan de igualdad`, `fuente=plan-igualdad-2026.pdf`, `curso=2026-2027`, `seccion=Medidas`, `chunk=2`, más `hash` del texto e `indexado` con la fecha de la carga. `pagina` si la extracción la conoce.
3. Por ejemplo, el nombre del alumno que hizo la prueba y el texto de la pregunta usada para depurar. La colección no es un registro de consultas. Tampoco el vector duplicado dentro de los metadatos.

## 6. Actualizar sin dejar huérfanos

1. `_000` no se envía a Titan: el hash coincide. No hace falta `upsert` salvo que se quiera refrescar la fecha de indexación; el vector puede quedarse.
2. `_001` se vuelve a embeber y se hace `upsert` con el mismo identificador.
3. Se borran `_002` y `_003`, que ya no existen en la fragmentación nueva.

Si se omite el borrado, el calendario viejo sigue siendo recuperable.

## 7. Recall@5

1. Aciertos en el top 5: cinco de ocho. Recall@5 = 5/8 = 0,625, es decir, 62,5 %.
2. No. El proyecto pide más del 80 % con 3 a 5 fragmentos.
3. Con k = 10 la pregunta 4 sumaría y el recall sería 6/8 = 75 %, y seguiría por debajo del 80 %. Aunque superara el 80 %, no valdría: el indicador del proyecto está escrito para k entre 3 y 5. Subir k a escondidas mejora la cifra y empeora lo que ve el usuario, que recibe más ruido.

## 8. El filtro que llega tarde

1. Devuelve una lista vacía. Los cinco candidatos eran de programaciones y se descartan todos. El fragmento de oferta educativa ni siquiera se llegó a pedir.
2. El `where` de `categoria = g4` va dentro de la consulta a ChromaDB, y k = 5 significa cinco resultados que ya cumplen el filtro.
3. La pregunta de ejemplo del proyecto junta horas de un módulo y condiciones de acceso. Puede necesitar fragmentos de más de una categoría. En ese caso el filtro no se fija a una sola categoría: se consulta la colección completa, o se hacen dos consultas acotadas y se unen. Forzar `g4` perdería una programación que sí dice las horas, y forzar `g1` perdería el acceso. El filtro es una decisión de la pregunta, no un valor fijo del sistema.

## 9. Escala del IES

1. No hace falta para la latencia. 1.500 × 1024 operaciones son del orden de un millón y medio de multiplicaciones, milisegundos en el servidor previsto. El presupuesto de 3 segundos de la API lo consume la redacción, no el k-NN exacto.
2. `hnsw:search_ef`, subiéndolo hasta que el top 5 coincida con el barrido exacto.
3. No se cambia el modelo, ni el corte de los documentos, ni el espacio de la colección, mientras no se haya demostrado que el índice devuelve los mismos vecinos que el barrido.

## 10. Cambio de modelo en la fase local

1. No. Los vectores antiguos están en el espacio de Titan. El modelo local produce otro espacio, a menudo otra dimensión. Mezclarlos da un ranking sin significado.
2. El texto del fragmento y los metadatos. Con eso se puede volver a llamar al modelo nuevo. Los vectores se tiran.
3. El recall@5 sobre el mismo conjunto de preguntas. Si baja, la sustitución no está validada, aunque el servidor local ya responda.
