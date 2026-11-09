# Oracle: aprendizajes de la fase de Product Feedback

> **Estado:** borrador en curso. Las notas entre corchetes indican qué falta y en qué paso de `PLAN.md` se completa.

## 1. Resumen ejecutivo

[Paso 9. El problema identificado, qué hemos aprendido y qué vamos a construir, en pocas líneas.]

## 2. Punto de partida

[Paso 9. La idea inicial, qué existe hoy y por qué pasamos de un enfoque técnico a uno de producto.]

### 2.1. La idea inicial
### 2.2. Qué teníamos construido
### 2.3. El cambio de enfoque

## 3. Usuario objetivo

Nuestro usuario objetivo inicial es **una persona que usa un sistema de *Second Brain* o toma notas de forma sistemática y tiene dificultades para**:

- organizar la información;
- mantenerla al día;
- recuperarla o usarla cuando hace un trabajo importante.

La investigación matiza esta definición. No todas las personas que usan estos sistemas tienen estas dificultades: quien ya tiene un método que le funciona no forma parte de nuestro usuario objetivo, aunque nos enseñe mucho sobre qué evitar (ver [vogelke](#42-conversaciones-en-rsecondbrain)).

## 4. Investigación con usuarios

### 4.1. Metodología y limitaciones

Entre octubre y noviembre de 2026 buscamos entender las dificultades reales a lo largo del método **CODE** de Tiago Forte: *Capture* (capturar), *Organise* (organizar), *Distil* (destilar) y *Express* (expresar, es decir, aplicar lo guardado para crear o decidir).

Lo que hicimos:

- Participamos en un [hilo sobre la dificultad de llegar a la etapa *Express*](https://www.reddit.com/r/secondbrain/comments/1x6o0vj/how_often_does_your_second_brain_actually_get_to/) en r/secondbrain.
- Publicamos un [hilo propio para hablar de problemas reales con el *Second Brain*](https://www.reddit.com/r/secondbrain/comments/1xipx4a/second_brain_user_in_problems_and_building_a/).
- Continuamos la conversación con tres participantes mediante comentarios y mensajes.
- Roberto consultó a dos profesoras de inglés que usan mucho Notion.

**Limitaciones de esta evidencia:**

- La muestra es pequeña y no es representativa: no permite afirmar qué le ocurre a la mayoría de los usuarios.
- Son intercambios escritos, no entrevistas estructuradas ni en profundidad.
- Las personas que responden en una comunidad especializada no representan necesariamente a todos los usuarios de estas herramientas.

Por eso, en este documento separamos lo que dijeron los usuarios de lo que interpretamos nosotros.

### 4.2. Conversaciones en r/secondbrain

#### e3e6: el problema sin resolver más claro

- **Qué nos contó:** a veces no escribe nada porque no sabe dónde ponerlo; otras veces sabe que lo apuntó "en algún sitio", pero no lo encuentra. Tiene las notas repartidas entre varias aplicaciones y espacios de Notion.
- **Solución actual:** no describió ningún método que le resuelva estos problemas.
- **Nuestra interpretación:** es el ejemplo más claro de una necesidad no cubierta al organizar y recuperar notas. No hay evidencia directa de que quiera ayuda de IA para crear entregables.

#### mrz999: un problema resuelto con una rutina

- **Qué nos contó:** capturar puede resultar abrumador, porque lo que hoy parece esencial mañana puede ser un impulso pasajero.
- **Solución actual:** vacía dos bandejas de entrada (Apple Notes y Drafts) con dos tareas diarias. Cada elemento se convierte en una tarea, un recordatorio o un bloque de tiempo para un proyecto, o se borra. Guarda sus conclusiones en notas permanentes, escritas con sus propias palabras, para reutilizarlas.
- **Nuestra interpretación:** es un flujo eficaz del que aprender, no una demanda validada. No dijo que su proceso de *Express* falle ni que necesite IA.

#### vogelke: el contraejemplo

- **Qué nos contó:** usa el sistema de archivos de Linux/Unix, con nombres descriptivos y directorios por fecha, y encuentra lo que busca con `locate`, según su relato en menos de cuatro segundos entre más de nueve millones de archivos. Para cada proyecto crea una carpeta con las fuentes que necesita.
- **Su advertencia:** ya construyó sistemas demasiado complejos y acabó abandonándolos.
- **Solución actual:** le resulta suficiente. Preguntado directamente, dijo que no tiene dificultades importantes para conectar y aplicar información de varias fuentes.
- **Nuestra interpretación:** se pueden cubrir estas necesidades con herramientas simples y buenos hábitos. Un producto nuevo debe eliminar fricción real, no añadir otro sistema.

#### Virtual_Loss6666: una referencia, no un testimonio

Solo compartió un enlace a [Hippocampus](https://github.com/marcelinollima/hippocampus), un sistema autoalojado de memoria persistente para Claude Code y clientes MCP. Nos sirve como referencia técnica, pero no es evidencia de un problema ni de interés en Oracle.

### 4.3. Feedback de usuarias de Notion

Roberto consultó a dos profesoras de inglés que usan mucho Notion. Este feedback es **de segunda mano** y **se refiere a tareas, no a notas**. Según su resumen, la idea les parece muy buena y les resultaría útil que la aplicación pudiera:

- clasificar automáticamente las tareas por temática (por ejemplo, administrativa, personal, laboral o un tema concreto);
- sugerir cómo organizarlas y gestionarlas, haciendo preguntas cuando haga falta para clasificarlas bien;
- detectar y recordar las más urgentes o importantes, para ayudar a priorizar.

**Nuestra interpretación:** son funciones concretas que nos señalan una dirección, y ambas profesoras están disponibles como *beta testers* del MVP. Aun así, que una idea guste no demuestra que se vaya a usar. Tampoco sabemos todavía si estas usuarias siguen un sistema de *Second Brain* ni si lo que piden se aplica también a sus notas.

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
| **Destilar** | Seleccionar lo importante y guardar conclusiones con palabras propias. | Práctica descrita por mrz999; ningún problema validado. |
| **Expresar** | Usar ideas y fuentes en proyectos; reutilizar conclusiones. | Prácticas descritas por mrz999 y vogelke; **ningún problema común demostrado**. |

**Lo que aprendimos:**

1. **Hay flujos de trabajo y problemas muy distintos, no una necesidad universal.** Algunas personas tienen dificultades para guardar y encontrar sus notas; otras consideran que su sistema funciona.
2. **La señal más clara de un problema sin resolver está en organizar y recuperar**, sobre todo en el caso de e3e6. Es una señal, no una validación.
3. **La simplicidad es un criterio de producto.** Lo que más se repite es el interés por reducir la fricción, aunque se manifiesta de formas distintas. Si Oracle obliga a mantener otro sistema o a duplicar el trabajo de organización, puede empeorar la experiencia.
4. **La etapa *Express* sigue siendo una hipótesis prometedora, pero no está validada.** Era nuestra idea de partida, y las conversaciones no demostraron que los participantes necesiten IA para crear o conectar ideas.
5. **La tecnología por sí sola no nos diferencia.** Ya existen implementaciones de RAG, memoria persistente y búsqueda contextual. El valor debe venir de una experiencia demostrablemente mejor.

## 5. Conclusiones de la reunión de equipo

En la reunión de seguimiento, el equipo revisó la dirección del proyecto y organizó el trabajo de validación.

### Qué acordamos

- **Pasar de las demostraciones técnicas a la validación de producto.** El proyecto nació para practicar ingeniería. Patri pidió un enfoque más orientado a producto, y el equipo lo aceptó aun sabiendo que suponía trabajo adicional antes de implementar. El trabajo previo de arquitectura no se descarta.
- **Validar antes de construir.** Antes de la siguiente reunión de Product Feedback debíamos identificar usuarios objetivo, hacer al menos una entrevista o encuesta asíncrona y documentar alternativas y competidores.
- **Buscar usuarios en sus comunidades.** Reddit, Twitter, Facebook y LinkedIn, con publicaciones abiertas y contacto personal con quienes respondieran.
- **Preparar tres entregables para la presentación del día 11:** información validada de usuarios, alternativas y competidores documentados, y una propuesta de valor que indique qué se construirá y qué no.

### Qué pensábamos entonces

El problema de partida era que los usuarios capturan y organizan notas, pero rara vez las usan para crear resultados (la etapa *Express*). Arturo lo había observado en las comunidades de *Second Brain*, y el equipo lo reconoció como un problema real, también en su propia experiencia. Como Notion y otras herramientas ya cubren parte del flujo, la diferenciación se buscaba precisamente ahí.

Con esa idea, Roberto propuso:

- recomendar cosas concretas que crear a partir de las notas existentes, como un artículo o una práctica de vocabulario, y permitir crearlas con un clic;
- generar automáticamente informes, diapositivas o artículos, con referencias a las notas de origen;
- combinar el chat con recomendaciones proactivas.

Eran propuestas del equipo, pendientes de contrastar con usuarios.

### Qué ha pasado desde entonces

| Compromiso | Responsable | Estado |
| --- | --- | --- |
| Publicar y gestionar el hilo de Reddit | Arturo | Hecho (ver [4.1](#41-metodología-y-limitaciones)) |
| Contactar con usuarios que usan mucho Notion | Roberto | Hecho (ver [4.3](#43-feedback-de-usuarias-de-notion)) |
| Buscar comunidades en Facebook y LinkedIn | Roberto | Sin resultados documentados |
| Documentar alternativas y competidores | Equipo | Pendiente (sección 6) |
| Definir qué se construye y qué no | Equipo | Pendiente (sección 9) |

**El principal cambio:** la investigación no confirmó el punto de partida. Las conversaciones no demostraron que los participantes tengan una necesidad no cubierta en *Express*; la señal más clara apareció antes, al organizar y recuperar la información. Por eso el equipo ha replanteado la prioridad, como se explica en la [sección 9](#9-decisión-sobre-el-mvp).

## 6. Competidores y alternativas

Analizamos las alternativas para un asistente que organice notas ya existentes, empezando por Notion. Esta sección resume el [informe completo](reports/Competidores%20asistente%20organizaci%C3%B3n%20notas.md), con datos a 9 de noviembre de 2026.

**Conclusión principal:** el mayor competidor es la propia Notion, seguida de Claude o ChatGPT conectados a Notion. Queda una oportunidad estrecha, pero no hemos demostrado ni que ese hueco exista ni que organizar sea el problema que hay que resolver.

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

| Alternativa | ¿Trabaja en tu Notion? | Reorganizar lo existente (según su documentación) | Preguntas y revisión documentadas | Precio |
| --- | --- | --- | --- | --- |
| **Notion AI** | Sí, de forma nativa | Clasifica filas y edita páginas y bases; la ayuda no menciona mover páginas | Plan Mode, aprobación de ediciones e historial | Business, 19,50 € por miembro al mes (sin aclarar el tipo de facturación); Free y Plus, solo prueba |
| **Claude o ChatGPT con MCP** | Sí, con conector | Claude: herramienta para mover, sin flujo propio. ChatGPT: escritura sin detalle por plan | Depende del cliente | Claude Pro, 20 $ al mes; Free en conflicto; ChatGPT sin verificar |
| **Mem** | No consta conexión | Auto-organize en su propia aplicación | Sugerir y aceptar | De 9 $ a 199 $ |
| **Obsidian** | No | Note Companion: bandeja de entrada. Copilot: por instrucciones | Copilot: permisos y vista de cambios | Copilot Free con claves propias; resto sin verificar |
| **Plantillas PARA** | Se instalan | Estructura vacía | No aplica | Hay gratuitas; de pago sin verificar |

### 6.3. Oportunidad de diferenciación

*Esta parte es una interpretación nuestra a partir de la documentación revisada.*

Tres argumentos no bastan para diferenciarnos:

- **Clasificar:** ya lo hacen Autofill, Zapier e incluso un proyecto de concurso.
- **Revisar y deshacer:** aparece en varias herramientas, así que es un requisito, no una ventaja.
- **Hacer preguntas, sin más:** choca con Plan Mode.

Queda una combinación que no vimos documentada en ninguna herramienta revisada, lo que no prueba que no exista:

1. Auditar un Notion ya existente.
2. Proponer un mapa, PARA u otro.
3. Preguntar solo por las notas dudosas.
4. Aplicar los cambios por lotes, con opción de deshacer.
5. Mantener el orden después.

Sus destinatarios serían personas no técnicas, sobre todo en los planes Free y Plus, que no incluyen la IA de Notion más allá de una prueba.

**El riesgo es alto:** Notion controla la plataforma y puede cerrar este hueco cambiando sus funciones o sus planes. Una *skill* o plantilla compartida para Claude también podría cubrir gran parte. Además, no sabemos si estos usuarios pagarían.

### 6.4. Qué dice la evidencia externa sobre la demanda

**No encontramos ninguna encuesta que compare captura, organización, recuperación y uso.** Por eso no podemos afirmar que organizar sea el problema principal de la mayoría; lo defendible es que es un dolor recurrente para algunas personas.

| A favor | En contra |
| --- | --- |
| e3e6 a veces no escribe porque no sabe dónde guardar | "Basta con buscar": [un estudio de IBM de 2011](https://www.technologyreview.com/2011/05/20/194578/stop-organizing-your-e-mail-says-study/) halló que quienes no archivaban encontraban sus correos más rápido e igual de bien (solo correo, anterior a los modelos de lenguaje). vogelke defiende lo mismo |
| Dos profesoras valoran la clasificación automática, aunque hablan de tareas | Quizá el dolor esté en recuperar: [un estudio con 27 entrevistas](https://aisel.aisnet.org/ecis2026/cog_hbis/cog_hbis/38/) habla de gestionar, recuperar y aplicar conocimiento disperso, sin medir frecuencias |
| [Una persona en el foro de Obsidian](https://forum.obsidian.md/t/help-finding-a-workflow-for-organizeing-notes-using-a-llm/114174) pide una IA que reparta contenido y le deje aprobar cada movimiento (anécdota) | Organizar puede ser la trampa: [Westenberg](https://westenberg.beehiiv.com/p/i-deleted-my-second-brain) borró unas 10.000 notas porque el sistema aplazaba el pensar. Un organizador podría hacer más eficiente esa conducta |
| [Un estudio de 2010](https://www.tau.ac.il/education/muse/publications/101.pdf) con 296 personas halló un 94 % de éxito navegando por carpetas (anterior a los modelos de lenguaje) | Hay quien ya está bien: mrz999 y vogelke tienen métodos que les funcionan |

**La pregunta decisiva sigue abierta:** no hallamos ninguna comparación de la recuperación con IA sobre notas desordenadas y ordenadas. Tampoco hay datos de disposición a pagar, y las cifras de tamaño de mercado difieren unas 2,7 veces y no miden este segmento, así que no las usamos. Nuestra formulación más defendible es organizar para que recuperar y usar las notas funcione mejor, no por tener carpetas ordenadas.

### 6.5. Límites de esta investigación

- **No hicimos pruebas prácticas:** todo sale de documentación y relatos, y que algo no esté documentado no significa que no exista.
- **No pudimos leer Reddit ni el foro de Notion** en esta investigación, y las comunidades consultadas son sobre todo técnicas.
- **Algunas afirmaciones se apoyan solo en extractos o resúmenes de páginas.**
- **La tracción es débil:** hay descargas acumuladas, estrellas y cifras del propio proveedor, sin datos de retención.
- **Casi todas las quejas sobre Notion son anteriores a sus agentes de octubre de 2026.**
- **Los precios pueden cambiar**, y los marcados "sin verificar" o "en conflicto" no deben citarse como firmes.

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

Esta propuesta solo se sostiene si se cumplen estas condiciones, y ninguna está comprobada:

- **Hay un problema suficiente:** ordenar un Notion existente debe importar a más personas que e3e6, y las profesoras deben tener ese problema también con sus notas, no solo con sus tareas.
- **Ordenar aporta valor:** si la búsqueda con IA funciona igual de bien sobre notas desordenadas, el argumento se debilita.
- **El flujo supera a la alternativa gratuita o barata:** debe ser claramente mejor que pedírselo directamente a Notion AI o a Claude.
- **Los usuarios confían y aceptan:** deben aprobar una parte importante de las sugerencias y permitir que se escriba en su espacio.
- **Hay un modelo viable:** alguien debe estar dispuesto a pagar, o el coste de la IA debe poder cubrirse en planes Free y Plus.

**Esta diferenciación es sobre todo de experiencia, y por tanto fácil de copiar.** Notion podría lanzar un flujo parecido, y una *skill* compartida podría cubrir a los usuarios técnicos. Además, centrarnos en Notion deja fuera parte del problema de e3e6, que tiene las notas repartidas entre varias aplicaciones.

## 8. Hipótesis

Son las suposiciones que deben cumplirse para que la propuesta de la [sección 7](#7-propuesta-de-diferenciación) funcione. Están ordenadas por prioridad: primero, las que harían caer la propuesta y se pueden comprobar con menos esfuerzo. Ninguna está validada, y los umbrales concretos se fijarán en la [sección 11](#11-próximos-pasos).

| # | Hipótesis | Evidencia actual | Cómo validarla | Qué la refutaría |
| --- | --- | --- | --- | --- |
| **H1** | Para algunos usuarios de Notion, tener su espacio desordenado es un problema que quieren resolver | **Débil.** e3e6, una anécdota en el foro de Obsidian y ninguna encuesta | Hablar con las profesoras y con más usuarios de Notion sobre su última dificultad real con sus notas | Que el dolor real esté en otra parte, como tareas o recuperación, o que no les importe lo suficiente para actuar |
| **H2** | Un espacio ordenado mejora la recuperación y el uso de las notas, también con búsqueda por IA | **Abierta.** Solo estudios anteriores a los modelos de lenguaje y anécdotas, con opiniones en ambos sentidos | Hacer las mismas preguntas a una IA antes y después de ordenar el espacio de un *beta tester* | Que las respuestas no mejoren de forma apreciable |
| **H3** | Un flujo guiado es claramente mejor que pedírselo directamente a Notion AI o a Claude | **Sin probar.** Solo comparamos documentación | Reorganizar copias del mismo espacio con las tres opciones y comparar tiempo, errores y correcciones | Que Notion AI o Claude logren un resultado similar con un esfuerzo parecido |
| **H4** | Los usuarios confiarán en las sugerencias y permitirán escribir en su espacio si pueden revisar y deshacer | **Anecdótica.** Una petición de aprobar cada movimiento | Medir sugerencias aceptadas, cambios revertidos y tiempo de revisión con usuarios reales | Que rechacen muchas sugerencias, no concedan permisos o la revisión les resulte pesada |
| **H5** | Una vez ordenado el espacio, seguirán usando Oracle para mantenerlo | **Débil.** Los usuarios se quejan del mantenimiento, pero no hay datos de uso continuado | Observar si los *beta testers* siguen usándolo tras la primera limpieza | Que sea un uso puntual, lo que debilitaría un modelo de suscripción |
| **H6** | Personas no técnicas en planes Free o Plus pagarían por esto | **Sin datos.** Solo sabemos que estos planes no incluyen la IA de Notion más allá de una prueba | Preguntar qué plan usan y pedir un compromiso concreto de pago | Que nadie se comprometa, o que estén en planes que ya incluyen la IA de Notion |
| **H7** | PARA es un buen mapa de partida, siempre que se pueda adaptar | **Débil.** Es una idea del equipo, ningún participante lo pidió y sus límites ambiguos son una queja repetida | Ver cuánto modifican los usuarios el mapa propuesto | Que lo cambien casi siempre o que no lo entiendan |

**Primeros pasos, por ser los más baratos:**

- **H1 y H6:** preguntar a las profesoras si su problema son tareas o notas, si siguen un sistema de *Second Brain* y qué plan de Notion usan. Es una conversación breve que Roberto puede tener.
- **H2 y H3:** requieren pruebas prácticas que no hemos podido hacer antes de esta presentación. Son las primeras pruebas pendientes después de ella.

### Hipótesis que dejamos para más adelante

- **Asistente de trabajo (*Express*):** ayudar a usar las notas en proyectos relevantes puede tener mucho potencial, pero las conversaciones no demostraron que exista esa necesidad.
- **Asistente conversacional:** puede ser valioso, pero Notion AI y los asistentes generales ya ofrecen chat sobre las notas.
- **Varias fuentes:** conectar otras aplicaciones respondería al problema de e3e6, pero no entra en un primer producto centrado en Notion.

## 9. Decisión sobre el MVP

[Paso 8. Qué construimos, qué modificamos y qué descartamos o posponemos.]

### 9.1. Qué construimos
### 9.2. Qué modificamos
### 9.3. Qué posponemos o descartamos
### 9.4. Qué cambia respecto al alcance original
### 9.5. Por qué usar IA

[Imanol añadirá la justificación.]

## 10. Riesgos y preguntas abiertas

[Paso 9. Riesgos del MVP y lo que todavía no sabemos.]

## 11. Próximos pasos

[Paso 9. Validación con las usuarias beta y criterios de éxito.]

## Referencias

[Paso 9. Hilos de Reddit, herramientas analizadas y documentos internos.]
