# Progreso - Paulina Madrid IE

**Última actualización:** 2026-02-23
**Actualizado por:** Claude Code

## Estado General: 🟢 Completado y Desplegado

## Resumen Ejecutivo
Dashboard de presupuesto completo con autenticación Supabase, persistencia de configuración en la nube, 3 escenarios financieros y gastos personalizados. Desplegado y funcional en Streamlit Cloud.

---

## Componentes

### Completados
| Componente | Fecha | Estado |
|------------|-------|--------|
| Estructura del proyecto | 2026-02-18 | Completado |
| Scripts generadores (JSONs, Excel) | 2026-02-18 | Completado |
| Dashboard Streamlit | 2026-02-18 | Completado |
| Autenticación Supabase | 2026-02-18 | Completado |
| Gastos personalizados | 2026-02-18 | Completado |
| Multi-moneda (EUR/USD/COP) | 2026-02-18 | Completado |
| Repositorio GitHub | 2026-02-18 | Completado |
| Tablas Supabase | 2026-02-18 | Completado |
| Documentación (CLAUDE.md) | 2026-02-18 | Completado |
| Deploy Streamlit Cloud | 2026-02-23 | Completado |
| Fix RLS para registro | 2026-02-23 | Completado |
| Guardar config de sliders | 2026-02-23 | Completado |
| Usuario Paulina creado | 2026-02-23 | Completado |

### Pendiente (Opcional)
| Feature | Prioridad | Descripción |
|---------|-----------|-------------|
| Notificaciones por email | Baja | Alertas de cambios |
| Exportar PDF | Baja | Resumen descargable en PDF |
| Comparador visual escenarios | Baja | Side-by-side de los 3 escenarios |

---

## URLs y Recursos

| Recurso | URL/ID |
|---------|--------|
| Dashboard Live | https://fsardi19-paulina-madrid-ie-dashboardapp.streamlit.app |
| GitHub | https://github.com/Fsardi19/paulina-madrid-ie |
| Supabase | https://supabase.com/dashboard/project/bsaazljcfxczdwtzhkcz |
| Project ID Supabase | bsaazljcfxczdwtzhkcz |

---

## Credenciales

### Supabase
```
SUPABASE_URL = "https://bsaazljcfxczdwtzhkcz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJzYWF6bGpjZnhjemR3dHpoa2N6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE0NTA0NzgsImV4cCI6MjA4NzAyNjQ3OH0.lqUKekS_B3hlfWo6PltOcOrFudO29XbvzOE0XBMeyuY"
```

### Usuario Paulina
- Email: paulinatrianaq@icloud.com
- Estado: Confirmado manualmente en Supabase

---

## Datos Financieros

| Escenario | Total 4 años | Mensual |
|-----------|--------------|---------|
| Austero | €134,666 | €2,806 |
| **Moderado** | **€183,953** | **€3,832** |
| Cómodo | €231,406 | €4,821 |

**Ahorro con beca 40%:** ~€46,400 en 4 años

---

## Arquitectura

```
┌─────────────────┐     ┌──────────────────┐
│  Streamlit      │────▶│  JSONs (datos)   │
│  Cloud          │     │  output/*.json   │
└────────┬────────┘     └──────────────────┘
         │
         ▼
┌─────────────────┐
│    Supabase     │
│  - Auth         │
│  - user_settings│
│  - gastos_pers. │
└─────────────────┘
```

---

## Notas Técnicas

- **RLS user_settings:** DESACTIVADO (permite registro sin auth previa)
- **RLS gastos_personalizados:** ACTIVADO (usuarios solo ven sus gastos)
- **App Streamlit Cloud:** Configurada como PÚBLICA
- **Protección:** Autenticación Supabase (email/password)
- **Auto-deploy:** Push a main → deploy automático

---

## Para Próxima Sesión

Si necesitas continuar el proyecto:
1. Lee `CLAUDE.md` para reglas del proyecto
2. Lee `.claude/SESSION_LOG.md` para historial
3. El dashboard está funcional en la URL de arriba
4. Para cambios: editar → commit → push (deploy automático)

---
