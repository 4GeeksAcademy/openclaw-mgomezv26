# TOOLS.md — Herramientas y servicios

## 1. Herramientas y estado

| Servicio | Estado | Uso posible | Limitaciones conocidas |
|---|---|---|---|
| Telegram | Verificado mediante conversaciones reales | Canal Telegram conectado y funcionando mediante el bot OpenClawPingu; se han intercambiado mensajes correctamente. | La verificación procede de conversaciones reales, no de una comprobación desde WebChat. No asumir permisos o capacidades adicionales a las comprobadas ni compartir datos confidenciales. |
| Zapier MCP | Verificado | En una comprobación anterior se accedió al servidor MCP y se verificaron conexiones mediante lecturas seguras. | No se hicieron pruebas de escritura en esta revisión. Los métodos del servidor no aparecen entre las herramientas actualmente expuestas; confirmar que están disponibles antes de usarlos. |
| Google Docs | Verificado | Lectura y consulta de documentos mediante Zapier MCP: una lectura se completó correctamente en la comprobación anterior. | La verificación confirma lectura, no creación, edición ni permisos generales de la cuenta. |
| Google Calendar | Verificado | Consulta de calendario mediante Zapier MCP: se confirmó acceso de lectura en una comprobación anterior. | La búsqueda por intervalo devolvió vacío aunque una consulta directa por ID encontró un evento; no asumir que una lista vacía confirma ausencia. No se verificó escritura. |
| Gmail | No disponible (conexión no verificada) | No se ha confirmado una herramienta o conexión autorizada. | No asumir acceso a mensajes ni capacidad para enviar correo. |
| Google Drive | No disponible (conexión no verificada) | No se ha confirmado una herramienta o conexión autorizada. | No asumir acceso a archivos, carpetas o permisos de Drive. |
| Google Tasks | No disponible (conexión no verificada) | No se ha confirmado una herramienta o conexión autorizada. | No asumir acceso a listas o tareas. |
| GitHub | No disponible | No hay credenciales de GitHub disponibles para este agente según la comprobación de estado. | No se verificó acceso a repositorios mediante una integración de GitHub. La identidad/autora local de Git no demuestra acceso a GitHub. |

Los estados «verificado» de Zapier MCP, Google Docs y Google Calendar reflejan comprobaciones de lectura anteriores; no implican que toda acción o permiso esté habilitado actualmente.

## 2. Convenciones

- Idioma habitual: español.
- Zona horaria: `Europe/Madrid`.
- No inventes calendarios, carpetas, etiquetas ni destinatarios predeterminados. Pregunta cuando falte esa información.
- Prioriza nombres claros y descriptivos para documentos y tareas.

## 3. Permisos

- Puedes consultar información cuando esté autorizado por `AGENTS.md`.
- Solicita confirmación antes de enviar correos, crear eventos, compartir documentos, publicar contenido o realizar cambios externos importantes.
- Nunca compartas credenciales ni datos confidenciales.

## 4. Manejo de errores

- Si una herramienta falla, indica el error real; distingue entre fallo, falta de conexión y falta de permisos.
- No afirmes que una integración funciona sin comprobarla con una acción segura adecuada.
- No configures nuevas APIs, conexiones OAuth ni servicios externos.
- No realices pruebas que creen, modifiquen o envíen contenido sin autorización explícita.
