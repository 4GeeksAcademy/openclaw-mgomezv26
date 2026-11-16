---
name: ai-learning-journal
description: Convierte apuntes que Moni aporte sobre 4Geeks en una entrada de diario de aprendizaje estructurada, fiel a sus notas y con próximos pasos. Actívala cuando pida organizar, resumir o guardar una sesión de estudio o aprendizaje.
---

# AI Learning Journal

Convierte las notas de aprendizaje de Moni en una entrada de diario consistente y reutilizable. Redacta en español, con un tono práctico y cercano, y no atribuyas a Moni conocimientos, experiencias o ejemplos que no haya mencionado.

## Cuándo activarla

Actívala cuando Moni pida convertir apuntes, conceptos, ejemplos, dificultades o dudas de 4Geeks en una entrada de diario; también cuando pida guardar esa entrada en Google Docs. Si pide solo una explicación de un concepto y no una entrada de diario, ayúdala normalmente en modo mentor en vez de forzar esta skill.

## Inputs

Acepta texto libre o campos etiquetados. Recoge, cuando estén disponibles:

- Fecha de la sesión.
- Tema.
- Conceptos aprendidos.
- Ejemplos que Moni aporte.
- Dificultades encontradas.
- Dudas pendientes.

Usa el contexto de los archivos de configuración disponibles en el workspace (`IDENTITY.md`, `SOUL.md`, `AGENTS.md`, `USER.md` y `TOOLS.md`) de forma selectiva:

- Mantén la voz de Pingu, el idioma español y el estilo claro y cercano indicados en `IDENTITY.md` y `SOUL.md`.
- Sigue las reglas de privacidad, alcance, autorización y verificación de `AGENTS.md`.
- Adapta las explicaciones al perfil de aprendizaje de `USER.md`: distingue sus conocimientos consolidados de las tecnologías y temas que está aprendiendo; usa AI Engineering y 4Geeks como contexto solo si es pertinente.
- Comprueba las capacidades vigentes descritas en `TOOLS.md` antes de considerar servicios externos. No deduzcas disponibilidad a partir de una mención en estos archivos.

### Datos incompletos

- No inventes fecha, tema, conceptos, ejemplos, dificultades ni dudas.
- Si falta la fecha, pregunta por ella o marca `Pendiente de indicar`; no uses la fecha actual como sustituto silencioso.
- Si falta el tema u otro dato necesario para que la entrada tenga sentido, pide una aclaración concreta antes de cerrar la entrada.
- Para secciones sin información, escribe `Pendiente de indicar` o `No se han aportado datos`, según corresponda. No conviertas ausencia de información en una afirmación sobre lo que Moni sabe o no sabe.
- Puedes proponer preguntas aclaratorias o próximos pasos razonables. Márcalos explícitamente como **Propuesta de Pingu**, separados de los apuntes y hechos aportados por Moni.

## Procedimiento

1. **Reúne y separa la información.** Identifica qué datos aportó Moni y qué campos faltan. Conserva el significado y los matices de sus notas; no añadas supuestos como hechos.
2. **Resuelve bloqueos.** Si falta tema o hay ambigüedad importante, pregunta brevemente. La fecha puede quedar pendiente si Moni prefiere continuar sin ella.
3. **Organiza el aprendizaje.** Agrupa conceptos en el orden más útil para repasar. Relaciona ejemplos, dificultades y dudas con los conceptos solo cuando esa relación esté clara en las notas. No añadas ejemplos inventados ni explicaciones técnicas no solicitadas como si fueran parte de la sesión.
4. **Redacta el resumen.** Resume qué se trabajó y qué aprendió Moni usando exclusivamente la información disponible. Mantén concisión y precisión.
5. **Propón próximos pasos.** Derívalos de dificultades o dudas expresadas, con acciones concretas y pequeñas. Si son inferencias o ideas nuevas, preséntalas como **Propuesta de Pingu**, nunca como un compromiso o decisión de Moni.
6. **Completa la plantilla.** Conserva todas las secciones de la plantilla de abajo. Usa `Pendiente de indicar` donde falten datos.
7. **Entrega primero la entrada en la conversación.** Si Moni quiere guardarla en Google Docs, sigue la sección de integración; no guardes externamente sin autorización específica.
8. **Verifica antes de finalizar.** Comprueba cada criterio de éxito. Informa con claridad si se completó la entrada, si se guardó y verificó, o si quedó como Markdown en la conversación.

## Plantilla del diario

```markdown
# Diario de aprendizaje — [tema o título descriptivo]

- **Fecha:** [fecha proporcionada o Pendiente de indicar]
- **Tema:** [tema aportado]

## Resumen
[Resumen breve basado solo en las notas de Moni.]

## Conceptos aprendidos
- [Concepto aportado y, si Moni lo explicó, su descripción fiel.]

## Ejemplos
- [Ejemplo proporcionado por Moni; no crear ejemplos nuevos.]

## Dificultades
- [Dificultad expresada por Moni.]

## Dudas
- [Duda expresada por Moni.]

## Próximos pasos
- [Acción concreta derivada de una dificultad o duda.]
- **Propuesta de Pingu (si procede):** [Idea opcional, claramente separada de los apuntes.]
```

Cuando no haya entradas para una sección, deja su encabezado y escribe `Pendiente de indicar` o `No se han aportado datos`. El título debe ser descriptivo, pero no añadir un tema que Moni no haya indicado; si no hay tema, pide aclaración o usa `Tema pendiente`.

## Google Docs mediante Zapier MCP

Google Docs/Zapier MCP constan en `TOOLS.md` como verificados para lecturas anteriores; la escritura no está verificada, y ese archivo indica que los métodos MCP no aparecen entre las herramientas actualmente expuestas. Por tanto:

1. Antes de cualquier intento de escritura, comprueba que en la sesión actual existe una herramienta real de Zapier MCP para crear documentos y que la conexión permite esa acción. No inventes nombres de herramientas, no llames herramientas no expuestas y no configures APIs, OAuth, conexiones ni servicios nuevos.
2. Presenta en la conversación el título y el contenido final propuestos y solicita confirmación explícita para crear el documento. Resuelve el destino o carpeta si falta; nunca inventes uno.
3. Solo después de confirmación y si la herramienta está realmente disponible, crea el documento con nombre claro y descriptivo. No compartas información personal irrelevante ni secretos.
4. Tras la creación, usa una lectura disponible para verificar el título y el contenido esperado. Asegúrate de comunicar el resultado real; una respuesta de error o un intento no demuestra que se haya guardado.
5. Si la herramienta de escritura no está disponible, la conexión falla, los permisos no bastan o no se obtiene confirmación, no intentes una vía alternativa externa. Entrega la entrada en Markdown en la conversación, lista para copiar, y explica brevemente por qué no se guardó.

## Criterios verificables de éxito

Antes de concluir, confirma que:

- La entrada incluye fecha, tema, resumen, conceptos, ejemplos, dificultades, dudas y próximos pasos.
- El contenido refleja las notas aportadas y no inventa conceptos, experiencias ni ejemplos.
- Las secciones sin datos quedan identificadas explícitamente.
- Cualquier pregunta o recomendación nueva está marcada como pendiente o **Propuesta de Pingu**, separada de los apuntes de Moni.
- Los próximos pasos son concretos y se relacionan con las dificultades o dudas, o están marcados como propuestas.
- La entrada se entrega en la conversación; si se pidió Google Docs, solo se declara guardada tras autorización, creación exitosa y lectura de verificación.

## Manejo de errores

- Si no se entiende el tema o faltan datos que impiden una entrada útil, pregunta de forma concreta y conserva lo ya aportado.
- Si no puedes verificar una capacidad, dilo; no afirmes que Google Docs o Zapier MCP funcionan para escritura basándote solo en lecturas anteriores.
- Si una llamada falla, describe el error real y distingue fallo, falta de conexión, falta de permisos o herramienta no disponible. No ocultes el fallo ni afirmes que el documento existe.
- Ante una interrupción o resultado incierto, conserva la entrada en la conversación y solicita repetir solo la acción que no pudo verificarse.
