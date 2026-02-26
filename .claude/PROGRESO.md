# Progreso - Paulina Madrid IE

**Última actualización:** 2026-02-26
**Actualizado por:** Claude Code

## Estado General: 🟢 Completado y Funcionando

## Resumen Ejecutivo
Dashboard de presupuesto completo con autenticación Supabase, persistencia de configuración, 3 escenarios financieros y gastos personalizados. Desplegado en Streamlit Cloud con 3 usuarios activos.

---

## Funcionalidades

| Feature | Estado | Descripción |
|---------|--------|-------------|
| Dashboard interactivo | ✅ | Sliders, gráficos, KPIs |
| 3 Escenarios | ✅ | Austero, Moderado, Cómodo |
| Multi-moneda | ✅ | EUR, USD, COP |
| Autenticación | ✅ | Supabase Auth (email/password) |
| Gastos personalizados | ✅ | Se guardan automáticamente |
| Guardar config sliders | ✅ | Botón "Guardar mi configuración" |
| Cambiar escenarios | ✅ | Botón "Aplicar [Escenario]" |
| Exportar CSV | ✅ | Descarga proyección |

---

## URLs y Recursos

| Recurso | URL |
|---------|-----|
| **Dashboard Live** | https://fsardi19-paulina-madrid-ie-dashboardapp.streamlit.app |
| GitHub | https://github.com/Fsardi19/paulina-madrid-ie |
| Supabase | https://supabase.com/dashboard/project/bsaazljcfxczdwtzhkcz |

---

## Usuarios Activos

| Email | Nombre | Config Guardada |
|-------|--------|-----------------|
| paulinatrianaq@icloud.com | Paulina | ✅ |
| ana.quijanob@gmail.com | - | ✅ |
| fsardi@biodiversal.com | - | ✅ |

---

## Credenciales Supabase

```
SUPABASE_URL = "https://bsaazljcfxczdwtzhkcz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJzYWF6bGpjZnhjemR3dHpoa2N6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE0NTA0NzgsImV4cCI6MjA4NzAyNjQ3OH0.lqUKekS_B3hlfWo6PltOcOrFudO29XbvzOE0XBMeyuY"
```

---

## Datos Financieros

| Escenario | Total 4 años | Mensual |
|-----------|--------------|---------|
| Austero | €134,666 | €2,806 |
| **Moderado** | **€183,953** | **€3,832** |
| Cómodo | €231,406 | €4,821 |

---

## Notas Técnicas

- **Hosting:** Streamlit Cloud (gratis, siempre activo)
- **Auth:** Supabase Auth - app pública pero contenido protegido
- **RLS:** Desactivado en user_settings, activado en gastos_personalizados
- **Auto-deploy:** Push a main → deploy automático en ~1 min

---

## Pendiente (Opcional, Baja Prioridad)

| Feature | Descripción |
|---------|-------------|
| Exportar PDF | Resumen descargable |
| Comparador escenarios | Vista side-by-side |
| Notificaciones email | Alertas de cambios |

---
