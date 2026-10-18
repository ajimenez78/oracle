# Review IA del repo ajimenez78/oracle

Fecha: 15/10/2026
Alcance: ingesta y vectorización de notas, sistema RAG y decisiones de IA de la spec.
Base: `legacy/vectorize.py`, `legacy/run_chat.py` y `specs/SPEC.md` (branch `develop`). El PoC se ha movido a `legacy/`, pero sigue siendo lo único que corre y la referencia de calidad del proyecto, así que lo trato como código vivo. No he revisado la parte de infra/CI ni el frontend; me centro en la parte de IA.

## Contexto

En el repo conviven dos cosas: un PoC que funciona (Gradio + Chroma + LangChain, indexa 4 páginas raíz de Notion y responde preguntas sobre ellas) y una spec v0.4 que propone reescribirlo como microservicios serverless en AWS (S3 Vectors, EventBridge + SQS, DynamoDB, frontend React).

Lo primero que llama la atención es que la spec audita al propio PoC: sección 10.2 con 12 findings, requisitos con IDs estables y aceptación explícita, y el PoC se conserva como baseline que el sistema nuevo tiene que igualar o superar (sección 13). Esto último es la forma correcta de migrar un RAG y no siempre se hace.

Voy por partes: primero lo que está bien, luego los defectos del PoC ordenados por lo que afecta a la calidad de las respuestas (no por gravedad técnica), los huecos que le veo a la spec y qué haría yo.

## Lo que está bien

El cliente de Notion está por encima de la media de lo que suelo ver en ingesta: reintentos con backoff exponencial y jitter, `status_forcelist` para 429/5xx, respeto del `Retry-After`, timeouts de conexión y lectura separados. Y los errores no abortan la ejecución: los bloques o páginas que fallan se registran y se reportan al final. Fallo parcial ≠ fallo total, que es como debe ser.

También hay idempotencia parcial en el índice: los ids de chunk son deterministas (`{page_id}-chunk-{i}`), así que re-ejecutar sobre la misma versión de página no duplica contenido.

## Defectos del PoC

1. **Aplanado del árbol de Notion.** Los chunks de todas las páginas hijas se concatenan al texto de la raíz y el metadata lleva título y URL de la raíz. Doble efecto: las citas apuntan a "Projects" en vez de a la nota real (para un oracle con citas esto destruye la confianza del usuario) y la recuperación empeora porque un chunk puede mezclar contenido de dos hijas distintas. Además hace imposible sincronizar por página.

2. **Chunking ciego a los headings.** `RecursiveCharacterTextSplitter` sobre texto plano, cuando `extract_text_from_block` ya emite `#`, `##`, `###`. Los chunks atraviesan secciones y temas distintos. Es el problema de retrieval más frecuente y el más barato de arreglar.

3. **Re-indexación completa y basura acumulada.** Se re-embedea todo en cada ejecución (coste y tiempo innecesarios) y los chunks de páginas borradas o reducidas nunca se quitan de Chroma. En notas personales, donde lo archivado convive con lo actual, el contenido obsoleto acaba compitiendo en el top-k.

4. **Sin umbral de similitud.** `as_retriever(k=10)` devuelve siempre 10 chunks pasen lo que pasen. Un oracle que no puede decir "no he encontrado nada relevante en tus notas" está abocado a alucinar con seguridad. Para mí es el requisito número 1 de un asistente personal.

5. **Generación mal afinada para RAG.** `temperature=0.7` en Q&A grounded introduce variación y riesgo de invención; para respuestas basadas en contexto lo dejaría en 0.2 o menos. Y `ConversationalRetrievalChain` va camino de deprecación, con memoria en proceso y una reescritura de preguntas opaca. La spec ya decide eliminarla (ADR-0007): de acuerdo.

6. **Embeddings por defecto de la librería.** `OpenAIEmbeddings()` sin fijar modelo ni dimensiones. Un cambio de default en una actualización mezclaría vectores de modelos distintos en la misma colección. Es de los fallos que solo detectas cuando ya has corrompido el índice; la spec lo cubre (FR-13, FR-36).

7. **Metadatos mínimos.** Solo `source`, `title` y `page_id`. Faltan heading path, posición, hash de contenido, fecha de edición y sección raíz. Sin hash no hay indexación incremental; sin sección no puedes filtrar (excluir Archive por defecto, por ejemplo).

## Huecos en la spec

La spec cubre mucho (eventos versionados, idempotencia, DLQs, streaming, citas), pero desde el punto de vista de IA le faltan cuatro cosas que para mí son imprescindibles:

**Búsqueda híbrida.** El hueco más importante. Las notas personales están llenas de nombres propios, siglas, código y términos en español; los embeddings puros fallan sistemáticamente ahí ("API Gateway" no se parece a "APIGW", y el nombre de un proyecto interno no tiene señal semántica). Con pgvector u OpenSearch el híbrido (RRF sobre BM25 + kNN) viene casi de serie; S3 Vectors, el default de la spec, es muy nuevo y su superficie de filtrado es básica. Es mi principal objeción técnica a la elección de vector store: no me preocupa el rendimiento (para el QPS de un usuario sobra), me preocupa que condicione la evolución del retriever. Dejaría la decisión condicionada a que el híbrido sea requisito, o directamente apostaría por pgvector en Aurora Serverless v2.

**Reranking.** Con k=10 y notas que mezclan temas e idiomas, un reranker entre retriever y prompt (Cohere Rerank o un cross-encoder open-source) es hoy la mejora con mejor ratio coste/calidad: retrieve con k=25-50 (barato), rerank a top-5 (caro, pero son pocas queries). Menos contexto irrelevante, menos alucinación, prompts más pequeños. No aparece en ningún FR; lo añadiría en `knowledge` o `chat`.

**Chunking heading-aware como prioridad, no como opción.** FR-10 lo deja "configurable" y mantiene 1000/200 de baseline por comparabilidad. Entiendo el baseline para medir, pero no debería retrasar la mejora: split por secciones de heading y recursive dentro de cada sección, con tamaños en tokens y no en caracteres (`len()` sobre caracteres subestima el consumo real con texto en español).

**Evaluación separada de retriever y generador.** La spec junta "hit-rate@k y groundedness". Yo lo separo: para el retriever, recall@k y MRR sobre un golden set de pregunta → página/chunk esperado (sin esto no puedes decidir entre cambiar embeddings, chunking o añadir reranker, porque siempre mides el sistema completo); para el generador, faithfulness, relevancia y verificación de citas (RAGAS o un harness propio con LLM-as-judge). Y una cosa barata que evita el peor fallo de UX de un sistema con citas: comprobar que los chunk ids que cita el LLM existen de verdad en el contexto entregado, porque inventan citas con frecuencia.

## Arquitectura

De acuerdo con: eventos versionados con `event_id` y `version`; el índice vectorial como almacén derivado reconstruible por replay (la decisión más importante de la spec y está tomada de forma explícita); no reutilizar `ConversationalRetrievalChain` ni memoria en proceso; y el PoC como baseline de evaluación.

Donde tengo dudas:

- **Sobre-ingeniería para un solo usuario.** Tres microservicios, EventBridge, SQS, DLQs, DynamoDB por servicio, contratos OpenAPI y CI por servicio, para lo que en el fondo es: cron sincroniza, chunk + embed, una función responde. La propia spec lo admite (G3). Si el objetivo es aprender, es legítimo; si el objetivo es el producto, yo empezaría con un monolito modular (2-3 Lambdas compartiendo módulo de dominio) y migraría solo si aparece un motivo real de escalado. El roadmap ya contiene el antídoto contra la fragmentación (sección 12); aplicárselo al arranque no es menos válido. La mejor arquitectura de IA es la que llega a producción.
- **Polling cada 10 minutos.** Correcto como v1, pero Notion ya ofrece webhooks (beta) y para frescura del índice me parecen mejores y más baratos. Lo dejaría como OQ.
- **S3 Vectors como default**, por lo del híbrido de arriba.

## Qué haría yo, en orden

1. Páginas hijas como unidades de indexación propias (metadata por página real).
2. Umbral de similitud y respuesta explícita de "no encontrado".
3. Chunking heading-aware, tamaño en tokens.
4. Golden set del retriever (recall@k, MRR) y medir el PoC como baseline.
5. `temperature=0.2`, prompt versionado, chunks con ids citables en el prompt.
6. Borrado real de chunks obsoletos y no re-embeddear lo que no cambió de hash.
7. Reranking.
8. Búsqueda híbrida y decisión de vector store en consecuencia (ADR).
9. Verificación de citas contra el contexto entregado.
10. Fijar modelo y dimensiones de embeddings en config, con detección de mismatch.
11. Historial de conversación truncado por tokens, con resumen de turnos antiguos.

Los puntos 1 a 6 caben dentro del PoC actual, sin esperar a la reescritura. De hecho lo recomiendo: mejoran el producto esta semana y dejan el baseline más exigente para el sistema nuevo.

## Resumen

El PoC es un RAG v1 correcto, con una ingesta mejor de lo habitual y los defectos clásicos de primera iteración, todos documentados por su propia spec; nada bloqueante. La spec es de las mejores que he visto en un proyecto personal; sus huecos son de calidad de retrieval (híbrido, reranking, evaluación separada) y de una elección de vector store que condiciona todo eso. Mi consejo: mejoras rápidas sobre el PoC como camino incremental, y el ADR de híbrido/vector store cuanto antes, porque es la decisión que más ata el diseño de `knowledge`.
