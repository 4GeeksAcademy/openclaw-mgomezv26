# Diseño de skills personalizadas — Proyecto 4Geeks

**Estado:** especificación de diseño; no implementa skills ni configura integraciones.

## Skill 1: AI Learning Journal

### 1. ¿Qué hace esta skill?
Convierte los apuntes que Moni aporta sobre 4Geeks en una entrada clara, estructurada y útil para repasar su aprendizaje.

### 2. ¿Qué input necesita el agente?

- **Formato:** texto libre o campos con etiquetas; aceptar información parcial y señalar lo que falte sin inventarlo.
- **Datos proporcionados por Moni:** fecha, tema, conceptos aprendidos, ejemplos, dificultades y dudas. Si la fecha no se proporciona, preguntar o dejarla pendiente; no inferirla silenciosamente.
- **Contexto de configuración disponible:**
  - `IDENTITY.md`: identidad de Pingu; orientar la respuesta con una voz cercana, resolutiva y curiosa.
  - `SOUL.md`: español habitual, explicaciones prácticas y tono natural; al enseñar, guiar con razonamiento y pistas antes de dar una solución completa.
  - `AGENTS.md`: respetar el alcance pedido, proteger datos privados, no inventar hechos y verificar acciones externas.
  - `USER.md`: Moni estudia AI Engineering en 4Geeks, busca trabajar con agentes, LLMs y automatizaciones, domina Python/R/SQL/estadística/ML/análisis espacial y está aprendiendo TypeScript/JavaScript, React, agentes, MCP, OpenClaw y n8n. Usar solo lo pertinente al tema; no dar por supuesto que domina lo que está aprendiendo.
  - `TOOLS.md`: Google Docs y Zapier MCP constan como verificados para lecturas anteriores, pero la creación de documentos no está verificada y sus métodos no aparecen entre las herramientas actualmente expuestas. Respetar las limitaciones registradas.

### 3. ¿Cómo es un buen output?

- **Formato:** Markdown, con título y fecha, seguido de secciones `Resumen`, `Conceptos aprendidos`, `Ejemplos`, `Dificultades`, `Dudas` y `Próximos pasos`. Si no hay información para una sección, indicarlo como pendiente o formular una pregunta; no fabricar contenido. Resumen breve y próximos pasos concretos, verificables y adecuados al nivel indicado por el contexto.
- **Destino previsto:** Google Docs mediante Zapier MCP únicamente si una herramienta de escritura está disponible y la conexión permite crear documentos. Antes de guardar, mostrar el título y contenido propuestos y pedir confirmación, además de resolver cualquier carpeta o destino que falte. Tras autorización, comprobar el resultado mediante una lectura del documento creado.
- **Alternativa si Docs no permite escritura:** entregar la entrada completa en la conversación, lista para copiar. No crear archivos locales como alternativa sin que Moni lo solicite.
- **Criterios verificables de éxito:** aparecen todas las secciones; los datos corresponden al input; los conceptos y ejemplos no se inventan; los próximos pasos se relacionan con las dificultades o dudas; y, si se autorizó guardar en Docs, la lectura de verificación confirma título y contenido esperado. Si no se puede guardar, declararlo claramente y ofrecer el texto en la conversación.

### Justificación, herramientas, límites y errores

El formato consistente facilita repasar y detectar dudas pendientes; los pasos siguientes convierten la reflexión en práctica. La herramienta externa prevista es Google Docs mediante Zapier MCP, pero su escritura no consta verificada en `TOOLS.md`. No configurar APIs, OAuth ni conexiones. No compartir en el documento información personal irrelevante ni secretos. Si falta un dato esencial, preguntar o marcarlo pendiente. Si una herramienta falla o no está disponible, indicar el error real, no afirmar que se guardó y ofrecer el contenido en la conversación.

## Skill 2: MØLI Content Planner

### 1. ¿Qué hace esta skill?
Transforma una idea de contenido de MØLI Studio en una ficha de producción accionable, adaptada al formato y al tono educativo o de gaming/streaming correspondiente.

### 2. ¿Qué input necesita el agente?

- **Formato:** texto libre o campos etiquetados; se puede aceptar una idea inicial incompleta y pedir solo las aclaraciones necesarias.
- **Datos proporcionados por Moni:** tipo de contenido (tutorial de programación/IA, gameplay o futuro directo/streaming), idea o tema, público objetivo, duración aproximada y objetivos.
- **Contexto de configuración disponible:**
  - `IDENTITY.md`: Pingu es cercano, inteligente, curioso y resolutivo; usar esa personalidad al colaborar, no imponerla como voz de MØLI.
  - `SOUL.md`: comunicarse directamente y ajustar el detalle a la tarea; investigar o proponer sin exagerar capacidades.
  - `AGENTS.md`: pedir autorización antes de publicar, compartir o realizar acciones externas; proteger información privada y explicar errores.
  - `USER.md`: MØLI Studio es un proyecto personal en fase inicial; Moni aún no ha publicado vídeos ni hace directos regularmente y quiere empezar desde cero con tutoriales de programación e IA para YouTube, gameplays y streaming en Twitch. Utiliza OBS Studio y quiere usar Discord para la comunidad. Proponer ideas realistas para empezar, sin presentar actividad futura como si ya ocurriera.
  - `TOOLS.md`: Telegram está verificado mediante conversaciones reales con el bot OpenClawPingu; la verificación no prueba permisos adicionales ni permite asumir que esta skill pueda acceder al canal. No se conocen integraciones para OBS Studio, YouTube, Twitch o Discord.

### 3. ¿Cómo es un buen output?

- **Formato:** ficha de producción Markdown con `Título`, `Tipo y plataforma prevista`, `Público objetivo`, `Objetivo`, `Duración aproximada`, `Estructura`, `Propuesta de guion`, `Materiales`, `Checklist de grabación` y `Próximos pasos`. Mantener alternativas claramente marcadas como propuestas, no como hechos. Para tutoriales, usar tono educativo y técnico, pasos comprensibles y una explicación correcta; para gaming y streaming, tono divertido y espontáneo, sin forzar el estilo tutorial. Adecuar el alcance a que MØLI empieza desde cero.
- **Destino previsto:** Telegram solo después de que Moni autorice expresamente el envío del contenido concreto y confirme el chat o destinatario si no está claro. La verificación del canal documentada en `TOOLS.md` no implica que haya una herramienta de Telegram expuesta a esta skill. Si no existe una capacidad de envío disponible, devolver la ficha en la conversación para que Moni la copie; no intentar otra vía.
- **Criterios verificables de éxito:** la ficha incluye todas las secciones; tema, público, duración y objetivo reflejan el input; estructura y guion caben en la duración prevista; checklist accionable; materiales razonables para herramientas confirmadas; tono coherente con el formato; no afirma publicación, grabación ni control de herramientas; y no se envía externamente sin autorización y destino confirmados.

### Justificación, herramientas, límites y errores

La ficha reúne planificación y preparación en un solo entregable, y la separación de tonos evita que los tutoriales técnicos y el gaming suenen iguales. En esta fase solo se contempla redactar la ficha; OBS Studio, YouTube, Twitch y Discord no se controlan por esta especificación. Telegram es un destino potencial, no una capacidad de envío confirmada aquí. No publicar, enviar ni compartir sin autorización explícita; no enviar información privada ni credenciales. Si faltan público, duración u objetivo y afectan materialmente al plan, preguntar; en otro caso, indicar los supuestos como propuestas. Si el canal/herramienta falla o no está disponible, explicar el error y entregar la ficha en la conversación, sin afirmar que se envió.

## Alcance de esta especificación

Este documento diseña el comportamiento esperado; no crea `SKILL.md`, carpetas de skills, documentos de Google ni mensajes de Telegram. Cualquier implementación futura deberá volver a comprobar las capacidades y permisos vigentes en `TOOLS.md` antes de usar servicios externos.
