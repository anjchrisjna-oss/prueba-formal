# Plan de profesionalización en 4 fases

## 0) Resumen ejecutivo

Este plan profesionaliza el sistema FastAPI + SQLAlchemy actual (routers UI/API, motor de alertas, módulo de producción y pruebas de integración existentes) hacia un estándar enterprise en 4 fases secuenciales:

1. **Seguridad por diseño**.
2. **Calidad de ingeniería y gobernanza técnica**.
3. **IA avanzada aplicada a operación y analítica**.
4. **Operaciones de producción con confiabilidad SRE**.

Cada fase incluye: entregables técnicos, plan de pruebas, migraciones de datos/infraestructura y criterios de aceptación medibles.

---

## 1) Línea base del sistema actual (estado de partida)

### 1.1 Arquitectura observada

- Backend monolítico en **FastAPI** con routers funcionales para stock, tareas, ambiente, salas, pallets, alertas y producción.
- Persistencia en **SQLAlchemy** (SQLite en entorno local actual).
- Renderizado HTML con plantillas Jinja para UI operativa.
- Inicialización de esquema vía `Base.metadata.create_all(...)` y datos semilla en arranque.
- Hay pruebas de integración para escenarios de producción y atomicidad transaccional.

### 1.2 Riesgos de profesionalización identificados

- **Seguridad**: ausencia de capa robusta de autenticación/autorización centralizada y hardening operativo.
- **Calidad**: cobertura de tests limitada al flujo de producción; faltan puertas de calidad CI/CD integrales.
- **Escalabilidad de datos**: acoplamiento al arranque dinámico de tablas dificulta trazabilidad de cambios de esquema.
- **Operación**: sin observabilidad completa (métricas, trazas, SLOs) ni runbooks de incidentes.
- **IA**: sin pipeline MLOps, evaluación offline/online ni gobernanza de riesgo de modelos.

---

## 2) Fase 1 — Seguridad (4 a 6 semanas)

### Objetivo

Reducir superficie de ataque, formalizar control de acceso y garantizar trazabilidad de eventos críticos.

### Entregables técnicos

1. **Identidad y acceso (IAM)**
   - Autenticación basada en OAuth2/OIDC o JWT firmado con rotación de claves.
   - Autorización por roles (RBAC): `admin`, `operaciones`, `auditor`, `solo_lectura`.
   - Matriz de permisos por endpoint API/UI y por operaciones sensibles (stock, producción, config).

2. **Seguridad de API y aplicación**
   - Validación estricta de payloads y límites de tamaño en formularios/subidas.
   - Protección de sesiones/cookies (SameSite, Secure, HttpOnly) para UI.
   - Rate limiting por IP/usuario para endpoints críticos.
   - Cabeceras de seguridad (CSP, HSTS, X-Frame-Options, Referrer-Policy).

3. **Secretos y configuración segura**
   - Externalización de secretos a gestor seguro (Vault/Secrets Manager o equivalente).
   - Separación de configuración por ambiente con políticas de mínimo privilegio.
   - Rotación documentada de claves y credenciales.

4. **Auditoría y cumplimiento base**
   - Registro de auditoría inmutable para cambios de inventario, tareas, alertas y parámetros.
   - Correlación de eventos con `request_id` y `actor_id`.

5. **Dependencias y vulnerabilidades**
   - Escaneo SCA (dependencias Python) y política de bloqueo de CVEs críticas.
   - SBOM (CycloneDX/SPDX) versionado por release.

### Pruebas de la fase

- Pruebas unitarias de autorización por rol en cada router crítico.
- Pruebas de integración de login/refresh/expiración y accesos no permitidos (403/401).
- Pruebas DAST básicas contra entorno staging.
- Pruebas de regresión de funcionalidades existentes (incluye producción/stock).
- Simulaciones de abuso: rate-limit y payload malicioso.

### Migraciones requeridas

- Migración de base de datos para:
  - tablas `users`, `roles`, `permissions`, `audit_log`;
  - columnas de trazabilidad (`created_by`, `updated_by`) en entidades críticas.
- Migración de configuración:
  - variables de entorno nuevas para IAM, claves, y límites de seguridad.

### Criterios de aceptación

- 100% endpoints críticos con autenticación y autorización activa.
- 0 CVEs críticas abiertas al cierre de fase.
- Auditoría habilitada para todas las operaciones de alto impacto.
- Evidencia de pruebas de seguridad y regresión aprobadas por QA + responsable técnico.

---

## 3) Fase 2 — Calidad de ingeniería (5 a 7 semanas)

### Objetivo

Asegurar mantenibilidad, confiabilidad funcional y velocidad de entrega con gobernanza técnica y CI/CD.

### Entregables técnicos

1. **Estandarización de calidad**
   - Linter + formatter + type checking (ruff/black/mypy o stack equivalente).
   - Política de calidad en PR: checks obligatorios y umbral mínimo de cobertura.

2. **Estrategia de testing por capas**
   - Unit tests en servicios, CRUD y validaciones de schemas.
   - Integration tests para routers de stock, tareas, ambiente, historial y alertas.
   - Contract tests API (OpenAPI + tests de compatibilidad).
   - End-to-end smoke tests sobre flujos UI críticos.

3. **Refactor estructural progresivo**
   - Separación explícita por capas: routers -> services -> repositories.
   - Manejo uniforme de errores (catálogo de errores de dominio + HTTP mapping).
   - Eliminación de lógica crítica en arranque global; inicialización controlada por comandos.

4. **Pipeline CI/CD profesional**
   - Pipeline con etapas: lint, tests, seguridad, build de artefacto, despliegue a staging.
   - Versionado semántico y changelog automático.
   - Estrategia de releases con feature flags para cambios sensibles.

### Pruebas de la fase

- Cobertura objetivo:
  - >= 80% en capa de dominio/servicios.
  - 100% de casos críticos de negocio (producción/stock/alertas).
- Pruebas de regresión automatizadas por cada PR.
- Pruebas de performance base (latencia p95 y throughput de endpoints más usados).

### Migraciones requeridas

- Migración técnica de estructura de código (sin impacto funcional) por lotes.
- Migración de scripts de arranque y seed a comandos explícitos (`init-db`, `seed-demo`, `seed-minimum`).
- Ajuste de esquema para constraints e índices faltantes detectados por calidad de datos.

### Criterios de aceptación

- Pipeline CI verde en rama principal por 3 iteraciones consecutivas.
- Cobertura y quality gates cumplidos.
- Reducción >= 40% de incidencias regresivas respecto al baseline previo.
- Tiempos de revisión/merge medidos y dentro del objetivo acordado.

---

## 4) Fase 3 — IA avanzada (6 a 10 semanas)

### Objetivo

Incorporar capacidades de IA con impacto operativo real, gobernadas por prácticas MLOps y controles de riesgo.

### Casos de uso priorizados

1. Predicción de consumo de insumos (feed/stock) por sala/pallet.
2. Detección de anomalías en variables ambientales y eventos operativos.
3. Asistente operativo con recomendaciones explicables para producción.

### Entregables técnicos

1. **Plataforma de datos para IA**
   - Dataset versionado (features + labels) con trazabilidad por fecha y fuente.
   - Feature store liviano o capa equivalente de features reproducibles.

2. **Pipeline MLOps**
   - Entrenamiento reproducible + registry de modelos.
   - Validación offline (accuracy, MAE/MAPE, precision/recall según caso).
   - Despliegue de inferencia (batch y/o online) vía servicio versionado.

3. **Gobernanza y seguridad de IA**
   - Validaciones de drift de datos/modelo.
   - Registro de decisiones asistidas por IA y explicación mínima del resultado.
   - Políticas de fallback a reglas determinísticas cuando IA no cumpla umbral.

4. **Integración con producto**
   - Endpoints/API de predicción y recomendaciones.
   - Panel UI con indicadores de confianza, explicación y acción sugerida.

### Pruebas de la fase

- Validación offline con datasets de entrenamiento/validación/test separados.
- Backtesting de pronósticos (ventanas históricas deslizantes).
- Pruebas de robustez (datos faltantes, outliers, distribución cambiante).
- Pruebas online A/B o shadow mode antes de activar decisiones asistidas.

### Migraciones requeridas

- Nuevas tablas para:
  - `ml_model_registry`, `ml_prediction_log`, `ml_feature_snapshot`, `ml_drift_events`.
- ETL incremental de datos históricos operativos hacia dataset de IA.
- Versionado de esquemas de features para compatibilidad retroactiva.

### Criterios de aceptación

- Caso de uso 1 en producción con mejora demostrable (ej. reducción de quiebres de stock >= 20%).
- Monitoreo de drift y performance del modelo activo.
- Trazabilidad completa: input -> modelo -> output -> decisión humana final.
- Manual operativo de IA y política de rollback aprobados.

---

## 5) Fase 4 — Operaciones de producción (6 a 8 semanas)

### Objetivo

Operar con confiabilidad, observabilidad y capacidad de recuperación, bajo prácticas SRE/DevOps.

### Entregables técnicos

1. **Arquitectura de despliegue y entornos**
   - Contenerización estándar y despliegue automatizado (staging/prod).
   - Estrategia blue/green o canary para releases de bajo riesgo.
   - Infra como código para recursos críticos.

2. **Base de datos y resiliencia**
   - Migración a motor productivo gestionado (ej. PostgreSQL) si aplica.
   - Backups automáticos, pruebas de restore y política de retención.
   - Replicación/alta disponibilidad según RTO/RPO definidos.

3. **Observabilidad end-to-end**
   - Métricas (RED/USE), logs estructurados y trazas distribuidas.
   - Dashboards de negocio + técnicos (latencia, errores, saturación, salud jobs).
   - Alerting accionable con on-call y escalamiento.

4. **SRE y continuidad operativa**
   - Definición de SLI/SLO por capacidades críticas.
   - Error budget y proceso de gestión de incidentes.
   - Runbooks de incidentes, postmortems y simulacros (GameDays).

### Pruebas de la fase

- Pruebas de carga y estrés con objetivos de p95/p99.
- Pruebas de resiliencia (caída de dependencia, timeouts, reintentos).
- Disaster Recovery drill: restauración de backup y validación funcional.
- Smoke tests automáticos post-despliegue en cada release.

### Migraciones requeridas

- Migración de datos SQLite/local a base de datos productiva (con plan de corte y rollback).
- Migración de observabilidad a stack centralizada (Prometheus/Grafana/ELK/OTel o equivalente).
- Migración de secretos/config a plataforma administrada de producción.

### Criterios de aceptación

- Cumplimiento sostenido de SLOs por 30 días.
- RTO/RPO dentro de objetivos en simulacro real.
- MTTR reducido frente al baseline de pre-producción.
- Releases sin downtime perceptible en cambios estándar.

---

## 6) Roadmap de ejecución y dependencias

### Secuencia recomendada

- **F1 Seguridad** -> habilita control de acceso y auditoría para todo lo demás.
- **F2 Calidad** -> estabiliza base de código antes de introducir IA avanzada.
- **F3 IA avanzada** -> se apoya en calidad, datos confiables y observabilidad.
- **F4 Operaciones** -> consolida escalabilidad, continuidad y gobierno operacional.

### Hitos transversales por fase

- Kickoff de fase con definición de KPIs/KR.
- Demo quincenal con evidencia técnica + métricas.
- Gate de salida de fase (arquitectura, QA, seguridad, negocio).

---

## 7) Matriz de control (resumen por fase)

| Fase | Entregable clave | Prueba clave | Migración clave | Criterio de aceptación |
|---|---|---|---|---|
| Seguridad | IAM + RBAC + auditoría | DAST + tests de autorización | tablas de usuarios/roles/audit | 100% endpoints críticos protegidos |
| Calidad | CI/CD con quality gates | regresión automatizada + cobertura | refactor por capas + constraints | pipeline verde sostenido |
| IA avanzada | pipeline MLOps + modelo en producción | backtesting + shadow mode | tablas ML + ETL histórico | mejora operacional demostrable |
| Operaciones | observabilidad + SLO + DR | carga/estrés + DR drill | migración DB productiva + monitoreo | SLO cumplido y RTO/RPO validados |

---

## 8) Definición de “hecho” global del programa

El plan se considera completado cuando:

1. Cada fase tenga acta de aceptación con evidencias (tests, métricas, documentos, runbooks).
2. Existan migraciones versionadas y reproducibles para datos y configuración.
3. El sistema opere en producción con SLOs activos, seguridad auditada y mecanismos de mejora continua.

---

## 9) Instrucción concisa para solicitar la ejecución completa

**“Implementa de forma integral todas las observaciones pendientes del PR anterior, incorporando los cambios y mejoras funcionales, técnicas y de calidad necesarios, con pruebas actualizadas y criterios de aceptación verificables.”**
