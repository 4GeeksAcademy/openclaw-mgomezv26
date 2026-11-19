---
name: 4geeks-pending-work
description: Consulta el trabajo asignado de Moni en 4Geeks y distingue tareas pendientes, rechazadas que requieren correcciones y entregadas a la espera de revisión.
---

# Consultar trabajo pendiente en 4Geeks

Cuando Moni pregunte qué trabajo le falta completar en 4Geeks, qué tareas tiene pendientes o rechazadas, o qué ha entregado y espera revisión, ejecuta el cliente compartido:

```sh
python3 /root/.openclaw/workspace/scripts/fourgeeks_api.py pending-work
```

El recurso `pending-work` consulta únicamente `GET https://breathecode.herokuapp.com/v1/assignment/user/me/task`, con `limit` y `offset` para recorrer todas las páginas. Usa `TOKEN_4GEEKS` del entorno del proceso; no leas `.env` ni incluyas el token en argumentos, salida o registros. El cliente devuelve solo título, tipo y estado de las tareas con estado `PENDING`, `REJECTED` o `DONE`.

Interpreta y presenta los estados por separado:

- `PENDING`: Pendiente de completar.
- `REJECTED`: Rechazada; requiere correcciones y una nueva entrega.
- `DONE`: Entregada por la estudiante y a la espera de revisión; no la presentes como aprobada.

Resume primero cuántas hay en cada estado. Después, lista por título y tipo las `PENDING` y `REJECTED`, pues requieren acción. Informa también del total `DONE` y, si la lista es manejable o Moni pide detalle, muestra sus títulos bajo “Entregadas, pendientes de revisión”. Evita contar como únicas tareas con títulos repetidos: el resultado es un recuento de asignaciones devueltas por la API.

Si no hay elementos en uno de los estados, dilo explícitamente. Si el resultado completo está vacío, di que la consulta no encontró tareas en esos tres estados; no infieras que no hay trabajo asignado. El cliente solo devuelve estos tres estados, por lo que no deduzcas ni informes la presencia o ausencia de otros estados. Si el comando falla, comunica el error disponible y no afirmes que no hay tareas. No muestres variables de entorno, respuestas sin filtrar, comentarios de revisión, URLs, identificadores ni otros datos personales.

Limita esta skill a consultar y resumir las tareas asignadas que devuelve este endpoint. No consultes detalles, cohortes, actividad, catálogo ni progreso; no actualices ni entregues tareas, y no empieces por cuenta propia acciones para corregirlas.
