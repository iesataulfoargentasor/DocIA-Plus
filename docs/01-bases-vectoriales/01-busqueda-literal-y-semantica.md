# 1. Búsqueda literal y búsqueda semántica

## El fallo que DocIA+ tiene que evitar

En el proyecto hay una pregunta de ejemplo y un documento que no usa las mismas palabras:

| Lo que escribe la persona | Lo que dice el documento |
| --- | --- |
| ¿cómo me matriculo en el ciclo de IA? | procedimiento de formalización de matrícula |

Un buscador literal acierta si la cadena, o un trozo suficiente de ella, aparece en el texto. Aquí no aparece «cómo me matriculo». Aparece otra formulación del mismo trámite. La persona no encuentra el párrafo, aunque el párrafo responde a su pregunta.

Eso le pasa todos los días a la documentación de un centro: programaciones, instrucciones de la Consejería, planes y la web no comparten un vocabulario único. Familias, alumnado y profesorado preguntan con el suyo.

## Qué sí resuelve la búsqueda literal

Conviene decirlo para no tirar una herramienta útil. La búsqueda por palabras, por expresión regular o por índice invertido (el de SQL `LIKE`, el de Elasticsearch o el de `grep`) es la opción correcta cuando:

- el usuario conoce el identificador: un código de módulo, un número de resolución, un nombre propio de un plan;
- hay que encontrar una cadena exacta, por ejemplo `CVE-2026-4540`;
- el corpus es tan pequeño que una persona puede abrir el fichero.

DocIA+ no sustituye ese caso. Lo que no cubre es la pregunta formulada con otras palabras, que es la mayoría de las preguntas de la comunidad educativa.

## Qué hace la búsqueda semántica

La búsqueda semántica representa el texto como un punto en un espacio numérico. Dos textos quedan cerca si un modelo de lenguaje, entrenado con enormes cantidades de texto, ha aprendido que se usan en contextos parecidos. «Matricularse» y «formalizar la matrícula» caen cerca. «Plan de convivencia» cae en otra zona.

El procedimiento, visto desde fuera, es siempre el mismo:

1. El documento se parte en fragmentos.
2. Un modelo de embeddings convierte cada fragmento en un vector. Eso se hace **una vez** y se guarda.
3. Cuando llega una pregunta, **el mismo modelo** la convierte en un vector.
4. La base de datos devuelve los fragmentos cuyos vectores están más cerca del vector de la pregunta.
5. Esos fragmentos, no el documento entero, son la evidencia que verá el modelo que redacta la respuesta.

Los pasos 2 y 4 son el trabajo de almacenamiento y gestión que vamos a estudiar. El paso 5 ya no es una base de datos: es la generación, y en el proyecto la hace otro componente.

## Por qué no basta una tabla SQL clásica

Una tabla relacional guarda el texto y permite filtrar por columnas: categoría, fecha, nombre de fichero. Eso lo vamos a seguir necesitando, en forma de metadatos. Lo que una tabla clásica no hace es **ordenar por parecido de significado**.

Se podría guardar el vector como una columna de números y, en cada consulta, recorrer todas las filas calculando la similitud. Con el tamaño inicial de DocIA+ eso incluso funciona, y lo cuantificaremos en el tema 4. Sigue siendo una búsqueda vectorial: solo que el índice es un barrido completo. Una base de datos vectorial es el sistema que trata ese barrido, o un índice aproximado equivalente, como operación de primera clase, junto con el texto y los metadatos del fragmento.

## Lo que la semántica no garantiza

Cercanía no es verdad. El vector de un fragmento desactualizado puede ser el más parecido a la pregunta y estar mal. El vector de un índice o de una portada puede parecerse a muchas preguntas porque contiene palabras de todos los temas. Por eso el proyecto exige **cita de la fuente** y una precisión medida en pruebas controladas, no la confianza de que «la IA ya lo encontrará».

La base vectorial devuelve candidatos ordenados. Decidir si bastan para responder, y redactar sin inventar lo que no está en ellos, es una capa distinta. Si esta capa de candidatos falla, la capa de redacción no tiene de dónde citar.

## Consecuencia para DocIA+

El indicador del proyecto no es «el chatbot contesta bonito». Es: ante una pregunta de prueba cuya respuesta sabemos en qué documento está, los 3 a 5 fragmentos recuperados incluyen ese documento. Esa medida se define en el tema 9. Todo lo que hay en medio —modelo, distancia, fragmentación, metadatos— existe para que esa medida salga bien.
