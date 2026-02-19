# CLAUDE.md - Proyecto Paulina Madrid IE

## Descripción del Proyecto
Dashboard interactivo de presupuesto para planificar el costo de permanencia de Paulina estudiando en IE University Madrid durante 4 años (2026-2030).

## Stack Tecnológico
- **Frontend:** Streamlit
- **Visualización:** Plotly
- **Base de Datos:** Supabase (PostgreSQL)
- **Autenticación:** Supabase Auth
- **Lenguaje:** Python 3.10+
- **Deploy:** Streamlit Cloud (auto-deploy desde GitHub)

## Estructura del Proyecto
```
paulina-madrid/
├── dashboard/
│   └── app.py              # Dashboard principal con auth
├── output/
│   ├── datos_paulina.json  # Datos base y costos
│   ├── escenarios_paulina.json  # 3 escenarios precalculados
│   └── resumen_paulina.xlsx     # Excel para la familia
├── scripts/
│   ├── generar_datos.py    # Genera JSONs desde parámetros
│   └── generar_excel.py    # Genera Excel profesional
├── .streamlit/
│   └── secrets.toml.example
├── requirements.txt
├── supabase_setup.sql      # SQL para crear tablas
└── CLAUDE.md               # Este archivo
```

## URLs y Recursos
- **GitHub:** https://github.com/Fsardi19/paulina-madrid-ie
- **Streamlit Cloud:** [Pendiente deploy]
- **Supabase Project:** bsaazljcfxczdwtzhkcz

## Reglas del Proyecto

### Arquitectura
- El dashboard **SOLO lee de JSONs**, nunca hace cálculos inline
- Los scripts en `/scripts/` generan los JSONs
- Supabase guarda: gastos personalizados y configuración de usuario
- Los JSONs contienen los datos base y escenarios precalculados

### Datos Financieros
- **Matrícula base:** €29,000/año
- **Descuento aplicable:** 40%
- **Duración:** 4 años (2026-2030)
- **Inflación estimada:** 3% anual
- **Monedas:** EUR, USD, COP

### Escenarios
| Escenario | Descripción | Total 4 años |
|-----------|-------------|--------------|
| Austero | Mínimo posible, sin extras | ~€135,000 |
| Moderado | Balance calidad-costo | ~€184,000 |
| Cómodo | Sin restricciones | ~€231,000 |

### Reglas de Código
- NUNCA calcular mentalmente → siempre código Python
- NUNCA hardcodear datos → todo parametrizado
- Usar `@st.cache_data` para carga de datos
- Usar `@st.cache_resource` para conexiones (Supabase)
- Máximo 6 KPIs por vista, 4 gráficos por sección

### Supabase
- **Tablas:** `user_settings`, `gastos_personalizados`
- **RLS habilitado:** usuarios solo ven sus datos
- **Auth:** Email/password

## Comandos Útiles

```bash
# Regenerar JSONs
python scripts/generar_datos.py

# Regenerar Excel
python scripts/generar_excel.py

# Ejecutar dashboard local
streamlit run dashboard/app.py

# Deploy (automático al hacer push)
git add . && git commit -m "mensaje" && git push
```

## Cambios que Requieren Actualizar JSONs
Si se modifica cualquiera de estos, ejecutar `python scripts/generar_datos.py`:
- Costos base (matrícula, vivienda, servicios)
- Rangos de escenarios
- Tasas de cambio
- Supuestos de inflación

## Notas para Claude
- El perfil de Paulina: 19 años, colombiana, menor de 26 (descuento transporte)
- Los vuelos Colombia-España están incluidos (2/año en moderado)
- El fondo de emergencia es % del total (5-10%)
- Los gastos personalizados se guardan en Supabase, no en JSONs
