# 10. ChromaDB en DocIA+

ChromaDB es la base vectorial elegida en el proyecto. Esta página junta las decisiones ya tomadas con lo que el laboratorio demuestra en local. No abre todavía la cuenta de AWS.

## Decisiones ya tomadas

| Decisión | Valor de partida | Dónde se justifica |
| --- | --- | --- |
| Producto | ChromaDB, en la misma máquina que la API | Tema 5. El proyecto descarta un buscador gestionado de coste fijo |
| Modelo de embeddings, fase cloud | Amazon Titan Embeddings v2, 1024 dimensiones, normalizado | Tema 2 |
| Espacio de la colección | Coseno | Tema 3 |
| Unidad de indexación | Fragmento con texto citable, no el PDF | Tema 7 |
| Colección integrada | Una, con `categoria` filtrable | Tema 6 |
| Escritura | `upsert` por identificador estable, más borrado de huérfanos | Tema 8 |
| Qué no se guarda | Preguntas de usuarios y datos personales | Tema 5, y el diseño de privacidad del proyecto |
| Copias | Instantánea periódica del directorio de la base, fuera de la máquina | Tema 8 |

Estas decisiones se pueden revisar con una medida del tema 9 en la mano. No se revisan por preferencia de herramienta a mitad de la indexación: cambiar el espacio o el modelo implica construir otra colección.

## Qué hay que tener en la cabeza el día que se despliegue

![La web habla con la API. La API consulta ChromaDB y Titan. La colección no se publica en internet.](../assets/esquemas/10-arquitectura.svg)

En el proyecto, ChromaDB y FastAPI comparten una instancia pequeña (dos vCPU y 4 GB de RAM). Para el volumen del IES sobra, siempre que no se convierta la máquina en el sitio donde también se entrenan modelos. El índice HNSW de unos miles de vectores de 1024 floats ocupa decenas de megabytes, no gigabytes.

La base escucha en la red privada de esa máquina. No se publica ChromaDB a internet para que el widget de la web le consulte directo. Quien consulta es la API, que aplica autenticación en las operaciones de escritura. La lectura que hace el chatbot pasa por la API. Abrir el puerto de ChromaDB al público dejaría la colección de documentos internos al alcance de cualquiera, con o sin embeddings de por medio.

Los originales y las copias de la base van a un almacén de objetos distinto. Si la instancia se rehace, se restaura la copia o se reindexa desde los originales. Las dos vías tienen que estar probadas antes de dar el hito por cumplido.

## Dos laboratorios, en este orden

La sesión 1 ya ha usado un modelo de verdad (`all-MiniLM-L6-v2`, 384 números) y ChromaDB en Colab, con frases de ejercicio y los códigos `g1` a `g5`. La distancia de aquel primer cuaderno es una resta de listas. La de ChromaDB, en espacio coseno, es 1 menos el coseno. No se comparan.

Después de esa sesión, el laboratorio local separa otras dos cosas, sin descargar un modelo y con vectores escritos a mano:

1. **Geometría**, en Python puro: producto escalar, norma y coseno, y un ranking de cuatro textos del estilo de los documentos del centro.
2. **ChromaDB local**: crear la colección en espacio coseno, hacer `upsert`, consultar con filtro `g4`, borrar un huérfano y comprobar que dos vectores iguales dan distancia 0.

Instrucciones y qué observar: [laboratorio/README.md](https://github.com/iesataulfoargentasor/DocIA-Plus/blob/main/laboratorio/README.md).

Cuando el script local sale bien, el grupo ha visto las operaciones de la base sin el ruido de la nube. El paso siguiente, ya fuera de esta unidad, es sustituir el vector escrito a mano por la salida real de Titan y el texto de ejercicio por un documento de una de las cinco categorías. El esquema de metadatos y las operaciones no cambian.

## Qué viene inmediatamente después

El trabajo de implementación, cuando se cierre esta unidad, sigue este orden:

1. Cerrar en el aula el esquema de metadatos del tema 6, con los cinco grupos delante.
2. Elegir un documento real corto de cada categoría y escribir a mano cinco preguntas cuya respuesta esté en ese documento.
3. Implementar el ciclo del tema 7 para esos cinco documentos, todavía en local, con el modelo de embeddings que esté disponible en ese momento.
4. Calcular el recall@5 del tema 9 sobre esas preguntas.
5. Solo con esa medida, decidir si el corte y los metadatos aguantan el salto a la colección compartida.

Hasta no tener el punto 4, no compensa discutir la instancia, el dominio ni el chatbot.
