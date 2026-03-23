# Roadmap — Monitor de Noticias de Derecho Medioambiental

> **Versión actual:** 1.0 — Monitor básico para un usuario, un área legal, fuentes fijas.
> **Visión:** Plataforma SaaS de inteligencia legal para bufetes de abogados en Chile y Latinoamérica.

---

## ¿Por qué existe este proyecto?

Los abogados especialistas en derecho medioambiental pasan tiempo valioso revisando manualmente decenas de sitios web cada mañana para no perderse novedades regulatorias, fallos judiciales, sanciones o noticias que puedan afectar a sus clientes. Ese tiempo debería estar dedicado a analizar y asesorar, no a navegar sitios.

Este proyecto automatiza esa revisión diaria. Comenzamos con una solución simple y funcional para un profesional, con la arquitectura pensada para crecer hacia un producto comercial de alto valor para el mercado legal latinoamericano.

---

## Estado actual — Versión 1.0

- ✅ 69 fuentes web monitoreadas diariamente
- ✅ Filtrado de relevancia con IA (Google Gemini)
- ✅ Tabla limpia y responsiva (web + móvil)
- ✅ Sin duplicados entre días (historial de URLs)
- ✅ Actualización automática a las 8:00 AM (hora Chile)
- ✅ Deploy estático gratuito (Vercel + GitHub Actions)
- ✅ Costo operativo: $0 (tiers gratuitos)

---

## Hoja de ruta por fases

### Fase 2 — Personalización por usuario
**Objetivo:** Permitir que cada abogado configure su propio monitor.

- Sistema de autenticación (login / registro)
- Panel de usuario donde cada uno elige:
  - Sus fuentes favoritas (de la lista base o agregando nuevas)
  - Su área de especialidad: ambiental, tributario, laboral, societario, etc.
  - Palabras clave adicionales para afinar el filtrado
- El scraper genera resultados personalizados por usuario
- Historial personal de noticias ya leídas

### Fase 3 — Notificaciones y resumen diario
**Objetivo:** Que el abogado reciba las noticias sin necesidad de entrar a la web.

- Email diario automático a las 8:00 AM con el resumen del día
- Selección de formato: lista completa o solo los 10 más relevantes
- Opción de notificación inmediata cuando aparece una noticia de alta urgencia (ej: nuevas sanciones SMA, fallos de tribunales ambientales)
- Integración futura con WhatsApp Business API

### Fase 4 — Panel de administración
**Objetivo:** Gestión centralizada para bufetes con múltiples abogados.

- Administrador del bufete puede gestionar usuarios y permisos
- Estadísticas de uso: qué noticias se leen más, qué fuentes son más relevantes
- Gestión de fuentes: agregar, editar o desactivar fuentes desde la interfaz (sin tocar código)
- Exportación de reportes semanales o mensuales en PDF/Excel
- Etiquetado de noticias: el usuario puede marcar noticias como "para seguimiento", "urgente", "archivado"

### Fase 5 — Expansión de cobertura
**Objetivo:** Aumentar la cobertura geográfica y temática.

- Soporte para más áreas del derecho chileno: tributario, laboral, societario, penal económico, etc.
- Expansión a otros países latinoamericanos: Argentina, Colombia, Perú, México
- Fuentes internacionales relevantes: UNEP, CEPAL, tribunales internacionales de arbitraje ambiental
- Monitoreo de Diario Oficial de Chile (nuevas leyes y decretos en tiempo real)
- Alertas sobre proyectos específicos en el SEIA (Sistema de Evaluación de Impacto Ambiental)

### Fase 6 — Modelo SaaS comercial
**Objetivo:** Convertir el proyecto en un producto con ingresos recurrentes.

**Segmentos objetivo:**
- Bufetes de abogados medianos y grandes en Chile (50–200 abogados)
- Empresas con departamento legal interno (mineras, forestales, pesqueras, constructoras)
- Organismos públicos con necesidad de monitoreo regulatorio
- Estudios jurídicos boutique especializados en derecho ambiental en Latinoamérica

**Planes de precios tentativo:**
| Plan | Usuarios | Áreas legales | Precio estimado |
|------|----------|--------------|-----------------|
| Básico | 1 | 1 | $19 USD/mes |
| Profesional | hasta 5 | hasta 3 | $59 USD/mes |
| Equipo | hasta 20 | ilimitadas | $149 USD/mes |
| Empresa | ilimitado | ilimitadas + soporte | a convenir |

**Infraestructura target:**
- Backend: FastAPI (Python) o Next.js API Routes
- Base de datos: PostgreSQL (Supabase o Railway)
- Autenticación: Clerk o Supabase Auth
- Pagos: Stripe
- Deploy: Vercel (frontend) + Railway o Render (backend)
- Correos: Resend o SendGrid

---

## Principios de diseño del producto

1. **Confiabilidad sobre sofisticación.** Que funcione todos los días sin falla, aunque no sea la tecnología más avanzada.
2. **Cero fricción para el usuario.** El abogado entra, ve las noticias, hace clic. Sin configuraciones complejas.
3. **Transparencia.** El usuario siempre sabe de dónde viene cada noticia y cuándo fue publicada.
4. **Privacidad por defecto.** Los datos del usuario y sus búsquedas no se venden ni comparten.
5. **Costo proporcional al valor.** Comenzar gratis o casi gratis; cobrar solo cuando el producto entregue valor demostrable.

---

## Métricas de éxito

- **Fase 1:** El scraper corre sin errores 5 días seguidos consecutivos
- **Fase 2:** 3 usuarios activos con configuraciones distintas
- **Fase 3:** Tasa de apertura de emails > 60%
- **Fase 4:** 1 bufete usando la versión de equipo
- **Fase 6:** 20 clientes de pago con MRR > $1.000 USD

---

*Documento creado: marzo 2026. Actualizar con cada hito alcanzado.*
