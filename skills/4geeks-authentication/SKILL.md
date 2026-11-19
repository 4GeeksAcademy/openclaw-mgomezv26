---
name: 4geeks-authentication
description: Comprueba si la autenticación de Moni con 4Geeks funciona; verifica el token mediante el endpoint de perfil actual, sin mostrar datos personales.
---

# Comprobar autenticación de 4Geeks

Activa esta skill cuando Moni pregunte en lenguaje natural si funciona su conexión, acceso o autenticación con 4Geeks. Limítate exclusivamente a comprobar el token con el endpoint indicado: no consultes proyectos, tareas, actividad, cohortes ni progreso.

## Procedimiento

1. Ejecuta desde el workspace el cliente existente, sin duplicar lógica ni leer el archivo `.env` directamente:

   ```sh
   python3 /root/.openclaw/workspace/scripts/fourgeeks_api.py verify-auth
   ```

   El cliente obtiene `TOKEN_4GEEKS` del entorno del proceso y envía `GET https://breathecode.herokuapp.com/v1/admissions/user/me` con `Authorization: Token <token>`. Nunca muestres ni incluyas el valor del token en argumentos, respuesta, mensajes o registros.

2. Interpreta únicamente el estado breve que imprime el cliente y su código de salida:
   - `AUTH_STATUS=VALID` / código `0`: informa que la API aceptó el token y que la consulta autenticada funcionó.
   - `AUTH_STATUS=TOKEN_MISSING` / código `2`: informa que `TOKEN_4GEEKS` no está disponible para este proceso. No solicites que pegue el token en el chat.
   - `AUTH_STATUS=TOKEN_REJECTED` / código `12`: informa que la API rechazó el token (HTTP 401/403); no digas que la sesión funciona.
   - `AUTH_STATUS=API_ERROR` / código `13`: informa el estado HTTP de error sin inferir que el token sea inválido.
   - error de conexión / código `11`: informa que no se pudo contactar con la API; el estado del token queda sin verificar.
   - Otros códigos (incluido error de respuesta no JSON o de tamaño) significan que no se completó la verificación; comunica el error genérico sin revelar salida sensible.

3. Responde en español, de forma concisa, distinguiendo claramente entre token aceptado, token ausente, token rechazado y verificación no disponible. No afirmes que hay una sesión web activa: la referencia documenta que `/v1/admissions/user/me` requiere autenticación, no un endpoint independiente de estado de sesión.

## Límites y privacidad

- Esta skill solo verifica autenticación y solo llama al recurso `verify-auth` del cliente compartido.
- No consultes ni muestres el objeto de perfil devuelto por la API; el modo `verify-auth` descarta el cuerpo de esa respuesta.
- No leas, imprimas, registres, copies ni almacenes el contenido de `~/.openclaw/.env` o `TOKEN_4GEEKS`.
- No reintentes repetidamente ante errores de red; informa del resultado observado y su limitación.
