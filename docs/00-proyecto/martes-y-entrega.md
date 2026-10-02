# Los martes de BDA y SBD

Trabajamos en bloques de **3 horas de BDA y 2 horas de SBD**. SBD prepara documentos y metadatos; BDA genera vectores, mantiene la colección y mide el proceso. PIA lidera la API, la generación de respuestas y la aplicación web.

La **Formación en Empresa comienza el 20 de mayo de 2027**. La entrega del trabajo de aula se cierra el **martes 18 de mayo**. Las tareas de junio corresponden al equipo coordinador y no dependen de la asistencia del alumnado al centro.

## Primeros martes

Fechas propuestas, sujetas a los ajustes del calendario del centro. El itinerario conceptual de siete sesiones de la unidad es una referencia de contenidos, no siete bloques de cinco horas adicionales.

| Martes | BDA — 3 h | SBD — 2 h | Evidencia |
| --- | --- | --- | --- |
| 6 octubre | Flujo de recuperación y cuaderno Ver el vector | Categorías y elección de fuentes reales | Cinco documentos piloto identificados |
| 13 octubre | Qdrant: colección, carga y consulta guiada | Texto, metadatos y procedencia | Explicar un resultado y su fuente |
| 20 octubre | Paráfrasis, coseno, top-k y filtros | Esquema común y vigencia documental | Comparar búsqueda libre y filtrada |
| 27 octubre | Reto de recursos y defensa breve | Revisar calidad y adaptar el esquema | Cuaderno razonado y registro documental |
| 10 noviembre | Trasladar el mismo catálogo a ChromaDB | Validar IDs, tipos y referencias | Comparación con modelo y vectores fijos |
| 17 noviembre | Ingesta de fragmentos y lectura por ID | Extraer PDF, DOCX y HTML; detectar ruido | Un documento real procesado por grupo |
| 24 noviembre | Comprobar contrato común y demostrar el piloto | Cerrar inventario de al menos 80 documentos | Evidencias para H1 |

Materiales: [De Qdrant a ChromaDB](../01-bases-vectoriales/qdrant-a-chromadb.md). Si BDA se imparte primero, utiliza el lote que SBD validó el martes anterior; SBD prepara después la siguiente entrega. Al principio se trabaja con datos proporcionados por el profesor.

## Entregas del proyecto

| Fecha de referencia | Trabajo de BDA | Trabajo de SBD | Hito del proyecto |
| --- | --- | --- | --- |
| Diciembre | Pipeline local reproducible; actualización sin duplicados ni huérfanos | Fragmentación y conjunto de preguntas | Piloto previo a la nube |
| Enero | Titan y ChromaDB como servicio, con PIA; registro de ejecución | Corpus preparado y validado antes del 31 de enero | H2 y revisión H3 |
| Febrero | Indexación de las cinco categorías y evaluación | Cobertura, fuentes y corrección de errores documentales | H4, coordinado con PIA |
| Marzo | Recuperación común y dashboard con PIA | Revisión de citas, vigencia y lagunas | H5 |
| 20 abril | Validación técnica con PIA y Digiytal | Validación de fuentes y cobertura | H6; fecha de visita por coordinar |
| 27 abril | Corregir incidencias y probar mantenimiento desde el panel | Sustituir y retirar documentos | Versión final de aula |
| 11 mayo | Copia, restauración y reconstrucción probadas | Auditar corpus y cerrar manual documental | Entrega reproducible |
| 18 mayo | Demostración y defensa individual del pipeline y métricas | Defensa de extracción, fragmentación y calidad | Cierre antes de Formación en Empresa |
| Junio | Coordinación técnica: migración local y documentación | Coordinación: validación y transferencia del corpus | H7 y H8; sin exigir asistencia del alumnado |

La comparación con un modelo local es una ampliación si el servidor está disponible antes de mayo. No desplaza las pruebas de restauración ni el cierre de las evidencias individuales. La Formación en Empresa tendrá su propio plan y seguimiento.

## Qué se entrega y cómo se evalúa

Cada grupo entrega inventario, fragmentos citables, esquema común, proceso de ingesta y actualización, evaluación reproducible y manual de mantenimiento. Cada alumno explica una decisión y demuestra una operación. SBD evalúa la preparación y calidad de los datos; BDA, su procesamiento, mantenimiento y presentación de resultados, mediante los instrumentos de las programaciones.

La dedicación de los martes no equivale al peso en la calificación. El proyecto debe distinguir ambas magnitudes y ajustar su previsión horaria al calendario real.

## Acuerdos que debe cerrar el equipo

- **80 documentos y 400 documentos:** el Word contiene ambos objetivos. Contar por separado originales y fragmentos; trocear 80 archivos no crea 400 documentos originales. El alcance definitivo de H4 debe aclararse con coordinación.
- **Cinco grupos:** comparten formato de entrada, metadatos y contrato de consulta. Cada grupo valida su categoría antes de integrarla; no se crean cinco interfaces incompatibles.
- **Calidad:** medir recuperación y respuesta generada por separado. El tema 9 define acierto, precisión, exhaustividad y errores de rechazo.
- **Uso del servicio:** acordar métricas agregadas que permitan mejorar el corpus sin guardar preguntas personales. Un top de temas no requiere publicar consultas literales.
