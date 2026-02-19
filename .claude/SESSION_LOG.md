# Session Log - Paulina Madrid IE

## Sesión: 2026-02-18 (Sesión Inicial)
**Duración:** ~2 horas
**Costo:** [Usar /cost para verificar]

### 🎯 Objetivo de la Sesión
Crear dashboard completo de presupuesto para que Paulina planifique su permanencia en Madrid estudiando en IE University durante 4 años.

### ✅ Completado
- [x] Extraer datos de costos de imagen IE Madrid (HEIC)
- [x] Crear estructura de proyecto con scripts y dashboard
- [x] Generar JSONs con datos base y 3 escenarios
- [x] Crear dashboard interactivo Streamlit con:
  - Selector de escenarios (Austero/Moderado/Cómodo)
  - Sliders para todas las variables de gasto
  - Toggles para incluir/excluir categorías
  - Multi-moneda (EUR/USD/COP)
  - Gráficos: barras, proyección 4 años, pie chart
  - Exportación CSV
- [x] Agregar gastos personalizados dinámicos
- [x] Integrar autenticación Supabase
- [x] Crear tablas en Supabase (user_settings, gastos_personalizados)
- [x] Persistencia de gastos personalizados en la nube
- [x] Crear repositorio GitHub (público)
- [x] Generar Excel profesional para la familia
- [x] Documentar proyecto (CLAUDE.md, prompts apertura/cierre)

### 📁 Archivos Creados
| Archivo | Descripción |
|---------|-------------|
| `dashboard/app.py` | Dashboard principal con auth Supabase |
| `scripts/generar_datos.py` | Generador de JSONs desde parámetros |
| `scripts/generar_excel.py` | Generador de Excel profesional |
| `output/datos_paulina.json` | Datos base y costos |
| `output/escenarios_paulina.json` | 3 escenarios precalculados |
| `output/resumen_paulina.xlsx` | Excel para la familia |
| `supabase_setup.sql` | SQL para crear tablas |
| `CLAUDE.md` | Documentación del proyecto |
| `.claude/PROMPT_APERTURA.md` | Prompt para iniciar sesión |
| `.claude/PROMPT_CIERRE.md` | Prompt para cerrar sesión |
| `requirements.txt` | Dependencias Python |
| `.gitignore` | Archivos a ignorar |

### 🔧 Decisiones Técnicas
- **Arquitectura:** Dashboard lee SOLO de JSONs, no hace cálculos inline
- **Auth:** Supabase Auth con email/password (gratis)
- **Persistencia:** Gastos personalizados en Supabase, datos base en JSONs
- **Deploy:** Streamlit Cloud con auto-deploy desde GitHub
- **Repo público:** Porque Streamlit Cloud gratis solo permite 1 app privada, pero la auth protege el acceso

### 💰 Datos Financieros Configurados
| Escenario | Total 4 años | Mensual promedio |
|-----------|--------------|------------------|
| Austero | €134,666 | €2,806 |
| Moderado | €183,953 | €3,832 |
| Cómodo | €231,406 | €4,821 |

### 🔗 URLs Creadas
- **GitHub:** https://github.com/Fsardi19/paulina-madrid-ie
- **Supabase Project:** bsaazljcfxczdwtzhkcz

### ⚠️ Pendiente
- [ ] **ALTA:** Completar deploy en Streamlit Cloud (configurar secrets)
- [ ] **MEDIA:** Crear cuenta de prueba para Paulina
- [ ] **BAJA:** Agregar más visualizaciones si se requieren

### 💡 Notas Importantes
- Paulina tiene 19 años → aplica descuento transporte (€8/mes vs €55)
- El descuento de matrícula del 40% está siendo solicitado, no confirmado
- Los vuelos Colombia-España están estimados en €1,000 por viaje (2/año)
- La inflación de España está configurada en 3%/año

### 🔑 Credenciales Supabase (para secrets)
```toml
SUPABASE_URL = "https://bsaazljcfxczdwtzhkcz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJzYWF6bGpjZnhjemR3dHpoa2N6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE0NTA0NzgsImV4cCI6MjA4NzAyNjQ3OH0.lqUKekS_B3hlfWo6PltOcOrFudO29XbvzOE0XBMeyuY"
```

---
