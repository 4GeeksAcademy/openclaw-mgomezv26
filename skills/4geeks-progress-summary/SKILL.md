---
name: 4geeks-progress-summary
description: Resume el progreso académico de Moni en 4Geeks con totales, estados y porcentajes, diferenciando entregas de aprobaciones.
---

# Resumir mi progreso de 4Geeks

1. Cuando Moni pregunte cuánto ha avanzado en 4Geeks, su progreso del curso o cuántas actividades tiene pendientes, entregadas, aprobadas o rechazadas, ejecuta `python3 /root/.openclaw/workspace/scripts/fourgeeks_api.py progress-summary`. Confirma que la salida sea JSON con un total, conteos y porcentajes, o comunica el error sin sustituirlo por una estimación.
2. Usa solo el resumen agregado de `GET https://breathecode.herokuapp.com/v1/assignment/user/me/task`; el cliente recorre `limit`/`offset` y carga `TOKEN_4GEEKS` del entorno. No leas `.env` ni consultes otros endpoints, y no muestres credenciales, registros personales, títulos, comentarios, URLs o IDs.
3. Presenta el total de actividades únicas y los conteos de `PENDING`, `DONE`, `APPROVED`, `REJECTED`; incluye `UNKNOWN` solo si no es cero. El cliente deduplica por ID de asignación, no por título, porque puede haber títulos iguales para asignaciones distintas. Si falta un ID o hay estados incompatibles para el mismo ID, comunica que no se pudo calcular un resumen fiable.
4. Traduce los estados con precisión: `PENDING` pendiente de completar; `DONE` completada/entregada por la estudiante y todavía no aprobada; `APPROVED` aprobada en revisión; `REJECTED` rechazada y requiere correcciones; `UNKNOWN` estado ausente o no reconocido, sin reclasificarlo.
5. Explica que cada porcentaje de estado es `conteo del estado / total de actividades únicas × 100`, redondeado a una cifra decimal. Puedes informar también `DONE + APPROVED` y su porcentaje como “entregadas o aprobadas”, aclarando que ese agregado incluye entregas aún no aprobadas. No llames aprobado a `DONE` ni cuentes `REJECTED` como progreso completado.
6. Si el total es cero, di que la API no devolvió actividades y que no hay porcentaje calculable; no presentes 0 % como un avance real. Indica que el resumen es una instantánea de las asignaciones y sus estados en la API, que pueden cambiar.

Limita esta skill a resumir el progreso basado en estados de asignación. No consultes detalles, cohorte, actividad agregada, catálogo ni otros endpoints, y no modifiques ni entregues tareas.