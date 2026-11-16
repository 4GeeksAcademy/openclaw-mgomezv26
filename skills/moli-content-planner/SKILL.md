---
name: moli-content-planner
description: Ayuda a Moni a planificar tutoriales de programación o IA, gameplays y futuros directos para MØLI Studio mediante una ficha de producción. Actívala cuando quiera desarrollar una idea para uno de esos formatos.
---

# MØLI Content Planner

Convierte una idea de MØLI Studio en una ficha práctica de producción. MØLI Studio es un proyecto personal en fase inicial: no presupongas que Moni ya publica vídeos o hace directos regularmente. No inventes su equipo, juegos, audiencia, canales concretos ni integraciones disponibles.

## Cuándo activarla

Actívala cuando Moni quiera planificar un tutorial de programación o IA, un gameplay o un futuro directo/streaming para MØLI Studio. Si solo pide una explicación técnica o ayuda general que no sea planificación de contenido, responde a esa petición sin forzar esta skill.

## Inputs

Acepta texto libre o campos etiquetados. Identifica, si están disponibles:

- **Tipo de contenido:** tutorial, gameplay o directo/streaming.
- **Tema o idea:** concepto, proyecto, juego o actividad que Moni proponga.
- **Público objetivo:** a quién quiere llegar.
- **Duración aproximada:** tiempo objetivo del vídeo o directo.
- **Objetivos:** qué quiere lograr con la pieza.

Utiliza las preferencias existentes de `USER.md` cuando sean relevantes: tutoriales de programación e IA para YouTube; gameplays y streaming para Twitch; OBS Studio como herramienta que utiliza; Discord como comunidad que quiere usar. Estos son planes o preferencias, no prueba de publicaciones, actividad regular, configuración o integración técnica.

Pregunta únicamente por datos imprescindibles para que el plan sea útil. Si algún dato opcional falta, indícalo como pendiente o plantea una opción claramente etiquetada como propuesta. No deduzcas ni inventes equipo, especificaciones técnicas, juegos concretos, tamaño o perfil de audiencia, canal confirmado, calendario de publicación ni disponibilidad de herramientas.

## Procedimiento de planificación

1. **Clasifica el formato.** Determina si es un tutorial, gameplay o directo. Si no está claro y cambia sustancialmente el resultado, pregunta; si no, ofrece una propuesta provisional explícita.
2. **Recoge los datos necesarios.** Usa el tema y el objetivo indicados. Reutiliza duración o público conocidos de la conversación si están claros; no conviertas preferencias generales en detalles específicos. Pregunta solo si la ausencia de un dato bloquea un plan coherente.
3. **Adapta el alcance al inicio de MØLI.** Propón una preparación sencilla y realizable desde cero, sin presentar una idea como actividad ya iniciada o publicada.
4. **Ajusta tono y estructura.** Para tutoriales, emplea un tono educativo, claro y técnicamente cuidadoso, con pasos comprensibles. Para gaming, usa un tono cercano, entretenido y espontáneo; para un directo, estructura momentos flexibles sin convertirlo en un guion rígido.
5. **Construye la ficha.** Redacta título, objetivo, público, duración, estructura, propuesta de guion, materiales, checklist de grabación y próximos pasos. Mantén los tiempos de las secciones compatibles con la duración total cuando haya una duración especificada.
6. **Distingue hechos de propuestas.** Refleja fielmente los datos aportados por Moni. Marca sugerencias de Pingu como propuestas y no como decisiones de Moni.
7. **Entrega y verifica.** Muestra la ficha en la conversación. Antes de cualquier envío a Telegram, aplica las condiciones de autorización y disponibilidad descritas abajo; luego verifica la respuesta de la herramienta antes de afirmar que se envió.

## Plantilla de producción

```markdown
# [Título]

- **Tipo de contenido:** [tutorial / gameplay / directo]
- **Plataforma prevista:** [solo si Moni la indicó o consta como preferencia; si no, Pendiente de decidir]
- **Objetivo:** [objetivo indicado]
- **Público objetivo:** [público indicado o Pendiente de definir]
- **Duración aproximada:** [duración indicada o Pendiente de definir]

## Estructura
1. [Bloque, intención y tiempo aproximado si se conoce la duración]
2. [Bloque, intención y tiempo aproximado]
3. [Cierre o siguiente momento]

## Propuesta de guion
- **Apertura:** [idea de introducción]
- **Desarrollo:** [puntos o transiciones]
- **Cierre:** [resumen, despedida o invitación opcional]

## Materiales necesarios
- [Material confirmado como necesario]
- [Propuesta opcional claramente señalada]

## Checklist de grabación
- [ ] Confirmar el tema, objetivo y formato.
- [ ] Preparar los materiales que se hayan confirmado.
- [ ] Revisar encuadre, sonido y captura en la herramienta que Moni confirme que utilizará.
- [ ] Hacer una comprobación previa de grabación o directo, sin afirmar que se controló OBS.
- [ ] Revisar el resultado antes de publicar o compartir.

## Próximos pasos
1. [Acción concreta para preparar la pieza]
2. [Decisión o comprobación pendiente]
```

Ajusta la plantilla al formato sin eliminar sus campos principales. Si no se han aportado datos, escribe `Pendiente de definir` o `Pendiente de confirmar`; no rellenes con detalles inventados. Los materiales sugeridos deben distinguirse de los confirmados. No prometas resultados de publicación, audiencia o rendimiento.

## Tono por formato

- **Tutorial de programación o IA:** educativo y claro. Divide el tema en pasos, define el resultado que se quiere enseñar y señala puntos donde conviene explicar o mostrar una demostración. No inventes hechos técnicos; si la exactitud depende de información no disponible, indícalo o pide el material de referencia.
- **Gameplay:** cercano y entretenido, con espacio para reacciones espontáneas y momentos del juego. No elijas un juego ni presupongas plataforma, equipo o estilo personal de Moni si no lo ha indicado.
- **Directo/streaming:** cercano y flexible. Propón bloques y transiciones, no un libreto que requiera seguirse palabra por palabra. No des por hecho que ya hay una audiencia, comunidad activa o frecuencia de directos.

## Entrega en conversación y Telegram

La entrega predeterminada es la ficha completa en la conversación. Telegram figura en `TOOLS.md` como verificado mediante conversaciones reales con el bot OpenClawPingu, pero eso no confirma por sí solo que haya una herramienta de envío disponible en la sesión actual ni permisos para cada destinatario.

- Solo considera Telegram si existe una herramienta de envío realmente disponible en la sesión.
- Antes de enviar, muestra la ficha final y pide autorización explícita para enviar ese contenido. Confirma el chat o destinatario si no está inequívocamente identificado; no inventes uno.
- No publiques contenido en YouTube, Twitch, Discord ni otros servicios, ni controles OBS, a menos que la capacidad esté disponible y Moni lo solicite expresamente. Esta skill planifica; no afirma que graba, transmite o publica.
- Si no hay herramienta de Telegram disponible, falta autorización o destinatario, entrega el plan aquí y explica brevemente la limitación. No intentes rutas alternativas ni configures APIs, OAuth o servicios.

## Criterios verificables de éxito

Antes de finalizar, comprueba que:

- La ficha incluye título, objetivo, público, duración, estructura, propuesta de guion, materiales necesarios, checklist y próximos pasos.
- El tipo, tema y objetivo corresponden a lo que pidió Moni; los datos no proporcionados se marcan pendientes o como propuestas.
- La estructura resulta compatible con la duración indicada o aclara si los tiempos son aproximados.
- El tutorial mantiene un tono educativo y claro; gaming/streaming, uno cercano y entretenido.
- No se inventan equipo, juegos, audiencia, canal, integraciones, actividad publicada ni frecuencia de directos.
- La ficha se entrega en la conversación; solo se declara enviada por Telegram si la herramienta está disponible, Moni autorizó el envío concreto, el destino está confirmado y la acción terminó con éxito.

## Limitaciones y manejo de errores

- Si falta información opcional, continúa dejando el campo pendiente o sugiriendo una alternativa explícitamente marcada. Si un dato imprescindible impide un plan útil, formula una pregunta concreta, no un cuestionario extenso.
- Si no se puede determinar una plataforma o material necesario, dilo y no lo des por supuesto. OBS Studio, YouTube, Twitch y Discord no implican que existan integraciones para controlarlos.
- Si la herramienta de Telegram no está disponible, no hay autorización o el envío falla, indica el estado/error real y deja la ficha en la conversación. No afirmes que se envió si solo se intentó.
- Protege la privacidad; no incluyas credenciales, tokens ni datos confidenciales en la ficha o en un mensaje externo.
