# 2. Embeddings

Un **embedding** de texto es una lista de números reales que un modelo produce a partir de un texto. Esa lista es el vector. En DocIA+ habrá dos usos del mismo modelo:

- **embedding de documento**, calculado al indexar y guardado en la base;
- **embedding de consulta**, calculado al llegar la pregunta y usado solo para buscar. El proyecto no guarda la pregunta ni datos de quien la hace.

## Qué entra y qué sale

Entra una cadena ya limpia: un fragmento, no un PDF binario. Sale un vector de longitud fija. La longitud se llama **dimensión**.

Si el modelo devuelve dimensión 1024, todos los vectores de esa colección tienen 1024 componentes. No se puede insertar uno de 768 al lado de uno de 1024. La base lo rechaza o, peor, una implementación descuidada compara magnitudes que no viven en el mismo espacio.

Cada componente, por separado, no significa «horas» ni «matrícula». El significado está en la **posición conjunta** del punto. No se interpreta la coordenada 37. Se interpreta a qué otros puntos se parece.

## No es un resumen, ni un cifrado, ni un hash

| Técnica | ¿Sirve para buscar por significado? | Qué conserva |
| --- | --- | --- |
| Hash criptográfico | No. Un carácter distinto cambia el resultado por completo | Identidad exacta del fichero |
| TF-IDF o bolsa de palabras | Solo coincidencia de términos, con pesos | Qué palabras aparecen |
| Embedding denso | Sí, dentro de lo que el modelo haya aprendido | Parecido de uso en el lenguaje |

TF-IDF sigue siendo una buena herramienta de SBD para explorar un corpus: ver términos dominantes, duplicados burdos, documentos que son casi la misma bolsa de palabras. No resuelve «matrícula» frente a «formalización de matrícula» si esas cadenas no comparten tokens suficientes. El embedding denso sí puede resolverlo, porque el modelo ha visto esas formulaciones en contextos similares durante el entrenamiento.

Un hash del texto sí lo usaremos, pero como **metadato de control**: para saber si el fragmento ha cambiado y hay que recalcular el vector. El hash no se consulta por similitud.

## El modelo elegido en el proyecto

En la fase cloud, DocIA+ usa **Amazon Titan Text Embeddings v2**, invocado a través de Bedrock. Las propiedades que condicionan el diseño de la colección, y que hay que volver a leer en la ficha oficial del modelo el día que se abra la cuenta, son estas:

- La dimensión configurable es **256, 512 o 1024**. El valor por defecto del modelo es 1024. Para DocIA+ partiremos de **1024**, que es la representación completa. Bajar a 512 o 256 reduce almacenamiento y puede perder matices; solo se haría midiendo la precisión de recuperación, no por costumbre.
- La entrada máxima está en el orden de **8.192 tokens**. Un token no es una palabra: en español, una palabra larga o con tilde puede partirse en varios. Un fragmento que supere el máximo se trunca o se rechaza, y el vector deja de representar el final del texto. Por eso el fragmentado del tema 7 tiene que quedar holgadamente por debajo.
- Con la normalización activada, cada vector tiene **longitud 1**. Eso simplifica la similitud: el producto escalar coincide con el coseno. Lo veremos en el tema 3. La colección se creará dando por hecho vectores normalizados, y el pipeline no debe renormalizar a medias ni mezclar llamadas con normalización activada y desactivada.
- El modelo cubre varios idiomas, incluido el español de los documentos del centro. Aun así, un texto lleno de códigos, tablas rotas o guiones de un PDF mal extraído produce un vector pobre. La calidad del embedding no compensa una mala extracción: eso es trabajo de SBD antes de llamar al modelo.

El proyecto presupuesto del orden de unos pocos euros al mes para esta partida, con unos cinco millones de tokens en la indexación inicial. La tarifa concreta se confirma en AWS en el momento de implementar. No es el coste dominante del sistema; el coste dominante previsto es la redacción de respuestas, que no forma parte de esta unidad.

## Llamada, en esquema

Cuando BDA escriba el pipeline, cada fragmento se enviará al modelo y la respuesta será el vector que se inserta en ChromaDB. En esquema, sin SDK todavía:

```text
entrada:  texto del fragmento
modelo:   amazon.titan-embed-text-v2:0
opciones: dimensión 1024, normalizar
salida:   lista de 1024 números, longitud del vector ≈ 1
```

La misma llamada, con las mismas opciones, se usará para la pregunta del usuario en el momento de la consulta. Si alguien indexa con dimensión 1024 y consulta con dimensión 512, la búsqueda es inválida.

## El mismo texto, otro modelo, otro espacio

Un embedding no es una propiedad del texto. Es una propiedad del par (texto, modelo, opciones). Dos modelos distintos colocan el mismo párrafo en espacios que **no se pueden comparar**.

Eso ata una decisión de la fase final del proyecto. Cuando los servicios pasen al servidor local del centro y Titan se sustituya por un modelo local, hay que:

1. generar de nuevo el vector de cada fragmento con el modelo nuevo;
2. construir una colección nueva (la dimensión y la geometría pueden cambiar);
3. repetir las pruebas de recuperación antes de dar por buena la sustitución.

No existe una conversión lineal fiable de «vector Titan» a «vector del modelo local» que nos ahorre esa reindexación. El texto sí se conserva: por eso en cada registro guardamos el fragmento original, no solo el vector. El vector se puede tirar y recalcular. El texto, si no está, no.

## Qué no hace el modelo de embeddings

No redacta la respuesta. No cita. No decide si el fragmento es vigente. No aplica el filtro «solo oferta educativa»: eso es un metadato y un `where`, tema 6. Si el grupo espera que el embedding «entienda el organigrama del IES» más allá de lo que dicen los documentos indexados, el sistema va a inventar huecos. Solo puede acercar la pregunta a texto que sí se ha guardado.
