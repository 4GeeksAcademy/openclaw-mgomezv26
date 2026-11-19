---
name: 4geeks-project-requirements
description: Cuando Moni pregunte qué debe hacer o cuáles son los requisitos/criterios de un proyecto de 4Geeks, busca el proyecto en el catálogo y distingue sus instrucciones de su asignación personal.
---

# Consultar requisitos de proyectos 4Geeks

1. Busca el nombre o una parte distintiva en el catálogo de proyectos: `python3 /root/.openclaw/workspace/scripts/fourgeeks_api.py project-search --query "<nombre>"`. La búsqueda usa `GET /v1/registry/asset?asset_type=PROJECT&like=...`, pagina resultados y muestra metadatos de contenido. Si hay varios resultados, presenta títulos y pide precisión solo si no puedes identificar inequívocamente el proyecto.
2. Para el candidato elegido, consulta `python3 /root/.openclaw/workspace/scripts/fourgeeks_api.py project-detail --asset-slug "<slug>"`. Resume solo la descripción, README URL, instrucciones y criterios/assessment que devuelva el catálogo. `assessment: null` o campo ausente significa que la API no aportó criterios por ese campo; no los inventes. No descargues README salvo que Moni pida explícitamente revisar su contenido.
3. Distingue catálogo de asignación personal. Busca aparte `python3 /root/.openclaw/workspace/scripts/fourgeeks_api.py project-assignment --query "<título exacto o término distintivo>"`. Esta consulta paginada filtra por título entre asignaciones `PROJECT` y devuelve estado, descripción propia de la asignación y slug asociado cuando estén disponibles. No des por hecho que un proyecto del catálogo está asignado, ni que una asignación coincide si los títulos/slug no lo confirman.
4. Si hay una coincidencia personal, consulta el detalle solo mediante `python3 /root/.openclaw/workspace/scripts/fourgeeks_api.py project-assignment-detail <assignment_id>`. Resume únicamente campos pertinentes que entregue la API, distingue feedback/estado personal de requisitos generales y no muestres identificadores internos. Si falta una asignación coincidente, dilo como resultado de búsqueda, sin inferir que nunca existió.
5. Separa con claridad: **Catálogo** (descripción, README y evaluación general disponibles) y **Tu asignación** (estado, instrucciones o feedback personal). Señala los datos ausentes; no conviertas descripción o título en criterios de evaluación no declarados.
6. El cliente usa `TOKEN_4GEEKS` del entorno y solo realiza GET. No leas `.env`, no muestres el token ni metadatos personales. Si falla una consulta, informa del error sin inferir ausencia de resultados.

Limita esta skill a la búsqueda de proyectos, sus detalles de catálogo y el detalle de asignaciones coincidentes. No entregues ni modifiques tareas.
