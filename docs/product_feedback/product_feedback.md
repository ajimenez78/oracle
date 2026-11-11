# Oracle: aprendizajes de la fase de Product Feedback

> **Estado:** borrador. Falta la revisión final de Roberto.

## 1. Resumen ejecutivo

**El problema.** Algunas personas que toman notas de forma sistemática tienen dificultades para organizarlas y encontrarlas después. El caso más claro es el de e3e6, en r/secondbrain: a veces no escribe nada porque no sabe dónde ponerlo, y otras veces no encuentra lo que apuntó.

**Qué hemos aprendido.**

- Empezamos pensando que el gran problema era usar las notas para crear resultados (la etapa *Express*). Las conversaciones señalaron antes un problema de organización y recuperación.
- La simplicidad es clave: quien ya tiene un método que le funciona no quiere otro sistema que mantener.
- El mayor competidor es la propia Notion, seguida de Claude o ChatGPT conectados a Notion. Aun así, hay una combinación de funciones que no vimos documentada en ninguna herramienta revisada.

**Qué vamos a construir.** Un asistente que ordena el Notion que el usuario ya tiene: audita, propone un mapa de organización, pregunta solo por las notas dudosas y aplica los cambios que el usuario aprueba, con opción de deshacer. El asistente de trabajo para proyectos y el chatbot quedan para más adelante.

**Con qué base lo decimos.** La muestra es pequeña para considerarse un problema amplio, pero es un problema que parece recurrente. Dos profesoras que usan mucho Notion están disponibles como *beta testers*, y el desarrollo del MVP nos permitirá comprobar las hipótesis con uso real.

## 2. Punto de partida

### 2.1. La idea inicial

Oracle nació como un asistente para consultar un *Second Brain* en Notion mediante una conversación: recuperar y sintetizar información de las notas, con referencias a las páginas de origen. El problema que queríamos resolver era el de los sistemas que crecen sin control hasta que consultarlos deja de ser práctico.

### 2.2. Qué teníamos construido

- **Una prueba de concepto local:** lee cuatro páginas raíz de Notion (*Projects*, *Areas*, *Resources* y *Archive*), las indexa con RAG y permite chatear con ellas desde una interfaz en Gradio.
- **Una prueba mínima de despliegue *serverless*** en AWS.
- **Documentos de producto y arquitectura:** `PRODUCT_BRIEF.md`, `SPEC.md` y `CLOUD_DESIGN.md`, que describen un chatbot con RAG sobre microservicios en AWS.

Todo esto es historia y punto de partida, no una restricción para el MVP.

### 2.3. El cambio de enfoque

El proyecto nació con un objetivo sobre todo técnico. Al pasar a un enfoque de producto, decidimos hablar con usuarios y analizar alternativas antes de construir. Primero nos centramos en la etapa *Express*, pero la investigación nos llevó a priorizar la organización, como se explica en las secciones siguientes.

## 3. Usuario objetivo

Nuestro usuario objetivo inicial es **una persona que usa un sistema de *Second Brain* o toma notas de forma sistemática y tiene dificultades para**:

- organizar la información;
- mantenerla al día;
- recuperarla o usarla cuando hace un trabajo importante.

No todas las personas que usan estos sistemas tienen estas dificultades: quien ya tiene un método que le funciona no forma parte de nuestro usuario objetivo, pero nos puede enseñar mucho sobre qué evitar (ver [vogelke](#42-conversaciones-en-rsecondbrain)).

## 4. Investigación con usuarios

### 4.1. Metodología y limitaciones

Entre octubre y noviembre de 2026 buscamos entender las dificultades reales a lo largo del método **CODE** de Tiago Forte: *Capture* (capturar), *Organise* (organizar), *Distil* (destilar) y *Express* (expresar, es decir, aplicar lo guardado para crear o decidir).

Lo que hicimos:

- Participamos en un [hilo sobre la dificultad de llegar a la etapa *Express*](https://www.reddit.com/r/secondbrain/comments/1x6o0vj/how_often_does_your_second_brain_actually_get_to/) en r/secondbrain.
- Publicamos un [hilo propio para hablar de problemas reales con el *Second Brain*](https://www.reddit.com/r/secondbrain/comments/1xipx4a/second_brain_user_in_problems_and_building_a/).
- Continuamos la conversación con tres participantes mediante comentarios y mensajes.
- Roberto consultó a dos profesoras de inglés que usan mucho Notion.

**Limitaciones de esta evidencia:**

- La muestra es pequeña: no permite afirmar qué le ocurre a la mayoría de los usuarios.
- Son intercambios escritos, no entrevistas en profundidad.

Por eso, se separa lo que dijeron los usuarios de lo que interpretamos nosotros.

### 4.2. Conversaciones en r/secondbrain

#### e3e6: el problema sin resolver más claro

- **Qué nos contó:** a veces no escribe nada porque no sabe dónde ponerlo; otras veces sabe que lo apuntó "en algún sitio", pero no lo encuentra. Tiene las notas repartidas entre varias aplicaciones y espacios de Notion.
- **Solución actual:** no describió ningún método que le resuelva estos problemas.
- **Nuestra interpretación:** es el ejemplo más claro de una necesidad no cubierta al organizar y recuperar notas. No hay evidencia directa de que quiera ayuda de IA para crear entregables.

#### mrz999: un problema resuelto con una rutina

- **Qué nos contó:** capturar puede resultar abrumador, porque lo que hoy parece esencial mañana puede ser un impulso pasajero.
- **Solución actual:** vacía dos bandejas de entrada (Apple Notes y Drafts) con dos tareas diarias. Cada elemento se convierte en una tarea, un recordatorio o un bloque de tiempo para un proyecto, o se borra. Guarda sus conclusiones en notas permanentes, escritas con sus propias palabras, para reutilizarlas.
- **Nuestra interpretación:** es un flujo eficaz del que aprender. El usuario parece haber resuelto su problema por sí mismo, aunque es una solución muy personal y algo compleja.

#### vogelke: el contraejemplo

- **Qué nos contó:** usa el sistema de archivos de Linux/Unix, con nombres descriptivos y directorios por fecha, y encuentra lo que busca con `locate`, según su relato en menos de cuatro segundos entre más de nueve millones de archivos. Para cada proyecto crea una carpeta con las fuentes que necesita.
- **Su advertencia:** ya construyó sistemas demasiado complejos y acabó abandonándolos.
- **Solución actual:** le resulta suficiente. Preguntado directamente, dijo que no tiene dificultades importantes para conectar y aplicar información de varias fuentes.
- **Nuestra interpretación:** se pueden cubrir estas necesidades con herramientas simples y buenos hábitos. Un producto nuevo debe eliminar fricción real, no añadir otro sistema.

#### Virtual_Loss6666: una referencia, no un testimonio

Solo compartió un enlace a [Hippocampus](https://github.com/marcelinollima/hippocampus), un sistema autoalojado de memoria persistente para Claude Code y clientes MCP. Nos sirve como referencia técnica de cómo se puede abordar el problema.

### 4.3. Feedback de usuarias de Notion

Roberto consultó a dos profesoras de inglés que usan mucho Notion. Este feedback es **de segunda mano** y **se refiere a tareas, no a notas**. Según su resumen, la idea les parece muy buena y les resultaría útil que la aplicación pudiera:

- clasificar automáticamente las tareas por temática (por ejemplo, administrativa, personal, laboral o un tema concreto);
- sugerir cómo organizarlas y gestionarlas, haciendo preguntas cuando haga falta para clasificarlas bien;
- detectar y recordar las más urgentes o importantes, para ayudar a priorizar.

**Nuestra interpretación:** son funciones concretas que nos señalan una dirección, y ambas profesoras están disponibles como *beta testers* del MVP. Es una idea atractiva, lo que no tiene por qué implicar necesariamente que se vaya a usar. 

### 4.4. Patrones y evidencia por etapa de CODE

| Problema o patrón | Evidencia | Fuente |
| --- | --- | --- |
| No saber dónde guardar la información | Directa | e3e6 |
| No encontrar lo que se guardó | Directa | e3e6 |
| Sobrecarga al capturar y filtrar | Directa | mrz999 |
| Complejidad y coste de mantener el sistema | Experiencia pasada y soluciones actuales | vogelke; indirectamente, mrz999 |
| Clasificar y priorizar tareas | Indirecta (de segunda mano) | Profesoras de inglés, vía Roberto |
| Reutilizar conocimiento en proyectos | Prácticas que ya funcionan, sin necesidad no cubierta | mrz999, vogelke |
| Conectar ideas olvidadas mientras se trabaja | Hipótesis del equipo, sin validar | Ninguna directa |

| Etapa | Qué observamos | Fuerza de la evidencia |
| --- | --- | --- |
| **Capturar** | Sobrecarga de información; dudas sobre dónde guardar una nota. | Directa: mrz999, e3e6. |
| **Organizar** | Información fragmentada y estructuras difíciles de mantener; también soluciones que funcionan con rutinas y archivos simples. | Directa e histórica: e3e6, mrz999, vogelke. |
| **Destilar** | Seleccionar lo importante y guardar conclusiones con palabras propias. | Práctica descrita por mrz999; es la fase en la que se han reportado menos problemas. |
| **Expresar** | Usar ideas y fuentes en proyectos; reutilizar conclusiones. | Prácticas descritas por mrz999 y vogelke; **el equipo de Oracle intuye un valor real en esta fase**. |

**Lo que aprendimos:**

1. **Hay flujos de trabajo y problemas muy distintos, más que una necesidad universal.** Algunas personas tienen dificultades para guardar y encontrar sus notas; otras consideran que su sistema funciona.
2. **La señal más clara de un problema sin resolver está en organizar y recuperar**.
3. **La simplicidad es un criterio de producto.** Lo que más se repite es el interés por reducir la fricción, aunque se manifiesta de formas distintas. Si Oracle obliga a mantener otro sistema o a duplicar el trabajo de organización, puede empeorar la experiencia.
4. **La etapa *Express* sigue siendo una hipótesis prometedora, aunque no está validada.** Era nuestra idea de partida, pero las conversaciones con los usuarios parecen apuntar que no es el principal elemento de fricción.
5. **La tecnología por sí sola no nos diferencia.** Ya existen implementaciones de RAG, memoria persistente y búsqueda contextual. El valor debe venir de una experiencia demostrablemente mejor.

## 5. Conclusiones de la reunión de equipo

En la reunión de seguimiento, el equipo revisó la dirección del proyecto y organizó el trabajo de validación.

### Qué acordamos

- **Pasar de las demostraciones técnicas a la validación de producto.** El proyecto nació como un sistema donde aplicar diseño de sistemas e ingeniería de IA. Patri pidió un enfoque más orientado a producto, y el equipo lo aceptó aun sabiendo que suponía trabajo adicional antes de implementar. El trabajo previo de arquitectura no se descarta.
- **Validar antes de construir.** Antes de la siguiente reunión de Product Feedback debíamos identificar usuarios objetivo, hacer al menos una entrevista o encuesta asíncrona y documentar alternativas y competidores.
- **Buscar usuarios en sus comunidades.** Reddit, Twitter, Facebook y LinkedIn, con publicaciones abiertas y contacto personal con quienes respondieran.
- **Preparar tres entregables para la presentación del día 11:** información validada de usuarios, alternativas y competidores documentados, y una propuesta de valor que indique qué se construirá y qué no.

### Qué pensábamos entonces

El problema de partida era que los usuarios capturan y organizan notas, pero rara vez las usan para crear resultados (la etapa *Express*). Arturo lo había observado en las comunidades de *Second Brain*, y el equipo lo reconoció como un problema real, también en su propia experiencia. Como Notion y otras herramientas ya cubren parte del flujo, la diferenciación se buscaba precisamente ahí.

Con esa idea, se propuso:

- recomendar cosas concretas que crear a partir de las notas existentes, como un artículo o una práctica de vocabulario, y permitir crearlas con un clic;
- generar automáticamente informes, diapositivas o artículos, con referencias a las notas de origen;
- combinar el chat con recomendaciones proactivas.

Estas propuestas del equipo quedaban pendientes de contrastar con usuarios.

### Qué ha pasado desde entonces

| Compromiso | Estado |
| --- | --- |
| Contactar con miembros de la comunidad de Second Brain en Reddit | Hecho (ver [4.1](#41-metodología-y-limitaciones)) |
| Contactar con usuarios que usan mucho Notion | Hecho (ver [4.3](#43-feedback-de-usuarias-de-notion)) |
| Buscar comunidades en Facebook y LinkedIn | Sin resultados documentados |
| Documentar alternativas y competidores | Hecho (ver [sección 6](#6-competidores-y-alternativas)) |
| Definir qué se construye y qué no | Decidido, pendiente de validar (ver [sección 9](#9-decisión-sobre-el-mvp)) |

**El principal cambio:** la investigación no confirmó el punto de partida. Las conversaciones no demostraron que los participantes tengan una necesidad no cubierta en *Express*; la señal más clara apareció antes, al organizar y recuperar la información. Por eso el equipo ha replanteado la prioridad, como se explica en la [sección 9](#9-decisión-sobre-el-mvp).

## 6. Competidores y alternativas

Analizamos las alternativas para un asistente que organice notas ya existentes, empezando por Notion. Esta sección resume el [informe completo](https://github.com/ajimenez78/oracle/blob/develop/docs/product_feedback/reports/Competidores%20asistente%20organizaci%C3%B3n%20notas.md), con datos a 9 de noviembre de 2026.

**Conclusión principal:** el mayor competidor es la propia Notion, seguida de Claude o ChatGPT conectados a Notion. Identificamos una oportunidad que no estaría cubierta.

### 6.1. Soluciones analizadas

- **Notion AI.** Según Notion, su agente crea y edita páginas y bases de datos, y Autofill clasifica filas. Plan Mode hace preguntas antes de actuar. Una página comercial promete ordenar páginas dispersas, pero la ayuda del agente no menciona mover páginas. Los planes Free y Plus solo tienen una prueba de la IA.
- **Claude o ChatGPT con Notion MCP.** MCP es el conector oficial que permite a asistentes externos usar Notion, e incluye herramientas para editar y mover páginas. Es la alternativa de "no comprar nada nuevo" para usuarios técnicos, aunque no ofrece un flujo pensado para organizar. No encontramos ningún relato en primera persona de reorganizar a escala un Notion personal.
- **Mem.** Promete encargarse de organizar, pero dentro de su propia aplicación, y no consta que se conecte con Notion. Hoy se presenta como un "jefe de gabinete" con IA. Interpretamos esto como un cambio de posicionamiento; no conocemos la causa.
- **Obsidian (Note Companion y Copilot).** Note Companion sugiere o aplica carpeta, etiquetas y título a las notas de la bandeja de entrada. Copilot no es un organizador, pero ejecuta agentes con permisos y vista de cambios. Son competencia indirecta para un producto sobre Notion.
- **Plantillas PARA.** Forte Labs y Thomas Frank, entre otros, ofrecen plantillas para Notion. Sirven para empezar de cero; a nuestro juicio, no resuelven el desorden que ya existe.

**Otras alternativas, adyacentes o marginales:**

- **Automatizaciones como Zapier, n8n o Make:** clasifican entradas nuevas de Notion, muy cerca de lo que piden las profesoras. Las plantillas revisadas no anuncian limpieza del histórico.
- **Fabric, Recall y Saner.AI:** prometen evitar la organización manual. Fabric usa Notion como fuente, sin escritura documentada.
- **Capacities, Tana y Heptabase:** exigen migrar a otra aplicación.
- **Motion, Reclaim, Todoist, Akiflow y Sunsama:** coinciden en priorizar tareas, no en organizar notas.
- **Khoj Cloud:** cerró el 15 de abril de 2026.

### 6.2. Comparativa

| Alternativa | ¿Trabaja en tu Notion? | Reorganizar lo existente (según su documentación) | Preguntas y revisión documentadas |
| --- | --- | --- | --- |
| **Notion AI** | Sí, de forma nativa | Clasifica filas y edita páginas y bases; la ayuda no menciona mover páginas | Plan Mode, aprobación de ediciones e historial |
| **Claude o ChatGPT con MCP** | Sí, con conector | Claude: herramienta para mover, sin flujo propio. ChatGPT: escritura sin detalle por plan | Depende del cliente |
| **Mem** | No consta conexión | Auto-organize en su propia aplicación | Sugerir y aceptar |
| **Obsidian** | No | Note Companion: bandeja de entrada. Copilot: por instrucciones | Copilot: permisos y vista de cambios |
| **Plantillas PARA** | Se instalan | Estructura vacía | No aplica |

### 6.3. Oportunidad de diferenciación

*Esta parte es una interpretación nuestra a partir de la documentación revisada.*

Algunas de estas herramientas ya realizan algunas de las funciones propuestas:

- **Clasificar:** ya lo hacen Autofill o Zapier.
- **Revisar y deshacer:** aparece en varias herramientas, así que es un requisito, no una ventaja.
- **Hacer preguntas, sin más:** ya lo realiza Plan Mode.

Hay una combinación que no vimos documentada en ninguna herramienta revisada:

1. Auditar un Notion ya existente.
2. Proponer un mapa, PARA u otro.
3. Preguntar solo por las notas dudosas.
4. Aplicar los cambios por lotes, con opción de deshacer.
5. Mantener el orden después.

Sus destinatarios serían personas no técnicas, sobre todo en los planes Free y Plus, que no incluyen la IA de Notion más allá de una prueba.

### 6.4. Qué dice la evidencia externa sobre la demanda

**No encontramos ninguna encuesta que compare captura, organización, recuperación y uso.** No podemos afirmar que organizar sea el problema principal de la mayoría pero sí que es un dolor recurrente para algunas personas.

| A favor | En contra |
| --- | --- |
| e3e6 a veces no escribe porque no sabe dónde guardar | "Basta con buscar": [un estudio de IBM de 2011](https://www.technologyreview.com/2011/05/20/194578/stop-organizing-your-e-mail-says-study/) halló que quienes no archivaban encontraban sus correos más rápido e igual de bien (solo correo, anterior a los modelos de lenguaje). vogelke defiende lo mismo |
| Dos profesoras valoran la clasificación automática, aunque hablan de tareas | Quizá el dolor esté en recuperar: [un estudio con 27 entrevistas](https://aisel.aisnet.org/ecis2026/cog_hbis/cog_hbis/38/) habla de gestionar, recuperar y aplicar conocimiento disperso, sin medir frecuencias |
| [Una persona en el foro de Obsidian](https://forum.obsidian.md/t/help-finding-a-workflow-for-organizeing-notes-using-a-llm/114174) pide una IA que reparta contenido y le deje aprobar cada movimiento (anécdota) | Organizar puede ser la trampa: [Westenberg](https://westenberg.beehiiv.com/p/i-deleted-my-second-brain) borró unas 10.000 notas porque el sistema aplazaba el pensar. Un organizador podría hacer más eficiente esa conducta |
| [Un estudio de 2010](https://www.tau.ac.il/education/muse/publications/101.pdf) con 296 personas halló un 94 % de éxito navegando por carpetas (anterior a los modelos de lenguaje) | Hay quien ya está bien: mrz999 y vogelke tienen métodos que les funcionan |

**Nota importante:** Hemos hallado que la organización inicial de las notas y el mantenimiento de esa organización supone un problema para algunos usuarios, pero eso no evidencia que un repositorio de notas ordenado vaya a mejorar la recuperación con IA frente a notas desordenadas.

### 6.5. Límites de esta investigación

- **No hicimos pruebas prácticas:** todo sale de documentación y relatos.
- **Las comunidades consultadas son sobre todo técnicas**.
- **La tracción es débil:** hay descargas acumuladas, estrellas y cifras del propio proveedor, sin datos de retención.
- **Casi todas las quejas sobre Notion son anteriores a sus agentes de octubre de 2026.**

## 7. Propuesta de diferenciación

*Esta sección es una propuesta del equipo, todavía sin probar con usuarios.*

**Oracle ordena el Notion que ya tienes, sin que tengas que montar nada, y sin cambiar nada que no hayas aprobado.**

### 7.1. Cómo funcionaría

1. **Audita** el espacio de Notion y detecta dónde hay desorden.
2. **Propone un mapa** de organización, con PARA como opción de partida y adaptable a cada persona.
3. **Pregunta solo por las notas dudosas**, para no convertir la revisión en otra tarea pesada.
4. **Aplica los cambios por lotes**, con aprobación previa y opción de deshacer.
5. **Mantiene el orden después**, sugiriendo dónde colocar cada nota nueva con el mismo mapa.

### 7.2. En qué nos diferenciamos de cada alternativa

| Alternativa | Qué deja sin cubrir | Qué ofrecería Oracle |
| --- | --- | --- |
| **Notion AI** | El agente se puede usar para organizar, pero el usuario tiene que saber pedirlo. Free y Plus solo tienen una prueba | Un flujo ya preparado, de principio a fin, también para esos planes |
| **Claude o ChatGPT con MCP** | Hay que conectarlo, escribir las instrucciones y controlar los cambios | Sin instrucciones ni configuración técnica, con una cola de revisión |
| **Mem** | Organiza dentro de su propia aplicación | Sin migrar: las notas siguen en Notion |
| **Obsidian** | Está fuera de Notion | Trabaja donde ya están las notas de nuestro usuario objetivo |
| **Plantillas PARA** | Dan una estructura vacía | Parte de las notas que ya existen |
| **Zapier, n8n o Make** | Las plantillas revisadas clasifican entradas nuevas | Incluye el histórico y usa un mapa común para lo nuevo |

### 7.3. Dónde no competimos

- **Clasificar sin más:** ya está cubierto.
- **Chat o búsqueda sobre las notas:** Notion AI y los asistentes generales ya lo ofrecen.
- **Gestión de tareas y prioridades:** es otro mercado, con competidores propios.
- **Una aplicación de notas nueva:** contradice lo que aprendimos sobre no añadir otro sistema que mantener.

### 7.4. Qué tendría que ser cierto

Vemos recorrido a esta propuesta si se cumplen las siguientes condiciones:

- **Hay un problema suficiente:** ordenar un Notion existente debe importar a suficientes personas.
- **Ordenar aporta valor:** especialmente para usuarios que ya utilicen mayoritariamente la búsqueda con IA. Si ésta funciona igual de bien sobre notas desordenadas, el argumento se debilita.
- **El flujo supera a la alternativa gratuita o barata:** debe ser mejor que pedírselo directamente a Notion AI o a Claude.
- **Los usuarios confían y aceptan:** deben aprobar una parte importante de las sugerencias y permitir que se escriba en su espacio.

**Esta diferenciación es sobre todo de experiencia, y por tanto fácil de copiar.** Notion podría lanzar un flujo parecido, y una *skill* compartida podría cubrir a los usuarios técnicos. Además, centrarnos en Notion deja fuera parte del problema de e3e6, que tiene las notas repartidas entre varias aplicaciones.

## 8. Hipótesis

Son las suposiciones que deben cumplirse para que la propuesta de la [sección 7](#7-propuesta-de-diferenciación) funcione. Están ordenadas por prioridad: primero, las que harían caer la propuesta y se pueden comprobar con menos esfuerzo. Ninguna está validada, y los umbrales concretos se fijarán en la [sección 11](#11-próximos-pasos).

| # | Hipótesis | Evidencia actual | Cómo validarla | Qué la refutaría |
| --- | --- | --- | --- | --- |
| **H1** | Para algunos usuarios de Notion, tener su espacio desordenado es un problema que quieren resolver | Miembros de la comunidad de second brain y en el foro de Obsidian | Hablar con las profesoras y con más usuarios de Notion sobre su última dificultad real con sus notas | Que el dolor real esté en otra parte, como tareas o recuperación, o que no les importe lo suficiente para actuar |
| **H2** | Un espacio ordenado mejora la recuperación y el uso de las notas, también con búsqueda por IA | **Abierta.** Solo estudios anteriores a los modelos de lenguaje y anécdotas, con opiniones en ambos sentidos | Hacer las mismas preguntas a una IA antes y después de ordenar el espacio de un *beta tester* | Que las respuestas no mejoren de forma apreciable |
| **H3** | Un flujo guiado es claramente mejor que pedírselo directamente a Notion AI o a Claude | **Sin probar.** Solo comparamos documentación | Reorganizar copias del mismo espacio con las tres opciones y comparar tiempo, errores y correcciones | Que Notion AI o Claude logren un resultado similar con un esfuerzo parecido |
| **H4** | Los usuarios confiarán en las sugerencias y permitirán escribir en su espacio si pueden revisar y deshacer | **Anecdótica.** Una petición de aprobar cada movimiento | Medir sugerencias aceptadas, cambios revertidos y tiempo de revisión con usuarios reales | Que rechacen muchas sugerencias, no concedan permisos o la revisión les resulte pesada |
| **H5** | Una vez ordenado el espacio, seguirán usando Oracle para mantenerlo | Los usuarios se quejan del mantenimiento, pero no hay datos de uso continuado | Observar si los *beta testers* siguen usándolo tras la primera limpieza | Que sea un uso puntual |
| **H6** | La IA puede deducir de las notas existentes una organización adaptada a cada usuario, partiendo de PARA y sin que tenga que configurar nada | Los participantes organizan sus notas de formas muy distintas (mrz999, vogelke, e3e6). PARA es una idea del equipo: ningún participante lo pidió, pero es la propuesta de Tiago Forte, creador de second brain | Ver cuánto modifican los usuarios el mapa propuesto | Que lo cambien casi siempre, que no lo entiendan o que tengan que configurarlo a mano |

**Primeros pasos:**

- **H1:** al enseñarles la primera versión, preguntar a las profesoras si su problema son tareas o notas y si siguen un sistema de *Second Brain* o similar.
- **H2 y H3:** requieren pruebas prácticas que haremos con esa primera versión.

### Hipótesis que dejamos para más adelante

- **Asistente de trabajo (*Express*):** ayudar a usar las notas en proyectos relevantes puede tener mucho potencial, pero las conversaciones no demostraron que exista esa necesidad.
- **Asistente conversacional:** puede ser valioso, pero Notion AI y los asistentes generales ya ofrecen chat sobre las notas.
- **Varias fuentes:** conectar otras aplicaciones respondería al problema de e3e6, pero no entra en un primer producto centrado en Notion.

## 9. Decisión sobre el MVP

**Vamos a construir primero un asistente que ayude a organizar las notas que ya existen en Notion.**

*Esta sección recoge una decisión del equipo. Es una apuesta razonada, no un resultado validado.*

Elegimos organizar porque es donde vimos la señal más clara de un problema sin resolver, sobre todo en el caso de e3e6, y porque en *Express* no encontramos ninguna necesidad demostrada. La muestra es pequeña, así que no podemos afirmar que sea el problema principal de la mayoría. Estas decisiones pueden cambiar según lo que aprendamos del mercado, empezando por las [hipótesis de la sección 8](#8-hipótesis).

### 9.1. Qué construimos

| Paso | Qué hará el MVP |
| --- | --- |
| **1. Conectar** | El usuario conecta su Notion y elige qué páginas puede ver Oracle. |
| **2. Auditar** | Oracle lee esas páginas y detecta las que parecen desordenadas o mal ubicadas. |
| **3. Proponer un mapa** | Sugiere una organización, con PARA como punto de partida, que el usuario puede cambiar. |
| **4. Preguntar** | Pregunta solo por las notas que no sabe clasificar con claridad. |
| **5. Revisar y aplicar** | Muestra los movimientos propuestos y aplica por lotes solo los que el usuario aprueba. |
| **6. Deshacer** | Guarda la ubicación original de cada nota para poder devolver un lote a su sitio. |
| **7. Volver a ejecutar** | El usuario puede lanzar de nuevo el flujo sobre sus notas nuevas, con el mismo mapa. |

**Límites del MVP.** El equipo solo dispone de unas pocas horas a la semana, así que acotamos el alcance:

- Solo Notion, y para un grupo reducido de *beta testers*.
- Oracle solo mueve páginas: no edita su contenido, no las renombra y no las borra.
- Todo se ejecuta a petición del usuario, sin sincronización ni cambios automáticos.
- Una interfaz web sencilla, centrada en la revisión de los cambios.

**Viabilidad técnica.** La API de Notion permite [mover páginas a otra página o a una base de datos](https://developers.notion.com/reference/move-page), pero solo páginas normales; las bases de datos no se pueden mover con esa operación. Por eso, si las notas de los *beta testers* están en bases de datos, quizá haya que organizarlas con propiedades en lugar de moverlas. Es una duda nuestra, que aclararemos con ellos al enseñarles la primera versión.

### 9.2. Qué modificamos

- **La etapa *Express* cambia de forma y de momento.** Era el centro del proyecto, con un buscador contextual. Queda para más adelante y, en lugar de un simple buscador, será un asistente de trabajo para proyectos relevantes.
- **Oracle pasa de leer a escribir en Notion.** Hasta ahora era de solo lectura; ahora podrá mover páginas, siempre con aprobación previa.
- **PARA pasa de estructura fija a propuesta adaptable.** La prueba de concepto partía de cuatro páginas raíz fijas (*Projects*, *Areas*, *Resources* y *Archive*). PARA es una idea del equipo y de esa prueba de concepto, no una petición de los usuarios ([H6](#8-hipótesis)).
- **Adaptamos a las notas una petición que se refería a tareas.** Clasificar por temática y preguntar cuando haga falta son ideas que vienen del feedback de segunda mano de las profesoras, que hablaba de tareas. Aplicarlas a notas es decisión nuestra, y aún tenemos que comprobar con ellas si les sirve.

### 9.3. Qué posponemos o descartamos

| Funcionalidad | Decisión | Motivo |
| --- | --- | --- |
| **Asistente de trabajo (*Express*)** | Posponer | Puede tener mucho potencial, pero no hemos demostrado la necesidad |
| **Recomendar qué crear y generar entregables** | Posponer, como parte del asistente de trabajo | Las conversaciones no mostraron esta demanda |
| **Asistente conversacional sobre las notas** | Posponer | Puede ser valioso, pero no es el foco y Notion AI y otros asistentes ya lo ofrecen |
| **Mantenimiento automático** | Posponer | Primero hay que ver si vuelven a usarlo a petición ([H5](#8-hipótesis)) |
| **Otras fuentes además de Notion** | Posponer | Respondería al problema de e3e6, pero amplía demasiado el primer producto |
| **Priorizar y recordar tareas** | Descartar por ahora | Lo pidieron las profesoras, pero es otro mercado con competidores propios |
| **Una aplicación de notas nueva** | Descartar | Contradice lo aprendido: no añadir otro sistema que mantener |

### 9.4. Qué cambia respecto al alcance original

| Aspecto | Alcance original (`PRODUCT_BRIEF.md` y `SPEC.md`) | MVP actual |
| --- | --- | --- |
| **Objetivo** | Recuperar y sintetizar información de las notas | Organizar las notas ya existentes |
| **Función principal** | Chatbot con RAG y citas de las fuentes | Flujo guiado de auditoría, revisión y aplicación de cambios |
| **Etapa *Organizar*** | Fuera del alcance | Centro del producto |
| **Escritura en Notion** | Fuera del alcance | Mover páginas, con aprobación previa |
| **Interfaz** | Chat en React | Pantalla de revisión de cambios |
| **Arquitectura** | Microservicios *serverless* en AWS con índice vectorial | La más simple que permita probar con *beta testers*; se definirá en el diseño técnico |
| **Plazo** | 8 semanas | Sin esa ventana; se mantiene el límite de pocas horas semanales |

**Qué podemos reutilizar.** La lectura de páginas de Notion de la prueba de concepto (recorrido de bloques, paginación y extracción de texto) y, si encaja, parte del trabajo de arquitectura en AWS. En cambio, el chat y la indexación vectorial no son necesarios para esta primera versión. Esos documentos y el código quedan como historia y punto de partida.

### 9.5. Por qué usar IA

La IA actuará como asistente para categorizar y organizar las notas: el usuario decide y Oracle no cambia nada sin su aprobación.

**Dónde la usamos.** Clasificar una nota exige entender su contenido, y las notas desordenadas rara vez lo dejan ver en el título, la carpeta o las etiquetas. Las reglas fijas no bastan para eso; un modelo de lenguaje sí puede:

- **Auditar:** detectar notas mal ubicadas por lo que dicen, no por cómo se llaman.
- **Proponer el mapa:** cada persona organiza sus notas a su manera, así que la IA deduce de las notas que ya existen sus temas y proyectos reales y adapta PARA a ellos, sin configuración ([H6](#8-hipótesis)).
- **Saber cuándo dudar:** colocar las notas claras y reservar las dudosas para preguntar al usuario.
- **Explicar cada propuesta:** dar un motivo breve que haga la revisión rápida.

**Dónde no la usamos.** Mover páginas, aplicar lotes y deshacer son operaciones directas sobre la API de Notion, sin IA. Así los cambios son predecibles y siempre reversibles.

**Qué nos diferencia.** La IA por sí sola no es la ventaja: Notion AI y Claude también la tienen. Lo que aportamos es el flujo que la rodea, y que ese flujo merezca la pena es lo que comprobaremos con [H2 y H3](#8-hipótesis).

## 10. Riesgos y preguntas abiertas

### Riesgos y cómo los abordamos

| Riesgo | Cómo lo abordamos |
| --- | --- |
| **Notion puede lanzar un flujo parecido** o cambiar sus funciones y planes | Avanzar en pasos pequeños y mantener el foco en la experiencia completa, para poder adaptarnos |
| **Una *skill* compartida para Claude** puede cubrir a los usuarios técnicos | Dirigirnos a personas no técnicas, sin instrucciones ni configuración |
| **Mover notas por error** o que los usuarios no quieran dar permisos de escritura | Solo mover páginas, con aprobación previa y opción de deshacer desde la primera versión |
| **Sugerencias de poca calidad** de la IA | Preguntar por las notas dudosas y medir cuántas sugerencias se aceptan |
| **Pocas horas de dedicación del equipo** | Alcance acotado, entregas pequeñas y reutilizar la lectura de Notion que ya existe |
| **Pocos *beta testers*** | Empezar con las dos profesoras e invitar a participantes de r/secondbrain y a otros usuarios de Notion |

### Preguntas abiertas

- **¿Las profesoras tienen este problema con sus notas?** Su feedback, de segunda mano, se refería a tareas.
- **¿Sus notas están en páginas o en bases de datos?** La respuesta puede cambiar cómo aplicamos el mapa de organización.
- **¿Ordenar mejora la recuperación con IA?** No hemos encontrado una comparación directa ([H2](#8-hipótesis)).
- **¿Volverán a usar Oracle después de la primera limpieza?** ([H5](#8-hipótesis))
- **¿Hasta dónde llega centrarse solo en Notion?** e3e6, por ejemplo, tiene las notas repartidas entre varias aplicaciones.

## 11. Próximos pasos

### 11.1. Plan

1. **Construir una primera versión con escritura desde el principio.** Oracle audita, propone el mapa y los movimientos, aplica los que el usuario aprueba y permite deshacerlos.
2. **Enseñársela a las profesoras (H1).** Comprobar con ella si el problema está en sus tareas o en sus notas, y si estas están en páginas o en bases de datos.
3. **Ampliar el grupo de *beta testers*.** Invitar a participantes de r/secondbrain y a otros usuarios de Notion.
4. **Hacer las pruebas prácticas (H2 y H3).** Usar esa versión sobre copias de un espacio de Notion y ajustar el alcance según los resultados.
5. **Revisar el resultado con el equipo** y decidir los siguientes pasos, incluido el momento de retomar el asistente de trabajo.

### 11.2. Criterios de éxito

*Son umbrales orientativos, propuestos por el equipo y pendientes de ajustar. Con tan pocos usuarios sirven para orientar decisiones, no como medida estadística.*

| Hipótesis | Criterio de éxito |
| --- | --- |
| **H1.** El desorden es un problema real | Al menos dos *beta testers* describen una dificultad reciente y concreta con sus notas |
| **H2.** Ordenar mejora la recuperación | De 10 preguntas hechas a una IA antes y después de ordenar, mejoran al menos 3 y no empeora más de 1 |
| **H3.** El flujo guiado supera a las alternativas | En el mismo espacio, requiere menos tiempo y menos correcciones que Notion AI y que Claude |
| **H4.** Los usuarios confían en las sugerencias | Se acepta al menos el 70 % de las sugerencias y se deshace menos del 10 % de los movimientos aplicados |
| **H5.** Siguen usando Oracle | Al menos la mitad de los *beta testers* vuelve a ejecutarlo por iniciativa propia en las 4 semanas siguientes |
| **H6.** PARA es un buen punto de partida | Al menos la mitad de los *beta testers* lo mantiene con cambios menores |

## Referencias

**Conversaciones con usuarios**

- [How often does your Second Brain actually get to "Express"?](https://www.reddit.com/r/secondbrain/comments/1x6o0vj/how_often_does_your_second_brain_actually_get_to/) (hilo de r/secondbrain)
- [Second Brain user in problems and building a…](https://www.reddit.com/r/secondbrain/comments/1xipx4a/second_brain_user_in_problems_and_building_a/) (hilo propio en r/secondbrain)
- [Organizing my Stuff](https://bezoar.org/posts/2020/0203/organizing-my-stuff/) (artículo compartido por vogelke)
- [Hippocampus](https://github.com/marcelinollima/hippocampus) (compartido por Virtual_Loss6666)

**Competidores y evidencia externa**

- [Informe completo de competidores](https://github.com/ajimenez78/oracle/blob/develop/docs/product_feedback/reports/Competidores%20asistente%20organizaci%C3%B3n%20notas.md), con las fuentes de cada herramienta analizada
- [Estudio de IBM sobre archivar el correo (2011)](https://www.technologyreview.com/2011/05/20/194578/stop-organizing-your-e-mail-says-study/)
- [Estudio con 27 entrevistas sobre conocimiento disperso](https://aisel.aisnet.org/ecis2026/cog_hbis/cog_hbis/38/)
- [Estudio con 296 personas sobre navegación por carpetas (2010)](https://www.tau.ac.il/education/muse/publications/101.pdf)
- [Petición en el foro de Obsidian](https://forum.obsidian.md/t/help-finding-a-workflow-for-organizeing-notes-using-a-llm/114174)
- [*I deleted my second brain*, de Westenberg](https://westenberg.beehiiv.com/p/i-deleted-my-second-brain)
- [API de Notion: mover una página](https://developers.notion.com/reference/move-page)

**Documentos internos**

- [Entrevistas con usuarios](https://github.com/ajimenez78/oracle/blob/develop/docs/product_feedback/user_interviews.md)
- [Notas de la reunión de equipo](https://github.com/ajimenez78/oracle/blob/develop/docs/product_feedback/product_recap_meeting_notes.md)
- [`PRODUCT_BRIEF.md`](https://github.com/ajimenez78/oracle/blob/develop/docs/PRODUCT_BRIEF.md), [`SPEC.md`](https://github.com/ajimenez78/oracle/blob/develop/docs/SPEC.md) y [`CLOUD_DESIGN.md`](https://github.com/ajimenez78/oracle/blob/develop/docs/CLOUD_DESIGN.md)
