---
name: 4geeks-projects
description: Consulta los proyectos asignados de Moni en 4Geeks y resume sus estados actuales, usando el cliente compartido y paginación completa.
---

# Consultar mis proyectos de 4Geeks

Cuando Moni pregunte qué proyectos tiene asignados en 4Geeks o por su estado, ejecuta el cliente compartido:

```sh
python3 /root/.openclaw/workspace/scripts/fourgeeks_api.py projects
```

El recurso `projects` llama solo a `GET https://breathecode.herokuapp.com/v1/assignment/user/me/task` con `task_type=PROJECT`, usa `TOKEN_4GEEKS` del entorno del proceso y recorre las páginas con `limit` y `offset`. No leas el archivo `.env` ni incluyas el token en argumentos, salida o registros.

Interpreta el JSON del cliente y presenta cada proyecto por título y estado, junto con el total. El cliente omite descripciones, URLs de entrega, identificadores y otros campos personales. Traduce los estados así:

- `PENDING`: Pendiente.
- `DONE`: Entregado.
- `APPROVED`: Aprobado.
- `REJECTED`: Rechazado.
- Cualquier otro valor: conserva el valor literal y aclara que la API devolvió un estado no reconocido.

Si la lista está vacía, di que la consulta no encontró proyectos asignados, sin inferir que nunca hayan existido. Si el comando falla, comunica el error disponible sin afirmar que no hay proyectos. No muestres variables de entorno ni datos adicionales de la respuesta.

Limita esta skill a listar los proyectos que devuelve este endpoint. No consultes proyectos del catálogo, tareas de otros tipos, detalles, cohortes, actividad, progreso, ni entregues o modifiques tareas.
