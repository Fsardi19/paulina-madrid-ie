# 🚀 PROMPT DE APERTURA - PAULINA MADRID IE
## Copiar al iniciar sesión de Claude Code

---

## INICIO DE SESIÓN

```
================================================================================
📁 PROYECTO: cd /Users/felipesardi/paulina_madrid
================================================================================
```

---

## FASE 1: CARGA DE CONTEXTO

**ANTES DE HACER CUALQUIER COSA, lee estos archivos EN ORDEN:**

1. **CONFIGURACIÓN:**
   - `CLAUDE.md` → Reglas y contexto del proyecto
   - `.streamlit/secrets.toml.example` → Variables de entorno necesarias

2. **DATOS:**
   - `output/datos_paulina.json` → Estructura de costos base
   - `output/escenarios_paulina.json` → 3 escenarios precalculados

3. **CÓDIGO:**
   - `dashboard/app.py` → Dashboard principal con autenticación
   - `scripts/generar_datos.py` → Generador de JSONs

4. **ESTADO:**
   - `.claude/SESSION_LOG.md` (si existe) → Sesiones anteriores
   - `git log --oneline -5` → Últimos commits

---

## FASE 2: VERIFICAR ENTORNO

```bash
# Estructura del proyecto
ls -la

# Estado de git
git status
git log --oneline -5

# Verificar JSONs existen
ls -la output/

# Verificar Streamlit corriendo (si aplica)
pgrep -f streamlit
```

---

## FASE 3: RECURSOS DEL PROYECTO

### 📊 Stack
| Componente | Tecnología | Notas |
|------------|------------|-------|
| Frontend | Streamlit | Dashboard interactivo |
| Gráficos | Plotly | Barras, líneas, pie |
| Base de Datos | Supabase | PostgreSQL + Auth |
| Deploy | Streamlit Cloud | Auto-deploy desde GitHub |

### 🔗 URLs
| Recurso | URL |
|---------|-----|
| GitHub | https://github.com/Fsardi19/paulina-madrid-ie |
| Supabase | https://supabase.com/dashboard/project/bsaazljcfxczdwtzhkcz |
| Streamlit Cloud | [Configurar en share.streamlit.io] |

### 💰 Datos Financieros Clave
| Concepto | Valor |
|----------|-------|
| Matrícula base | €29,000/año |
| Descuento beca | 40% |
| Duración | 4 años (2026-2030) |
| Inflación | 3%/año |
| Escenario Moderado | ~€184,000 total |

---

## FASE 4: COMANDOS ÚTILES

### Desarrollo Local
```bash
# Ejecutar dashboard
streamlit run dashboard/app.py

# Regenerar datos
python scripts/generar_datos.py

# Regenerar Excel
python scripts/generar_excel.py
```

### Git y Deploy
```bash
# Ver cambios
git status
git diff

# Commit y deploy (auto)
git add .
git commit -m "feat: descripción"
git push
```

### Sesión Claude
```
/compact    → Comprimir historial (cada 10-15 mensajes)
/cost       → Ver costo de la sesión
/context    → Ver tokens usados
```

---

## FASE 5: CONFIRMAR COMPRENSIÓN

**Antes de empezar, confirma que entendiste:**

- [ ] El dashboard tiene autenticación con Supabase
- [ ] Los datos base vienen de JSONs (no se calculan en el dashboard)
- [ ] Los gastos personalizados se guardan en Supabase
- [ ] El deploy es automático al hacer push a GitHub
- [ ] Hay 3 escenarios: Austero, Moderado, Cómodo

---

## REGLAS DE LA SESIÓN

### ✅ SIEMPRE:
- Leer CLAUDE.md antes de actuar
- Usar `/compact` cada 10-15 mensajes
- Si modificas costos base → regenerar JSONs
- Probar localmente antes de push

### ❌ NUNCA:
- Hacer cálculos inline en el dashboard
- Hardcodear datos que existen en JSONs
- Subir secrets.toml a GitHub
- Modificar estructura de Supabase sin documentar

---

## INICIO

**Ahora que cargaste el contexto:**

1. Resúmeme en 3 bullets qué entendiste del proyecto
2. Dime si hay cambios pendientes (git status)
3. Pregúntame qué quiero lograr en esta sesión

**NO empieces a codificar hasta que yo confirme el objetivo.**

---
