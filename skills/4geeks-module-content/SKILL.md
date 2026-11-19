---
name: 4geeks-module-content
description: Cuando Moni pregunte qué se aprende en un módulo de 4Geeks o qué lecciones/ejercicios hay, busca assets del catálogo y resume solo relaciones confirmadas.
---

# Consultar contenido educativo de 4Geeks

1. Busca en el catálogo con el cliente compartido y el texto del módulo o tema. Ejecuta `python3 /root/.openclaw/workspace/scripts/fourgeeks_api.py content-search --asset-type LESSON --query "<consulta>"`; si Moni pregunta también por actividades, repite para `EXERCISE`. El cliente autentica con `TOKEN_4GEEKS` del entorno y pagina resultados.
2. Resume los assets encontrados usando título, tipo, descripción, categoría y tecnologías devueltos por el cliente. No añadas conceptos ni objetivos que no consten. Si hace falta más detalle de un resultado, utiliza su slug: `python3 /root/.openclaw/workspace/scripts/fourgeeks_api.py content-detail --asset-slug "<slug>"`.
3. Si la consulta nombra un módulo, consulta `GET /v1/admissions/public/syllabus` solo cuando aporte contexto sobre si existe un syllabus con nombre parecido. El endpoint devuelve syllabi con nombre y slug, pero no demuestra que ese syllabus sea el módulo pedido ni relaciona sus lecciones con él. No afirmes pertenencia sin relación explícita de la API.
4. Trata búsqueda como descubrimiento, no como comprobación exhaustiva de módulo. Si no hay resultados, di que la búsqueda textual en el catálogo no encontró coincidencias; no concluyas que el módulo no existe o carece de contenido. Si ayuda, prueba una consulta breve alternativa en español o inglés.
5. Presenta categorías como etiquetas del catálogo, no como módulos. Informa de `assets_related` solo cuando el detalle indique esa relación explícitamente; no deduzcas relaciones por nombre, orden, categoría o semejanza temática. Separa claramente el contenido encontrado de la pertenencia al módulo no confirmada.
6. No muestres credenciales, IDs internos, datos del propietario ni metadatos ajenos al contenido. Si el cliente falla, informa del error disponible sin inferir resultados.

Limita esta skill a consultar y resumir syllabi públicos y assets LESSON/EXERCISE del catálogo. No consulta asignaciones de tareas ni inventa una secuencia curricular.
