# 🔒 PROMPT DE CIERRE - PAULINA MADRID IE
## Copiar antes de cerrar sesión de Claude Code

---

## CIERRE DE SESIÓN

---

## FASE 1: DOCUMENTAR LA SESIÓN

**Crea o actualiza `.claude/SESSION_LOG.md`:**

```markdown
# Session Log - Paulina Madrid IE

## Sesión: [FECHA Y HORA]
**Duración:** [X minutos/horas]
**Costo:** [usar /cost]

### 🎯 Objetivo de la Sesión
[Qué queríamos lograr]

### ✅ Completado
- [ ] Tarea 1
- [ ] Tarea 2
- [ ] Tarea 3

### 📁 Archivos Modificados
| Archivo | Acción | Descripción |
|---------|--------|-------------|
| dashboard/app.py | Modificado | Qué cambió |
| output/datos.json | Regenerado | Por qué |

### 🔧 Cambios Técnicos
- [Decisión 1 y por qué]
- [Dependencias nuevas]

### ⚠️ Pendiente
- [ ] Prioridad ALTA: ...
- [ ] Prioridad MEDIA: ...

### 💡 Notas
- [Cosas importantes a recordar]

---
```

---

## FASE 2: ACTUALIZAR PROGRESO

**Crea o actualiza `.claude/PROGRESO.md`:**

```markdown
# Progreso - Paulina Madrid IE

**Última actualización:** [FECHA]

## Estado: 🟢 Funcional

## Componentes

### ✅ Completados
- [x] Dashboard con autenticación Supabase
- [x] 3 escenarios (Austero/Moderado/Cómodo)
- [x] Gastos personalizados con persistencia
- [x] Multi-moneda (EUR/USD/COP)
- [x] Repositorio GitHub público
- [x] Tablas Supabase creadas

### 🔄 En Progreso
| Feature | % | Próximo paso |
|---------|---|--------------|
| Deploy Streamlit Cloud | 80% | Configurar secrets |

### 📋 Pendiente
| Feature | Prioridad |
|---------|-----------|
| [Feature pendiente] | Alta/Media/Baja |

## URLs
- GitHub: https://github.com/Fsardi19/paulina-madrid-ie
- Supabase: bsaazljcfxczdwtzhkcz
- Streamlit: [Pendiente]
```

---

## FASE 3: VERIFICACIÓN PRE-CIERRE

```bash
# 1. Estado de git
git status

# 2. Si hay cambios, commit
git add .
git commit -m "feat/fix: [descripción]

- Detalle 1
- Detalle 2

Session: [fecha]"

# 3. Push para deploy automático
git push

# 4. Ver costo
/cost
```

---

## FASE 4: CHECKLIST DE CIERRE

Antes de cerrar, confirma:

- [ ] SESSION_LOG.md actualizado
- [ ] PROGRESO.md actualizado
- [ ] Cambios commiteados y pusheados
- [ ] Dashboard funciona localmente (si modificaste)
- [ ] JSONs regenerados (si cambiaste datos base)

---

## RESUMEN PARA PRÓXIMA SESIÓN

**Dame este resumen estructurado:**

```
RESUMEN PARA PRÓXIMA SESIÓN
============================

📅 Fecha cierre: [HOY]
💰 Costo sesión: [/cost]

🎯 LO QUE SE LOGRÓ:
1.
2.
3.

⚠️ QUEDÓ PENDIENTE:
1.
2.

📁 ARCHIVOS MODIFICADOS:
-
-

🔜 PRÓXIMOS PASOS:
1.
2.

💡 CONTEXTO IMPORTANTE:
-

============================
```

---

## CIERRE FINAL

1. Ejecuta: `/compact`
2. Ejecuta: `/cost` (anota el costo)
3. Si no terminaste: `/rename paulina-madrid-[fecha]`
4. Cierra la terminal

---

## RECORDATORIO

📌 **Archivos que Claude leerá la próxima vez:**
- `CLAUDE.md` → Reglas del proyecto
- `.claude/SESSION_LOG.md` → Historial
- `.claude/PROGRESO.md` → Estado actual
- `output/*.json` → Datos actuales

📌 **El SESSION_LOG es tu memoria entre sesiones. Documenta bien.**

---
