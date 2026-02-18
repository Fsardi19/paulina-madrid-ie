#!/usr/bin/env python3
"""
Dashboard Interactivo - Presupuesto Paulina Madrid IE
Con autenticación Supabase y persistencia de datos
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from pathlib import Path
from supabase import create_client, Client
import os

# ============================================================
# CONFIGURACION
# ============================================================
st.set_page_config(
    page_title="Paulina Madrid - Presupuesto IE",
    page_icon="🇪🇸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Supabase config - usar secrets en producción
SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL", "https://bsaazljcfxczdwtzhkcz.supabase.co"))
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", os.getenv("SUPABASE_KEY", ""))

# Inicializar cliente Supabase
@st.cache_resource
def init_supabase():
    if SUPABASE_KEY:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    return None

supabase = init_supabase()

# Rutas locales
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"

# ============================================================
# AUTENTICACION
# ============================================================
def init_session_state():
    """Inicializa variables de sesión"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_email" not in st.session_state:
        st.session_state.user_email = None
    if "gastos_personalizados" not in st.session_state:
        st.session_state.gastos_personalizados = []
    if "user_settings" not in st.session_state:
        st.session_state.user_settings = {}

init_session_state()

def login_page():
    """Muestra página de login"""
    st.markdown("""
    <style>
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        .login-title {
            color: white;
            text-align: center;
            font-size: 2rem;
            margin-bottom: 10px;
        }
        .login-subtitle {
            color: rgba(255,255,255,0.8);
            text-align: center;
            font-size: 1rem;
            margin-bottom: 30px;
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("## 🇪🇸 Presupuesto Madrid")
        st.markdown("### IE University - Dashboard Privado")
        st.markdown("---")

        tab_login, tab_register = st.tabs(["Iniciar Sesión", "Registrarse"])

        with tab_login:
            email = st.text_input("Email", key="login_email", placeholder="paulina@email.com")
            password = st.text_input("Contraseña", type="password", key="login_password")

            if st.button("Entrar", use_container_width=True, type="primary"):
                if email and password:
                    try:
                        response = supabase.auth.sign_in_with_password({
                            "email": email,
                            "password": password
                        })
                        if response.user:
                            st.session_state.authenticated = True
                            st.session_state.user_email = response.user.email
                            load_user_data(response.user.email)
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error de autenticación: {str(e)}")
                else:
                    st.warning("Ingresa email y contraseña")

        with tab_register:
            new_email = st.text_input("Email", key="reg_email", placeholder="paulina@email.com")
            new_password = st.text_input("Contraseña", type="password", key="reg_password",
                                         help="Mínimo 6 caracteres")
            new_password2 = st.text_input("Confirmar contraseña", type="password", key="reg_password2")
            nombre = st.text_input("Nombre", key="reg_nombre", placeholder="Paulina")

            if st.button("Crear cuenta", use_container_width=True):
                if new_email and new_password and nombre:
                    if new_password != new_password2:
                        st.error("Las contraseñas no coinciden")
                    elif len(new_password) < 6:
                        st.error("La contraseña debe tener al menos 6 caracteres")
                    else:
                        try:
                            response = supabase.auth.sign_up({
                                "email": new_email,
                                "password": new_password
                            })
                            if response.user:
                                # Crear configuración inicial
                                supabase.table("user_settings").insert({
                                    "user_email": new_email,
                                    "nombre": nombre,
                                    "ajustes": {}
                                }).execute()
                                st.success("¡Cuenta creada! Revisa tu email para confirmar.")
                        except Exception as e:
                            st.error(f"Error al crear cuenta: {str(e)}")
                else:
                    st.warning("Completa todos los campos")

        st.markdown("---")
        st.caption("Dashboard privado para planificación financiera")

def logout():
    """Cierra sesión"""
    try:
        supabase.auth.sign_out()
    except:
        pass
    st.session_state.authenticated = False
    st.session_state.user_email = None
    st.session_state.gastos_personalizados = []
    st.session_state.user_settings = {}
    st.rerun()

# ============================================================
# PERSISTENCIA EN SUPABASE
# ============================================================
def load_user_data(email):
    """Carga datos del usuario desde Supabase"""
    try:
        # Cargar configuración
        settings = supabase.table("user_settings").select("*").eq("user_email", email).execute()
        if settings.data:
            st.session_state.user_settings = settings.data[0]

        # Cargar gastos personalizados
        gastos = supabase.table("gastos_personalizados").select("*").eq("user_email", email).order("created_at").execute()
        if gastos.data:
            st.session_state.gastos_personalizados = [
                {"id": g["id"], "nombre": g["nombre"], "monto": float(g["monto"]),
                 "tipo": g["tipo"], "activo": g["activo"]}
                for g in gastos.data
            ]
        else:
            st.session_state.gastos_personalizados = []
    except Exception as e:
        st.warning(f"No se pudieron cargar datos: {e}")

def save_gasto(email, nombre, monto, tipo):
    """Guarda un nuevo gasto en Supabase"""
    try:
        result = supabase.table("gastos_personalizados").insert({
            "user_email": email,
            "nombre": nombre,
            "monto": monto,
            "tipo": tipo,
            "activo": True
        }).execute()
        if result.data:
            return result.data[0]
    except Exception as e:
        st.error(f"Error al guardar: {e}")
    return None

def update_gasto(gasto_id, activo):
    """Actualiza estado de un gasto"""
    try:
        supabase.table("gastos_personalizados").update({"activo": activo}).eq("id", gasto_id).execute()
    except Exception as e:
        st.error(f"Error al actualizar: {e}")

def delete_gasto(gasto_id):
    """Elimina un gasto"""
    try:
        supabase.table("gastos_personalizados").delete().eq("id", gasto_id).execute()
    except Exception as e:
        st.error(f"Error al eliminar: {e}")

def save_user_settings(email, settings):
    """Guarda configuración del usuario"""
    try:
        supabase.table("user_settings").upsert({
            "user_email": email,
            **settings
        }).execute()
    except Exception as e:
        st.error(f"Error al guardar configuración: {e}")

# ============================================================
# VERIFICAR AUTENTICACION
# ============================================================
if not supabase:
    st.warning("⚠️ Modo local: Supabase no configurado. Los datos no se guardarán.")
    st.session_state.authenticated = True
    st.session_state.user_email = "local@demo.com"
elif not st.session_state.authenticated:
    login_page()
    st.stop()

# ============================================================
# CARGA DE DATOS (SOLO LECTURA DE JSONs)
# ============================================================
@st.cache_data
def cargar_datos_base():
    with open(OUTPUT_DIR / "datos_paulina.json", "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def cargar_escenarios():
    with open(OUTPUT_DIR / "escenarios_paulina.json", "r", encoding="utf-8") as f:
        return json.load(f)

try:
    DATOS = cargar_datos_base()
    ESCENARIOS = cargar_escenarios()
except FileNotFoundError as e:
    st.error(f"Error: No se encontraron los archivos JSON.")
    st.stop()

# ============================================================
# ESTILOS
# ============================================================
st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 700; color: #1a365d; text-align: center; margin-bottom: 0; }
    .sub-title { font-size: 1.1rem; color: #4a5568; text-align: center; margin-top: 5px; }
    div[data-testid="stMetric"] { background-color: #f7fafc; border-radius: 10px; padding: 15px; border-left: 4px solid #667eea; }
    .user-badge { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# FUNCIONES AUXILIARES
# ============================================================
def formato_moneda(valor, moneda="EUR"):
    simbolos = {"EUR": "€", "USD": "$", "COP": "$"}
    simbolo = simbolos.get(moneda, "€")
    if moneda == "COP":
        return f"{simbolo}{valor:,.0f} COP"
    return f"{simbolo}{valor:,.0f}"

def convertir_moneda(valor_eur, moneda, tasas):
    if moneda == "EUR":
        return valor_eur
    elif moneda == "USD":
        return valor_eur * tasas["EUR_USD"]
    elif moneda == "COP":
        return valor_eur * tasas["EUR_COP"]
    return valor_eur

def recalcular_con_ajustes(escenario_base, ajustes, descuento_matricula, inflacion, tasas_cambio):
    matricula_base = DATOS["costos_base"]["matricula"]["anual_base"]
    descuento = DATOS["supuestos"]["descuento_matricula_disponible"] if descuento_matricula else 0
    matricula_anual = matricula_base * (1 - descuento)

    total_mensual = sum(v for k, v in ajustes.items() if k not in ["vuelos_por_ano", "pct_emergencias", "gastos_personalizados"])
    total_mensual += ajustes.get("gastos_personalizados", 0)

    costo_vuelo = DATOS["costos_base"]["vuelos_colombia"]["medio"]
    vuelos_anual = costo_vuelo * ajustes.get("vuelos_por_ano", 2)
    gastos_vida_anual = (total_mensual * 12) + vuelos_anual

    pct_emergencias = ajustes.get("pct_emergencias", 0.05)
    emergencias_anual = (gastos_vida_anual + matricula_anual) * pct_emergencias
    total_anual = matricula_anual + gastos_vida_anual + emergencias_anual

    anos = DATOS["perfil"]["duracion_anos"]
    proyeccion = []
    total_acumulado = 0

    for i in range(anos):
        factor = (1 + inflacion) ** i
        mat = matricula_anual * factor
        gastos = gastos_vida_anual * factor
        emerg = emergencias_anual * factor
        total = mat + gastos + emerg
        total_acumulado += total
        proyeccion.append({"ano": DATOS["perfil"]["ano_inicio"] + i, "matricula": mat,
                          "gastos_vida": gastos, "emergencias": emerg, "total": total})

    return {
        "matricula_anual": matricula_anual, "ahorro_beca": (matricula_base - matricula_anual) * anos,
        "total_mensual": total_mensual, "vuelos_anual": vuelos_anual, "emergencias_anual": emergencias_anual,
        "total_anual_ano1": total_anual, "proyeccion": proyeccion, "total_4_anos": total_acumulado,
        "promedio_mensual": total_acumulado / (anos * 12)
    }

# ============================================================
# HEADER CON USUARIO
# ============================================================
col_title, col_user = st.columns([4, 1])
with col_title:
    st.markdown('<p class="main-title">🇪🇸 Presupuesto Madrid - IE University</p>', unsafe_allow_html=True)
with col_user:
    user_name = st.session_state.user_settings.get("nombre", st.session_state.user_email.split("@")[0])
    st.markdown(f'<span class="user-badge">👤 {user_name}</span>', unsafe_allow_html=True)
    if st.button("Salir", use_container_width=True):
        logout()

st.markdown(f'<p class="sub-title">Planificación Financiera | {DATOS["perfil"]["ano_inicio"]}-{DATOS["perfil"]["ano_inicio"] + DATOS["perfil"]["duracion_anos"]}</p>', unsafe_allow_html=True)
st.markdown("---")

# ============================================================
# SIDEBAR - CONTROLES
# ============================================================
st.sidebar.markdown("## 🎛️ Panel de Control")

# Escenario
st.sidebar.markdown("### 📊 Escenario Base")
escenario_sel = st.sidebar.selectbox("Cargar preset", ["Moderado", "Austero", "Comodo"], index=0)
escenario_key = escenario_sel.lower()
escenario_actual = ESCENARIOS["escenarios"][escenario_key]

st.sidebar.markdown("---")

# Moneda
st.sidebar.markdown("### 💱 Moneda")
moneda = st.sidebar.selectbox("Mostrar en", ["EUR", "USD", "COP"], index=0)

col_tasa1, col_tasa2 = st.sidebar.columns(2)
with col_tasa1:
    tasa_usd = st.number_input("EUR→USD", value=float(DATOS["supuestos"]["tasas_cambio"]["EUR_USD"]), step=0.01, format="%.2f")
with col_tasa2:
    tasa_cop = st.number_input("EUR→COP", value=float(DATOS["supuestos"]["tasas_cambio"]["EUR_COP"]), step=100.0, format="%.0f")
tasas = {"EUR_USD": tasa_usd, "EUR_COP": tasa_cop}

st.sidebar.markdown("---")

# Matricula
st.sidebar.markdown("### 🎓 Matrícula")
descuento_matricula = st.sidebar.toggle("Aplicar descuento 40%", value=True)
matricula_base = DATOS["costos_base"]["matricula"]["anual_base"]
if descuento_matricula:
    st.sidebar.success(f"€{matricula_base * 0.6:,.0f}/año (ahorro €{matricula_base * 0.4:,.0f})")
else:
    st.sidebar.warning(f"€{matricula_base:,.0f}/año (sin descuento)")

st.sidebar.markdown("---")

# Gastos mensuales
st.sidebar.markdown("### 🏠 Gastos Mensuales")
desglose = escenario_actual["desglose_mensual"]
costos = DATOS["costos_base"]
ajustes = {}

ajustes["vivienda"] = st.sidebar.slider("Vivienda", costos["vivienda"]["min"], costos["vivienda"]["max"],
                                        desglose["vivienda"]["valor"], 50, format="€%d")

with st.sidebar.expander("⚡ Servicios", expanded=False):
    ajustes["electricidad"] = st.slider("Electricidad", costos["electricidad"]["min"], costos["electricidad"]["max"],
                                        desglose["electricidad"]["valor"], 5, format="€%d")
    ajustes["gas_calefaccion"] = st.slider("Gas/Calefacción", costos["gas_calefaccion"]["min"], costos["gas_calefaccion"]["max"],
                                           desglose["gas_calefaccion"]["valor"], 5, format="€%d")
    ajustes["agua"] = st.slider("Agua", costos["agua"]["min"], costos["agua"]["max"],
                                desglose["agua"]["valor"], 5, format="€%d")
    ajustes["internet"] = st.slider("Internet", costos["internet"]["min"], costos["internet"]["max"],
                                    desglose["internet"]["valor"], 5, format="€%d")

ajustes["celular"] = st.sidebar.slider("Celular", costos["celular"]["min"], costos["celular"]["max"],
                                       desglose["celular"]["valor"], 5, format="€%d")
ajustes["supermercado"] = st.sidebar.slider("Supermercado", costos["supermercado"]["min"], costos["supermercado"]["max"],
                                            desglose["supermercado"]["valor"], 25, format="€%d")

es_menor_26 = DATOS["perfil"]["menor_26"]
ajustes["transporte"] = 8 if es_menor_26 else 55
st.sidebar.info(f"Transporte: €{ajustes['transporte']}/mes {'(Abono Joven)' if es_menor_26 else ''}")

ajustes["seguro_medico"] = st.sidebar.slider("Seguro Médico", costos["seguro_medico"]["min"], costos["seguro_medico"]["max"],
                                             desglose["seguro_medico"]["valor"], 5, format="€%d")

st.sidebar.markdown("---")

# Opcionales
st.sidebar.markdown("### 🎭 Gastos Opcionales")
incluir_ocio = st.sidebar.toggle("Ocio y Cultura", value=desglose["ocio_cultura"]["incluido"])
ajustes["ocio_cultura"] = st.sidebar.slider("Monto ocio", costos["ocio_cultura"]["min"], costos["ocio_cultura"]["max"],
                                            desglose["ocio_cultura"]["valor"], 25, format="€%d") if incluir_ocio else 0

incluir_ropa = st.sidebar.toggle("Ropa/Personal", value=desglose["ropa_personal"]["incluido"])
ajustes["ropa_personal"] = st.sidebar.slider("Monto ropa", costos["ropa_personal"]["min"], costos["ropa_personal"]["max"],
                                             desglose["ropa_personal"]["valor"], 10, format="€%d") if incluir_ropa else 0

incluir_materiales = st.sidebar.toggle("Materiales Estudio", value=desglose["materiales_estudio"]["incluido"])
ajustes["materiales_estudio"] = st.sidebar.slider("Monto materiales", costos["materiales_estudio"]["min"], costos["materiales_estudio"]["max"],
                                                  desglose["materiales_estudio"]["valor"], 10, format="€%d") if incluir_materiales else 0

st.sidebar.markdown("---")

# Vuelos
st.sidebar.markdown("### ✈️ Vuelos Colombia")
incluir_vuelos = st.sidebar.toggle("Incluir vuelos", value=True)
ajustes["vuelos_por_ano"] = st.sidebar.slider("Viajes por año", 0, 4, 2) if incluir_vuelos else 0

st.sidebar.markdown("---")

# Emergencias
st.sidebar.markdown("### 🛡️ Fondo Emergencia")
incluir_emergencias = st.sidebar.toggle("Incluir fondo", value=True)
ajustes["pct_emergencias"] = st.sidebar.slider("% del total", 0, 15, 5, format="%d%%") / 100 if incluir_emergencias else 0

st.sidebar.markdown("---")

# Inflacion
st.sidebar.markdown("### 📈 Proyección")
inflacion = st.sidebar.slider("Inflación anual %", 0.0, 8.0, 3.0, 0.5) / 100

st.sidebar.markdown("---")

# ============================================================
# GASTOS PERSONALIZADOS (CON PERSISTENCIA)
# ============================================================
st.sidebar.markdown("### ➕ Gastos Personalizados")
st.sidebar.caption("Se guardan automáticamente")

with st.sidebar.expander("Agregar nuevo gasto", expanded=False):
    nuevo_nombre = st.text_input("Nombre", placeholder="Ej: Gimnasio, Spotify...")
    col_m, col_t = st.columns(2)
    with col_m:
        nuevo_monto = st.number_input("Monto (€)", min_value=0, max_value=5000, value=0, step=10)
    with col_t:
        nuevo_tipo = st.selectbox("Frecuencia", ["Mensual", "Anual"])

    if st.button("➕ Agregar", use_container_width=True):
        if nuevo_nombre and nuevo_monto > 0:
            if supabase:
                result = save_gasto(st.session_state.user_email, nuevo_nombre, nuevo_monto, nuevo_tipo.lower())
                if result:
                    st.session_state.gastos_personalizados.append({
                        "id": result["id"], "nombre": nuevo_nombre, "monto": nuevo_monto,
                        "tipo": nuevo_tipo.lower(), "activo": True
                    })
            else:
                st.session_state.gastos_personalizados.append({
                    "id": len(st.session_state.gastos_personalizados),
                    "nombre": nuevo_nombre, "monto": nuevo_monto, "tipo": nuevo_tipo.lower(), "activo": True
                })
            st.rerun()

# Mostrar gastos existentes
if st.session_state.gastos_personalizados:
    st.sidebar.markdown("**Tus gastos:**")
    for i, gasto in enumerate(st.session_state.gastos_personalizados):
        col_info, col_toggle, col_del = st.sidebar.columns([3, 1, 1])
        with col_info:
            freq = "/mes" if gasto["tipo"] == "mensual" else "/año"
            st.caption(f"{gasto['nombre']}: €{gasto['monto']:.0f}{freq}")
        with col_toggle:
            new_activo = st.checkbox("", value=gasto["activo"], key=f"gasto_{i}", label_visibility="collapsed")
            if new_activo != gasto["activo"]:
                gasto["activo"] = new_activo
                if supabase:
                    update_gasto(gasto["id"], new_activo)
        with col_del:
            if st.button("🗑️", key=f"del_{i}"):
                if supabase:
                    delete_gasto(gasto["id"])
                st.session_state.gastos_personalizados.pop(i)
                st.rerun()

# Calcular totales personalizados
gastos_personalizados_mensual = sum(
    g["monto"] if g["tipo"] == "mensual" else g["monto"] / 12
    for g in st.session_state.gastos_personalizados if g["activo"]
)

if gastos_personalizados_mensual > 0:
    st.sidebar.success(f"Total: €{gastos_personalizados_mensual:,.0f}/mes")

ajustes["gastos_personalizados"] = gastos_personalizados_mensual

# ============================================================
# CALCULOS
# ============================================================
resultados = recalcular_con_ajustes(escenario_actual, ajustes, descuento_matricula, inflacion, tasas)

# ============================================================
# KPIs PRINCIPALES
# ============================================================
total_4_anos = convertir_moneda(resultados["total_4_anos"], moneda, tasas)
promedio_anual = convertir_moneda(resultados["total_4_anos"] / 4, moneda, tasas)
promedio_mensual = convertir_moneda(resultados["promedio_mensual"], moneda, tasas)
ahorro_beca = convertir_moneda(resultados["ahorro_beca"], moneda, tasas)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("💰 Total 4 Años", formato_moneda(total_4_anos, moneda), f"Inflación {inflacion*100:.1f}%/año")
with col2:
    st.metric("📅 Promedio Anual", formato_moneda(promedio_anual, moneda))
with col3:
    st.metric("📆 Promedio Mensual", formato_moneda(promedio_mensual, moneda))
with col4:
    st.metric("🎓 Ahorro Beca", formato_moneda(ahorro_beca, moneda) if descuento_matricula else "€0")

st.markdown("---")

# ============================================================
# TABS DE VISUALIZACION
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs(["📊 Desglose", "📈 Proyección", "🥧 Distribución", "📋 Detalle"])

with tab1:
    col_chart, col_table = st.columns([2, 1])

    with col_chart:
        cat_nombres = {
            "vivienda": "Vivienda", "electricidad": "Electricidad", "gas_calefaccion": "Gas/Calef.",
            "agua": "Agua", "internet": "Internet", "celular": "Celular", "supermercado": "Supermercado",
            "transporte": "Transporte", "seguro_medico": "Seguro Med.", "ocio_cultura": "Ocio/Cultura",
            "ropa_personal": "Ropa/Personal", "materiales_estudio": "Materiales"
        }

        categorias_chart = []
        valores_chart = []

        for cat, nombre in cat_nombres.items():
            if cat in ajustes and ajustes[cat] > 0:
                categorias_chart.append(nombre)
                valores_chart.append(convertir_moneda(ajustes[cat], moneda, tasas))

        for gasto in st.session_state.gastos_personalizados:
            if gasto["activo"]:
                monto_mensual = gasto["monto"] if gasto["tipo"] == "mensual" else gasto["monto"] / 12
                categorias_chart.append(f"✨ {gasto['nombre']}")
                valores_chart.append(convertir_moneda(monto_mensual, moneda, tasas))

        mat_mensual = resultados["matricula_anual"] / 12
        categorias_chart.append("Matrícula")
        valores_chart.append(convertir_moneda(mat_mensual, moneda, tasas))

        fig_barras = go.Figure(go.Bar(x=valores_chart, y=categorias_chart, orientation='h', marker_color='#667eea',
                                      text=[formato_moneda(v, moneda) for v in valores_chart], textposition='auto'))
        fig_barras.update_layout(title=f"Desglose Mensual ({moneda})", height=450, showlegend=False)
        st.plotly_chart(fig_barras, use_container_width=True)

    with col_table:
        st.markdown("#### Resumen Mensual")
        total_con_mat = resultados["total_mensual"] + mat_mensual
        st.markdown(f"**TOTAL: {formato_moneda(convertir_moneda(total_con_mat, moneda, tasas), moneda)}**")

with tab2:
    df_proy = pd.DataFrame(resultados["proyeccion"])
    fig_proy = go.Figure()
    fig_proy.add_trace(go.Bar(x=df_proy["ano"], y=df_proy["matricula"].apply(lambda x: convertir_moneda(x, moneda, tasas)),
                              name="Matrícula", marker_color="#1a365d"))
    fig_proy.add_trace(go.Bar(x=df_proy["ano"], y=df_proy["gastos_vida"].apply(lambda x: convertir_moneda(x, moneda, tasas)),
                              name="Gastos de Vida", marker_color="#667eea"))
    fig_proy.add_trace(go.Scatter(x=df_proy["ano"], y=df_proy["total"].apply(lambda x: convertir_moneda(x, moneda, tasas)),
                                  name="Total", mode="lines+markers", line=dict(color="#e53e3e", width=3)))
    fig_proy.update_layout(title=f"Proyección {DATOS['perfil']['duracion_anos']} Años", barmode="stack", height=400)
    st.plotly_chart(fig_proy, use_container_width=True)

with tab3:
    grupos = {
        "Vivienda": ajustes["vivienda"],
        "Servicios": ajustes.get("electricidad", 0) + ajustes.get("gas_calefaccion", 0) + ajustes.get("agua", 0) + ajustes.get("internet", 0),
        "Vida Diaria": ajustes.get("celular", 0) + ajustes.get("supermercado", 0) + ajustes.get("transporte", 0) + ajustes.get("seguro_medico", 0),
        "Opcionales": ajustes.get("ocio_cultura", 0) + ajustes.get("ropa_personal", 0) + ajustes.get("materiales_estudio", 0),
        "✨ Personalizados": gastos_personalizados_mensual,
        "Matrícula": resultados["matricula_anual"] / 12
    }
    labels_pie = [k for k, v in grupos.items() if v > 0]
    values_pie = [v for v in grupos.values() if v > 0]

    fig_pie = px.pie(values=values_pie, names=labels_pie, title="Distribución Mensual",
                     color_discrete_sequence=px.colors.sequential.Blues_r, hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

with tab4:
    st.markdown("### Proyección Completa")
    df_export = pd.DataFrame(resultados["proyeccion"])
    df_export.columns = ["Año", "Matrícula", "Gastos Vida", "Emergencias", "Total"]
    for col in ["Matrícula", "Gastos Vida", "Emergencias", "Total"]:
        df_export[col] = df_export[col].apply(lambda x: convertir_moneda(x, moneda, tasas))

    total_row = pd.DataFrame([{"Año": "TOTAL", "Matrícula": df_export["Matrícula"].sum(),
                               "Gastos Vida": df_export["Gastos Vida"].sum(), "Emergencias": df_export["Emergencias"].sum(),
                               "Total": df_export["Total"].sum()}])
    df_export = pd.concat([df_export, total_row], ignore_index=True)

    df_display = df_export.copy()
    for col in ["Matrícula", "Gastos Vida", "Emergencias", "Total"]:
        df_display[col] = df_display[col].apply(lambda x: formato_moneda(x, moneda))
    st.dataframe(df_display, hide_index=True, use_container_width=True)

    csv = df_export.to_csv(index=False)
    st.download_button("📥 Descargar CSV", csv, f"paulina_proyeccion_{moneda}.csv", "text/csv")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption(f"Dashboard privado | Usuario: {st.session_state.user_email} | Datos guardados en la nube ☁️")
