# Oracle: Resumen de Producto (Product Brief) - v0.1

## 📋 Contexto y Problema
El concepto de *Second Brain* (Segundo Cerebro) de Tiago Forte es un sistema digital de gestión del conocimiento personal diseñado para liberar espacio mental y organizar información, lecturas y notas. Sin embargo, con el volumen de contenido digital que se consume hoy en día, **estos sistemas tienden a crecer descontroladamente**. El usuario promedio de **Notion** sufre de "infoxicación" dentro de su propio espacio de trabajo, lo que convierte su Segundo Cerebro en un cementerio de datos donde el mantenimiento, el refinamiento y la consulta manual se vuelven ineficientes y frustrantes.

## 🎯 Objetivos
El propósito de Oracle es operar sobre el *Second Brain* del usuario bajo demanda para **recuperar, conectar y sintetizar información pertinente en tiempo real**. El sistema debe permitir al usuario realizar consultas conversacionales sobre su propio conocimiento almacenado en Notion, facilitando la conexión de ideas latentes y permitiéndole reutilizar sus notas como bloques de construcción para nuevos proyectos o creaciones.

## 💡 La Solución
Aprovechando las capacidades actuales de la IA Generativa, Oracle implementará una arquitectura de Generación Aumentada por Recuperación (**RAG**) que conecta de forma nativa con la **API de Notion**. 
El sistema migrará de un prototipo local funcional (Gradio + DB local) a una arquitectura **Cloud Serverless en AWS** con un Chatbot web responsivo para garantizar la escalabilidad y el coste cero en reposo.

## 🛑 Alcance y Exclusiones

### Dentro del Alcance (MVP)
* **Ingesta mediante API de Notion:** Sincronización bajo demanda (mediante un botón en la interfaz) que lee las páginas autorizadas por el usuario a través de la integración oficial de Notion.
* **Pipeline RAG en la Nube:** Fragmentación de bloques de texto, generación de *embeddings* e indexación en base de datos vectorial persistida en la nube.
* **Interfaz de Usuario Web:** Aplicación React (Chatbot) que sustituirá a la interfaz de Gradio para permitir despliegues estáticos económicos.
* **Trazabilidad:** Las respuestas del chat incluirán enlaces directos o nombres de las páginas de Notion utilizadas como contexto.

### Fuera del Alcance (Exclusiones del MVP)
* **Sincronización en tiempo real (Webhooks):** El sistema no reaccionará instantáneamente cuando el usuario edite Notion; la actualización se gatillará manualmente desde la app o mediante una tarea periódica en segundo plano.
* **Escritura en Notion:** El sistema es de solo lectura; el LLM no creará ni modificará páginas en el espacio de Notion del usuario.

## ⚠️ Restricciones y Riesgos

* **Disponibilidad del equipo:** Dedicación limitada a unas pocas horas semanales.
* **Tiempo límite (Timeboxing):** Ventana estricta de **8 semanas** para pasar el prototipo local a producción en AWS.
* **Infraestructura (Estrategia AWS Serverless):**
    * **Backend:** AWS Lambda (Python) exponiendo una API REST.
    * **Base de datos vectorial:** Migración del índice local en disco hacia **Amazon S3** (cargado en memoria de la Lambda de forma efímera para entornos pequeños) o **Amazon OpenSearch Serverless** para rendimiento óptimo.
    * **Frontend:** React desplegado en Amazon S3 + CloudFront o AWS Amplify.
