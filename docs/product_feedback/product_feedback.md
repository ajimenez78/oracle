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

[Paso 4. Qué acordó el equipo y cómo cambió el plan.]

## 6. Competidores y alternativas

[Paso 5. Soluciones existentes, qué cubren y qué huecos dejan.]

### 6.1. Soluciones analizadas
### 6.2. Comparativa
### 6.3. Oportunidad de diferenciación

## 7. Soluciones candidatas

[Paso 6. Breve propuesta de las primeras soluciones seleccionadas.]

## 8. Hipótesis

[Paso 7. Cada hipótesis, la evidencia que la apoya y cómo la validaríamos.]

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
