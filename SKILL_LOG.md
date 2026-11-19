# Registro de diseño, conversaciones y pruebas — integración académica 4Geeks

Este registro recoge las solicitudes y pruebas verificables del proyecto. No contiene el token, respuestas personales de la API ni datos privados innecesarios.

## Requisitos iniciales del proyecto

Moni pidió construir estas capacidades, una por una:

1. Verificar si el token 4Geeks es válido y si funciona la autenticación.
2. Consultar los proyectos asignados y sus estados.
3. Identificar el trabajo que falta completar.
4. Resumir el progreso del curso.

Para cada capacidad solicitó documentar la petición en lenguaje natural, la skill resultante y una prueba de funcionamiento. Moni indicó que quiere diseñar, implementar y probar cada skill mediante conversación y que no se avance a la siguiente hasta validar la actual.

## Preparación compartida de acceso API

### Solicitud registrada

Moni pidió verificar de forma segura que el token de estudiante está disponible en el entorno autorizado, preparar acceso HTTP reutilizable y probar `GET /v1/admissions/user/me` con la cabecera de autenticación, sin exponer ni copiar el secreto. Solicitó no crear las cuatro skills todavía.

### Preparación y resultado

- **Documentación de API:** `docs/STUDENT_API_CALLS_REFERENCE.es.md` documenta el endpoint autenticado `GET /v1/admissions/user/me`, token en cabecera `Authorization: Token ***` y el host habitual `https://breathecode.herokuapp.com`.
- **Variable:** `TOKEN_4GEEKS`. Se confirmó que la variable estaba presente en el proceso de la prueba. El valor nunca se imprimió ni se registró.
- **Almacenamiento seguro:** la credencial permaneció en el mecanismo de configuración local y no se copió a archivos del proyecto. No se modificó la configuración de OpenClaw.
- **Cliente preparado:** `scripts/fourgeeks_api.py`. Realiza peticiones de solo lectura a los endpoints documentados y toma el token del entorno. No contiene secretos.
- **Limitación de ejecución:** la prueba fue desde el proceso Gateway-host. Las ejecuciones en sandbox no heredan automáticamente el entorno del host; si se habilita sandbox para estas consultas, hará falta acordar una vía segura de entrega del secreto.

### Prueba inicial

- **Petición natural:** «Comprueba que el token está disponible para el proceso que ejecuta las skills y realiza una prueba de autenticación con GET /v1/admissions/user/me».
- **Resultado real:** HTTP 200; el token fue aceptado para esa petición.
- **Privacidad:** se descartó el cuerpo de respuesta, sin mostrar perfil ni token.

## Skill 1 — Autenticar

### Solicitud original en lenguaje natural

«Pingu, vamos a implementar la primera skill de nuestro proyecto de integración con 4Geeks.

Skill 1 — Autenticar

Quiero poder preguntarte en lenguaje natural si mi acceso a 4Geeks funciona correctamente y que compruebes si mi token de estudiante es válido.

Por ejemplo:
- “Pingu, ¿sigue funcionando mi conexión con 4Geeks?”
- “Comprueba mi autenticación con 4Geeks”.

Implementa una skill específica de autenticación siguiendo las convenciones oficiales de OpenClaw, reutiliza `scripts/fourgeeks_api.py`, usa `TOKEN_4GEEKS` sin mostrar ni almacenar su valor y comprueba `GET /v1/admissions/user/me`. Gestiona token válido, ausente, rechazado y errores de conexión. Limítala solo a autenticación; prueba la activación mediante conversación normal; no expongas datos sensibles. Actualiza este registro con solicitud, nombre/ubicación/descripción, endpoint, pruebas y limitaciones. Implementa únicamente la Skill 1.»

### Artefacto

- **Nombre:** `4geeks-authentication`
- **Ubicación:** `skills/4geeks-authentication/SKILL.md`
- **Descripción:** «Comprueba si la autenticación de Moni con 4Geeks funciona; verifica el token mediante el endpoint de perfil actual, sin mostrar datos personales.»
- **Endpoint:** `GET https://breathecode.herokuapp.com/v1/admissions/user/me`
- **Cliente compartido:** `scripts/fourgeeks_api.py`, invocado con `verify-auth`; no se duplicó la petición HTTP en el documento de skill.
- **Alcance:** exclusivamente autenticación. No consulta proyectos, tareas, cohortes, actividad ni progreso.

### Pruebas y resultados reales

1. **Validación oficial de estructura:** `python3 /usr/lib/node_modules/openclaw/skills/skill-creator/scripts/quick_validate.py skills/4geeks-authentication` → `Skill is valid!`.
2. **Sintaxis del cliente:** `python3 -m py_compile scripts/fourgeeks_api.py` → sin errores.
3. **Consulta autenticada real por el modo de verificación:** `python3 scripts/fourgeeks_api.py verify-auth` → código 0, `AUTH_STATUS=VALID HTTP_STATUS=200`. El modo no leyó ni imprimió el cuerpo de perfil.
4. **Token ausente:** se ejecutó el modo con `TOKEN_4GEEKS` retirado únicamente del entorno de prueba → código 2, `AUTH_STATUS=TOKEN_MISSING`.
5. **Rechazo y error de red:** pruebas aisladas con respuestas HTTP 401 y error de conexión simulados, sin llamadas externas ni token real → clasificó `TOKEN_REJECTED` (código 12) y error de conexión (código 11), respectivamente. El cuerpo 401 simulado no se imprimió.
6. **Visibilidad en OpenClaw:** `openclaw skills check --agent main` indicó que la skill está elegible, visible para el modelo y disponible como comando; `openclaw skills info 4geeks-authentication --agent main` confirmó `Ready`, `Visible to model: yes` y `Available as command: yes`.
7. **Activación conversacional real:** en una conversación aislada nueva se envió «Pingu, ¿sigue funcionando mi conexión con 4Geeks?». La skill se activó y ejecutó una comprobación única; la API aceptó el token (HTTP 200). El cuerpo de perfil y el token no se revelaron.
8. **Búsqueda/lectura auxiliar:** `skills_search` no devolvió esta skill y `skills_read` no pudo cargarla por nombre; estas herramientas no confirmaban la disponibilidad en conversación. La comprobación del Gateway y la prueba conversacional sí la confirmaron.

### Limitaciones conocidas

- La guía de API describe aceptación del token en `/v1/admissions/user/me`, no un endpoint independiente de sesión web activa. La skill solo confirma que la API acepta la autenticación en el momento de la prueba.
- Una respuesta de red no disponible no permite concluir si el token es válido.
- Las pruebas de 401 y red fueron simuladas; no se sustituyó el token real ni se hizo una petición externa con credenciales inválidas.
- La búsqueda auxiliar `skills_search` y la lectura `skills_read` por nombre no encontraron/cargaron esta skill en esta sesión, aunque el Gateway la marcó elegible y visible, y una conversación aislada nueva la activó correctamente. Para comprobar disponibilidad se priorizó el estado de skills del Gateway y la prueba conversacional observada.

## Skill 2 — Obtener mis proyectos

### Solicitud original en lenguaje natural

«Pingu, vamos a crear la Skill 2 — Obtener mis proyectos. Quiero poder preguntarte qué proyectos tengo asignados en 4Geeks y conocer su estado (pendiente, entregado, aprobado o rechazado).

- Consulta `GET /v1/assignment/user/me/task`, filtrando por `task_type=PROJECT` y gestionando la paginación.
- Reutiliza `scripts/fourgeeks_api.py` y la variable `TOKEN_4GEEKS`.
- Crea una skill independiente siguiendo las convenciones de OpenClaw.
- Comprueba que funciona mediante una conversación natural y que devuelve datos reales de la API.
- Actualiza `SKILL_LOG.md` con mi solicitud, descripción, endpoints y resultados de las pruebas, conservando lo anterior.

Implementa únicamente la Skill 2. Cuando termines, resume los resultados y los archivos modificados.»

### Artefacto y comportamiento

- **Nombre:** `4geeks-projects`
- **Ubicación:** `skills/4geeks-projects/SKILL.md`
- **Descripción:** «Consulta los proyectos asignados de Moni en 4Geeks y resume sus estados actuales, usando el cliente compartido y paginación completa.»
- **Endpoint:** `GET https://breathecode.herokuapp.com/v1/assignment/user/me/task?task_type=PROJECT&limit=<n>&offset=<n>`; consulta autenticada con `Authorization: Token <token>` desde `TOKEN_4GEEKS`.
- **Cliente:** recurso `projects` añadido a `scripts/fourgeeks_api.py`. Impone el filtro PROJECT, recorre páginas `limit`/`offset`, protege contra respuesta demasiado grande y más de 50 páginas, y reduce la salida a título/estado; no imprime el resto de los campos personales.
- **Estados presentados:** `PENDING` → Pendiente; `DONE` → Entregado; `APPROVED` → Aprobado; `REJECTED` → Rechazado. Mantiene explícito cualquier valor imprevisto.
- **Alcance:** solo proyectos asignados devueltos por ese endpoint. No accede a detalle, entregas, proyectos del catálogo, cohortes, actividad o progreso.

### Pruebas y resultados

1. **Validación de la skill:** `python3 /usr/lib/node_modules/openclaw/skills/skill-creator/scripts/quick_validate.py skills/4geeks-projects` → `Skill is valid!`.
2. **Sintaxis y parámetros:** `python3 -m py_compile scripts/fourgeeks_api.py` y aserciones de URL confirmaron endpoint, filtro `task_type=PROJECT`, `limit` y `offset` → correctos.
3. **Consulta real inicial:** `python3 scripts/fourgeeks_api.py projects` recibió proyectos reales desde la API; la respuesta se limitó a título/estado y no mostró el token ni campos adicionales.
4. **Paginación real:** ejecución con tamaño de página reducido recorrió varias páginas y devolvió resultados; no se conservan en este registro títulos ni estados personales.
5. **Última página real:** `--limit 1 --offset 38` devolvió 1 registro y reportó 1 página, verificando el desplazamiento hasta el final.
6. **Descubrimiento OpenClaw:** `openclaw skills check --agent main` incluyó `4geeks-projects` como eligible, visible al modelo y disponible como comando; `openclaw skills info 4geeks-projects --agent main` devolvió `Ready`, `Visible to model: yes`, `Available as command: yes`.
7. **Activación por conversación natural:** en una conversación aislada nueva se preguntó qué proyectos personales hay asignados y su estado. La skill `4geeks-projects` se activó y devolvió datos reales; los títulos y estados obtenidos se omiten de este registro por privacidad. La paginación multi-página se verificó separadamente con un tamaño de página reducido.

### Notas y límites

- Los datos y estados son una instantánea de la API en la fecha de la petición; pueden cambiar.
- El conteo es de los elementos de tipo PROJECT retornados por este endpoint, no un cálculo independiente de proyectos únicos por nombre.
- Los estados `APPROVED` y `REJECTED` están mapeados según la referencia; el registro no conserva la distribución real de estados de la cuenta.

## Skill 3 — Obtener trabajo pendiente

### Solicitud original en lenguaje natural

«Implementa únicamente la Skill 3 para consultar las tareas, ejercicios y proyectos que tengo pendientes, rechazados o entregados a la espera de revisión en 4Geeks. Consulta los endpoints documentados, reutiliza `scripts/fourgeeks_api.py` y `TOKEN_4GEEKS`, crea una skill independiente según OpenClaw, distingue `PENDING`, `REJECTED` y `DONE`, prueba la activación mediante conversación natural y datos reales, y actualiza este registro conservando lo anterior. Al terminar, resume pruebas y archivos modificados.»

### Artefacto y comportamiento

- **Nombre:** `4geeks-pending-work`
- **Ubicación:** `skills/4geeks-pending-work/SKILL.md`
- **Descripción:** «Consulta el trabajo asignado de Moni en 4Geeks y distingue tareas pendientes, rechazadas que requieren correcciones y entregadas a la espera de revisión.»
- **Endpoint:** `GET https://breathecode.herokuapp.com/v1/assignment/user/me/task`, con paginación mediante `limit` y `offset`.
- **Cliente:** recurso `pending-work` añadido a `scripts/fourgeeks_api.py`. Obtiene todas las páginas, con límite de seguridad de 50 páginas y 5 MiB por respuesta, y reduce la salida a título, tipo y estados solicitados. Usa `TOKEN_4GEEKS` desde el entorno sin exponerlo.
- **Estados:** `PENDING` → pendiente de completar; `REJECTED` → requiere correcciones y nueva entrega; `DONE` → entregada y a la espera de revisión (no equivale a aprobada).
- **Alcance:** solo consulta y resume tareas asignadas; no obtiene detalles ni cambia o entrega tareas.

### Pruebas y resultados

1. **Validación OpenClaw de la skill:** `python3 /usr/lib/node_modules/openclaw/skills/skill-creator/scripts/quick_validate.py skills/4geeks-pending-work` → `Skill is valid!`.
2. **Sintaxis del cliente y construcción de URL:** `python3 -m py_compile scripts/fourgeeks_api.py` y aserción con `limit=37&offset=74` → correctos; la URL usa el endpoint documentado y no aplica filtros de estado/tipo que pudieran omitir trabajo.
3. **Consulta real con paginación predeterminada:** `python3 scripts/fourgeeks_api.py pending-work` recorrió la lista de asignaciones en más de una página y produjo un resumen limitado a los estados/tipos previstos. Los valores personales no se conservan en este registro.
4. **Paginación forzada:** ejecutar con un tamaño de página reducido recorrió varias páginas y devolvió el resumen esperado; no se guardaron los conteos por privacidad.
5. **Minimización:** las pruebas de resultados imprimieron solo los campos previstos; no se revelaron token, identificadores ni respuestas de perfil. La salida contiene títulos de tareas asignadas.
6. **Prueba de activación mediante conversación natural:** en una sesión aislada se pidió resumir trabajo pendiente y entregado. La petición activó `4geeks-pending-work`, consultó datos reales y recorrió varias páginas sin errores. Se aclaró que son asignaciones y que los títulos pueden repetirse. Los estados y conteos de la cuenta no se conservan en este registro.

### Limitaciones

- Los resultados son una instantánea real de la API y pueden cambiar.
- La traducción de `REJECTED` está implementada, pero no se conserva aquí si ese estado apareció en la muestra real.
- El cliente muestra solo los estados solicitados (`PENDING`, `REJECTED`, `DONE`); no permite inferir otros estados.
- El conteo corresponde a asignaciones devueltas, no a títulos únicos.

## Skill 4 — Obtener resumen de progreso

### Solicitud original en lenguaje natural

«Pingu, vamos a crear la Skill 4 — Obtener resumen de progreso. Quiero poder preguntar cuánto he avanzado en mi curso de 4Geeks y recibir un resumen claro de mi progreso académico.

- Consulta los endpoints necesarios de `docs/STUDENT_API_CALLS_REFERENCE.es.md`.
- Reutiliza `scripts/fourgeeks_api.py` y `TOKEN_4GEEKS`.
- Muestra total de actividades, pendientes, entregadas, aprobadas o rechazadas.
- Calcula porcentajes explicando el cálculo y distinguiendo entregas de aprobaciones.
- Gestiona la paginación y evita duplicados.
- Crea una skill independiente, pruébala con conversación natural y datos reales y actualiza `SKILL_LOG.md` conservando el historial.

Implementa únicamente la Skill 4 y resume las pruebas y archivos modificados.»

### Artefacto y comportamiento

- **Nombre:** `4geeks-progress-summary`
- **Ubicación:** `skills/4geeks-progress-summary/SKILL.md`
- **Descripción:** «Resume el progreso académico de Moni en 4Geeks con totales, estados y porcentajes, diferenciando entregas de aprobaciones.»
- **Endpoint documentado:** `GET https://breathecode.herokuapp.com/v1/assignment/user/me/task`, con `task_status`, `limit` y `offset` disponibles; se obtienen todas las actividades sin filtrar por estado para no omitir categorías.
- **Cliente:** nuevo recurso agregado a `scripts/fourgeeks_api.py`; pagina hasta completar la lista (máximo 50 páginas, respuesta máxima 5 MiB por llamada), minimiza la salida a conteos y porcentajes, y deduplica por ID de asignación. Si falta ID o un mismo ID aparece con estados incompatibles, falla de forma segura. Utiliza `TOKEN_4GEEKS` desde el entorno sin exponerlo.
- **Porcentajes:** estado = `conteo del estado / total de IDs únicos × 100`, a una cifra decimal. También presenta `DONE + APPROVED` como suma de completadas/entregadas o aprobadas, explicando que `DONE` por sí sola no implica aprobación.
- **Alcance:** resumen agregado de estados de asignaciones; no consulta otros endpoints ni modifica tareas.

### Pruebas y resultados

1. **Skill y sintaxis:** `python3 /usr/lib/node_modules/openclaw/skills/skill-creator/scripts/quick_validate.py skills/4geeks-progress-summary` → `Skill is valid!`; `python3 -m py_compile scripts/fourgeeks_api.py` → correcto.
2. **Prueba unitaria del resumen:** fixture local verificó las cuatro categorías, estado desconocido, porcentaje, total vacío, duplicado idéntico y errores seguros por ID ausente/estado conflictivo → correcto.
3. **Consulta real:** `python3 scripts/fourgeeks_api.py progress-summary` recorrió los resultados reales y generó conteos/porcentajes agregados sin exponer títulos ni identificadores. Los valores específicos de la cuenta no se conservan en este registro.
4. **Paginación forzada:** el tamaño de página reducido devolvió un resumen consistente en varias páginas; la revisión de identificadores confirmó deduplicación y ausencia de conflictos. No se guardan totales personales.
5. **Límite de offset:** se verificó que el recurso no permite empezar a mitad de la lista, pues el resumen debe cubrir el total; `--offset 1` se rechazó con mensaje de uso.
6. **Prueba de activación conversacional con datos reales:** en sesión nueva se pidió un resumen de actividades y porcentajes. Se activó `4geeks-progress-summary` y devolvió el resumen agregado de asignaciones únicas, con la distinción entre entregadas y aprobadas, la fórmula de porcentaje y la advertencia de que es una instantánea mutable. Se omiten los valores de cuenta de este registro.

### Limitaciones

- El endpoint representa asignaciones académicas disponibles para la cuenta, no una medida independiente de duración, asistencia o porcentaje oficial del curso. El porcentaje de entregas o aprobaciones se define explícitamente sobre esas asignaciones únicas.
- Los cuatro estados se incluyen en el cálculo; no se conservan en este registro los valores observados para cada categoría.
- Los estados son una instantánea mutable de la API. Si hay cero asignaciones, no existe porcentaje calculable.

## Estado del proyecto

Implementadas las Skills 1, 2, 3, 4, 5 y 6.

## Skill 5 — Consultar contenido de módulos

### Solicitud original

«Pingu, vamos a implementar la Skill 5 — Consultar contenido de módulos. Quiero poder preguntarte qué se aprende en un módulo de 4Geeks, qué lecciones incluye y qué actividades están relacionadas.

- Consulta los endpoints de syllabus y recursos (`LESSON` y `EXERCISE`) documentados en `docs/STUDENT_API_CALLS_REFERENCE.es.md`.
- Primero comprueba con datos reales qué información está disponible.
- Crea una skill independiente que permita buscar y resumir contenidos, sin inventar relaciones entre módulos y lecciones.
- Reutiliza `scripts/fourgeeks_api.py` y `TOKEN_4GEEKS` cuando sea necesario.
- Prueba la skill mediante conversación natural con un módulo real, por ejemplo, «Capacitar al agente».
- Actualiza `SKILL_LOG.md` con la solicitud, endpoints, pruebas y limitaciones, conservando lo anterior.

Si la API no permite relacionar los contenidos con módulos, adapta la skill a consultar lecciones y recursos disponibles, dejando clara esa limitación. Implementa únicamente la Skill 5.»

### Datos reales comprobados antes de implementar

- `GET /v1/admissions/public/syllabus` devolvió 128 syllabi públicos. El esquema observado solo contiene `name`, `slug`, duraciones y logo; no lista módulos ni lecciones. Ningún nombre/slug coincidió con «Capacitar al agente» ni con los términos agentes/agent.
- `GET /v1/registry/asset?asset_type=LESSON&like=Capacitar&limit=10` devolvió 0 resultados; la búsqueda de `EXERCISE` con ese término también devolvió 0.
- Búsqueda `LESSON` con `like=agent` devolvió 6 recursos en catálogo (inglés y español), con título, slug, descripción, categoría y tecnologías. La consulta equivalente `EXERCISE` devolvió 0. La paginación del catálogo usa respuesta `{count, first, last, next, previous, results}`; `limit=3` recorrió tres páginas para los seis resultados.
- El detalle `GET /v1/registry/asset/creating-your-own-chatbot` devolvió la descripción y readme URL de una lección, categoría «Soft Skills for Developers» y `assets_related` vacío. El detalle incluye campos de categoría y recursos relacionados, pero no observamos relación con módulo/syllabus. La categoría no se trata como módulo.

### Artefactos y comportamiento

- **Skill:** `4geeks-module-content`, en `skills/4geeks-module-content/SKILL.md`.
- **Cliente compartido:** `scripts/fourgeeks_api.py` amplió el cliente read-only con `content-search` (LESSON/EXERCISE, término `like`, paginación y resumen minimizado) y `content-detail` (slug, campos educativos y relaciones explícitas). Lee `TOKEN_4GEEKS` del entorno; no imprime credenciales ni metadatos de propietario.
- **Endpoints:** syllabus público `GET /v1/admissions/public/syllabus`; catálogo `GET /v1/registry/asset` filtrado por `asset_type` y `like`; detalle `GET /v1/registry/asset/{asset_slug}`.
- **Adaptación y límites:** la skill busca y resume assets del catálogo, no promete contenido completo o secuencia de módulo. No asocia recursos por semejanza de título, tema o categoría; solo reportará relaciones cuando `assets_related` las confirme explícitamente. Cero coincidencias significa que la búsqueda no encontró resultados, no que el módulo no exista.

### Pruebas y resultados

1. `python3 /usr/lib/node_modules/openclaw/skills/skill-creator/scripts/quick_validate.py skills/4geeks-module-content` → `Skill is valid!`.
2. `python3 -m py_compile scripts/fourgeeks_api.py` → correcto. Pruebas de URL construyeron las rutas documentadas de búsqueda y detalle.
3. Cliente real `content-search --asset-type LESSON --query agent --limit 3` paginó los seis resultados en 3 páginas; `EXERCISE --query agent` devolvió 0; búsqueda de ambas categorías con «Capacitar al agente» devolvió 0. Salida limitada a datos de contenido necesarios.
4. Cliente real `content-detail --asset-slug creating-your-own-chatbot` devolvió el detalle esperado, sin relaciones declaradas; no se expusieron datos de propietario.
5. **Activación conversacional natural con «Capacitar al agente»:** prueba aislada completada. La consulta activó `4geeks-module-content`; se consultaron `/v1/registry/asset` para `LESSON` y `EXERCISE` con búsquedas en español e inglés, y `/v1/admissions/public/syllabus`. Búsquedas exactas y por «capacitar» dieron 0 coincidencias; «agente» y «training» encontraron lecciones en el catálogo, pero ninguna relación explícita con ese módulo. El syllabus no mostró nombre coincidente. La respuesta aclaró que no puede confirmar el contenido ni las lecciones/ejercicios del módulo, no atribuyó los recursos encontrados y pidió enlace o nombre exacto del curso para afinar la búsqueda. No se modificaron archivos durante la prueba conversacional.

### Limitaciones

- El endpoint de syllabus solo aporta nombres/slugs y metadatos de duración/logotipo; no hay un endpoint documentado ni relación observada para enumerar contenido de un módulo.
- El buscador de assets usa texto `like`, cuya cobertura/ranking no está garantizada; búsqueda sin resultados no prueba ausencia de contenido.
- Algunas descripciones están vacías y el README puede ser solo una URL externa; el cliente no descarga ese README, solo resume campos entregados por la API.
- Los datos observados son una instantánea del catálogo.

## Skill 6 — Consultar requisitos de proyectos

### Solicitud original

«Implementa únicamente la Skill 6 — Consultar requisitos de proyectos. Quiero buscar un proyecto de 4Geeks por nombre, resumir su descripción/README/requisitos/criterios disponibles, distinguir los datos del catálogo de mi asignación personal, probarla mediante conversación natural con datos reales y documentar la solicitud, endpoints, pruebas y limitaciones en este registro conservando el historial. No inventes criterios ausentes; reutiliza `scripts/fourgeeks_api.py` y `TOKEN_4GEEKS`; las consultas deben ser read-only.»

### Datos reales observados

- Búsqueda en `GET /v1/registry/asset?asset_type=PROJECT&like=Telemetry+Plan` devolvió 0. Esto demuestra una limitación del buscador por texto; no demuestra que el proyecto no exista.
- La consulta directa del asset mediante `GET /v1/registry/asset/{asset_slug}` devolvió descripción, enlace README y campos de ficha; `assessment` era nulo e instrucciones de entrega vacías, por lo que no se afirmaron criterios ausentes.
- La lista personal `GET /v1/assignment/user/me/task?task_type=PROJECT&limit=100&offset=0` permitió encontrar y vincular una asignación con el asset mediante título/slug. Se omiten título, slug y estado personal de este registro.
- El detalle mediante `GET /v1/assignment/task/{task_id}` devolvió campos personales de estado/feedback/revisión. No se conserva ningún identificador ni valor personal en este registro.

### Artefactos y comportamiento

- **Skill:** `4geeks-project-requirements`, en `skills/4geeks-project-requirements/SKILL.md`.
- **Cliente compartido:** nuevos recursos `project-search`, `project-detail`, `project-assignment` y `project-assignment-detail`; todas las llamadas siguen siendo GET. El buscador pagina y reduce salida; detalle de catálogo y detalle personal generan vistas filtradas distintas.
- **Endpoints:** `GET /v1/registry/asset`; `GET /v1/registry/asset/{asset_slug}`; `GET /v1/assignment/user/me/task`; `GET /v1/assignment/task/{task_id}`.
- **Política de respuesta:** separar catálogo de asignación personal, confirmar la coincidencia con título/slug, no inferir requisitos a partir del estado personal, no revelar identificadores internos y señalar campos ausentes/vacíos. No entregar ni modificar tareas.

### Pruebas y resultados

1. `python3 -m py_compile scripts/fourgeeks_api.py` → correcto en la validación final.
2. Construcción de URLs verificada para búsqueda de catálogo, detalle de catálogo y detalle de asignación. IDs de asignación no numéricos y slugs inválidos se rechazan antes de hacer una llamada.
3. La búsqueda textual del catálogo no encontró coincidencias; la consulta posterior del asset por slug asociado y la búsqueda de asignación permitieron completar el flujo. El detalle de asignación también se consultó correctamente. No se guardan los datos personales obtenidos.
4. Validador de skill: `python3 /usr/lib/node_modules/openclaw/skills/skill-creator/scripts/quick_validate.py skills/4geeks-project-requirements` → `Skill is valid!`.
5. **Prueba conversacional natural aislada:** se preguntó por requisitos, criterios y asignación de un proyecto real. La respuesta activó el flujo, resumió únicamente la descripción disponible, indicó que la evaluación y las instrucciones de entrega no estaban informadas y separó catálogo de asignación. No reveló IDs personales ni afirmó haber leído el README. Las búsquedas textuales no encontraron el asset; la asociación observada en la lista de asignaciones permitió consultar la ficha por slug. No hubo errores.
6. Errores de entrada: `project-assignment-detail` con ID no numérico y `project-detail` con slug inválido fueron rechazados antes de hacer petición. La construcción de URL se verificó para los tres flujos.
7. `python3 -m py_compile scripts/fourgeeks_api.py`, `quick_validate.py skills/4geeks-project-requirements` y `git diff --check` → correctos. Revisión final de archivos acotada a Skill 6.

### Limitaciones

- El buscador del catálogo puede no devolver un asset aunque exista; si hay 0 resultados, probar otros términos o una asociación por slug observada en la lista personal, y describirlo solo como resultado de búsqueda.
- README solo se enlaza; no se descarga ni resume su contenido salvo que se solicite expresamente.
- Evaluación e instrucciones de entrega no siempre están informadas. Para este proyecto se observaron `assessment: null` e instrucciones vacías, así que no se listan criterios adicionales.
- Los resultados son una instantánea mutable de catálogo y asignaciones.
