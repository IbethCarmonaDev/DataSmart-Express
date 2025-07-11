import streamlit as st
import pandas as pd
import os
import time
from dotenv import load_dotenv
import openai

from auth.interfaz_login import mostrar_login
from auth.reset_password import mostrar_reset_password
from core.analisis_estado_resultados import cargar_cache, obtener_estado_por_mes, obtener_estado_anual, generar_estado_resultados_detallado
from core.planes import obtener_funcionalidades, filtrar_kpis_por_plan
from core.preparacion_datos import preparar_df_mensual, validar_archivo_usuario
from core.configuracion import registrar_log
from secciones.seccion_detallado import mostrar_detallado
from secciones.seccion_anual import mostrar_anual
from secciones.seccion_kpi import mostrar_kpis
from secciones.seccion_analisis import mostrar_analisis
from secciones.seccion_graficas_inteligente import mostrar_graficas
from secciones.seccion_exportar import mostrar_exportacion
from auth.verificacion import mostrar_verificacion_o_reset
from auth.redireccion_fragmento import redireccionar_fragmento_si_es_necesario
from auth.manejo_confirmacion import insertar_perfil_post_signup
from utilidades.mensajes import mostrar_mensaje_confirmacion
from secciones.seccion_planes import mostrar_interfaz_planes
from presentacion.layout_base import mostrar_layout
from secciones.seccion_inicio import mostrar_inicio
from secciones.seccion_perfil import mostrar_perfil

# --- Configuración inicial ---
load_dotenv(override=True)
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="", layout="wide")
redireccionar_fragmento_si_es_necesario()

# --- Leer parámetros desde la URL ---
params = st.query_params
params = {k: v[0] if isinstance(v, list) else v for k, v in params.items()}
token = params.get("access_token")
recovery_type = params.get("type")

# --- Flujo de recuperación de contraseña ---
if token and recovery_type == "recovery":
    mostrar_reset_password(token)
    st.stop()

elif token and recovery_type == "signup":
    resultado = insertar_perfil_post_signup()
    if resultado["status"] == "ok":
        mostrar_mensaje_confirmacion(
            titulo="¡Registro confirmado!",
            mensaje="Tu perfil ha sido creado exitosamente. Ya puedes iniciar sesión.",
            tipo="success",
            boton_texto="Iniciar sesión",
            boton_callback=mostrar_login(),
            mensaje_final="¡ Gracias por unirte a DataSmart Express. Tu análisis financiero inteligente comienza ahora !"
        )
    else:
        st.error(f"⚠ {resultado['mensaje']}")
        st.markdown("⬅ [Volver al login](?reload=true)")
    st.stop()

elif token:
    mostrar_verificacion_o_reset(token)
    st.stop()

if "usuario" not in st.session_state:
    mostrar_login()
    st.stop()

usuario = st.session_state["usuario"]
if "pagina_actual" not in st.session_state:
    st.session_state["pagina_actual"] = "Inicio"

form_data = params.get("pagina", None)
if form_data:
    st.session_state["pagina_actual"] = form_data

mostrar_layout(nombre_usuario=usuario["nombre"], plan_usuario=usuario["plan_actual"])
pagina = st.session_state.get("pagina_actual", "Inicio")
ruta_parametros = "data/Parametros.xlsx"

# --- Navegación principal ---
if pagina == "Planes":
    mostrar_interfaz_planes(ruta_parametros)
    st.stop()
elif pagina == "Perfil":
    mostrar_perfil(usuario)
    st.stop()
elif pagina == "Salir":
    del st.session_state["usuario"]
    st.success("Sesión cerrada.")
    st.stop()

# --- Página de inicio (carga de archivo) ---
archivo_usuario = mostrar_inicio(usuario["nombre"], usuario["plan_actual"])

if not archivo_usuario:
    mostrar_interfaz_planes(ruta_parametros)
    st.stop()

# --- Parámetros generales ---
df_kpis_param = pd.read_excel(ruta_parametros, sheet_name="KPIS_FINANCIEROS")
df_tarjetas = pd.read_excel(ruta_parametros, sheet_name="TARJETAS")
df_tarjetas.columns = df_tarjetas.columns.str.strip().str.upper()
df_graficas = pd.read_excel(ruta_parametros, sheet_name="GRAFICAS")
kpis_para_resaltar = df_kpis_param[df_kpis_param["MOSTRAR_EN_PG"] == 1]["KPI"].dropna().str.upper().tolist()
config_analisis = pd.read_excel(ruta_parametros, sheet_name="EN_ANALISIS", index_col=0)

# --- Lógica de análisis ---
if archivo_usuario:
    t_inicio = time.time()
    df_datos = pd.read_excel(archivo_usuario, sheet_name="DATOS_FINANCIEROS")
    df_clasificacion = pd.read_excel(archivo_usuario, sheet_name="CLASIFICACION_CUENTAS")
    registrar_log("Carga archivo", round(time.time() - t_inicio, 2))

    if not validar_archivo_usuario(df_datos, df_clasificacion):
        st.stop()

    df_planes = pd.read_excel(ruta_parametros, sheet_name="PLANES", index_col=0)
    plan_seleccionado = usuario['plan_actual']
    config_plan = obtener_funcionalidades(plan_seleccionado, ruta_parametros)
    config = {f: bool(config_analisis.loc[f, plan_seleccionado]) for f in config_analisis.index}

    usar_gpt_graficas = False
    if config_plan.get("GRAFICAS_INTELIGENTES", 0):
        usar_gpt_graficas = st.checkbox("💡 Activar análisis GPT en Gráficas (puede consumir créditos)", value=False)

    año = st.selectbox("1️⃣ Selecciona el año", sorted(df_datos["AÑO"].unique(), reverse=True))
    meses = {i: m for i, m in enumerate(
        ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"], start=1)}
    mes_nombre = st.selectbox("2️⃣ Selecciona el mes", list(meses.values()))
    mes = list(meses.keys())[list(meses.values()).index(mes_nombre)]

    if config_plan.get("FILTRAR_CENTRO_COSTO", 0):
        centros = ["TODOS"] + sorted(df_datos["CENTRO_COSTOS"].dropna().unique())
        centro = st.selectbox("3️⃣ Selecciona centro de costos (opcional)", centros)
    else:
        st.warning("🔒 Tu plan no permite filtrar por centro de costos. Se analizarán todos.")
        centro = "TODOS"

    estados = cargar_cache(df_datos, df_clasificacion, ruta_parametros)
    df_mes, df_mes_ant = obtener_estado_por_mes(estados, año, mes, centro)
    df_mensual = preparar_df_mensual(df_datos, df_clasificacion, año, mes, centro)
    df_pg_anual = obtener_estado_anual(estados, df_clasificacion, df_kpis_param, año, centro)
    df_kpis_filtrados = filtrar_kpis_por_plan(df_kpis_param, plan_seleccionado, ruta_parametros)

    t_estado = time.time()
    df_estado, df_kpis_tarjeta = generar_estado_resultados_detallado(estados, df_clasificacion, df_tarjetas, año, mes, df_kpis_filtrados, centro)
    registrar_log("Estado de Resultados Mensual", round(time.time() - t_estado, 2))

    tabs = ["📜 Detallado"]
    if config_plan.get("PG_ANUAL", 0): tabs.append("📊 Anual")
    if config_plan.get("TARJETAS_KPI", 0): tabs.append("📌 KPIs")
    if config_plan.get("ANALISIS_LENGUAJE", 0) or config_plan.get("ANALISIS_AVANZADO", 0): tabs.append("👀 Análisis")
    if config_plan.get("GRAFICAS", 0): tabs.append("📈 Gráficas")
    if config_plan.get("EXPORTAR_EXCEL", 0) or config_plan.get("EXPORTAR_PDF", 0): tabs.append("📤 Exportar")

    selected = st.tabs(tabs)
    for i, tab in enumerate(tabs):
        with selected[i]:
            if tab == "📜 Detallado":
                mostrar_detallado(df_estado, df_kpis_filtrados)
            elif tab == "📊 Anual":
                mostrar_anual(df_pg_anual, kpis_para_resaltar)
            elif tab == "📌 KPIs":
                mostrar_kpis(df_kpis_tarjeta, df_tarjetas, plan_seleccionado)
            elif tab == "👀 Análisis":
                mostrar_analisis(df_estado, estados, ruta_parametros, año, mes, config_plan,
                                 df_pg_anual, df_mensual, plan_seleccionado, config)
            elif tab == "📈 Gráficas":
                t_graficas = time.time()
                mostrar_graficas(df_graficas, df_pg_anual, df_mensual, plan_seleccionado, usar_gpt_graficas, año, mes_nombre)
                registrar_log("Gráficas", round(time.time() - t_graficas, 2))
            elif tab == "📤 Exportar":
                mostrar_exportacion(df_estado, df_kpis_filtrados, año, mes, config_plan)

# --- Mensajes de plan ---
plan = usuario.get("plan_actual")
dias_restantes = usuario.get("dias_restantes_trial")

if plan == "Premium_trial" and dias_restantes is not None and dias_restantes > 0:
    mostrar_mensaje_confirmacion(
        titulo="¡Estás usando el plan Premium Trial!",
        mensaje=f"📆 Te quedan {dias_restantes} días para disfrutar todas las funcionalidades.",
        tipo="info"
    )

# import streamlit as st
# import pandas as pd
# import os
# import time
# from dotenv import load_dotenv
# import openai
#
# from auth.interfaz_login import mostrar_login
# from auth.reset_password import mostrar_reset_password
# from core.analisis_estado_resultados import cargar_cache, obtener_estado_por_mes, obtener_estado_anual, generar_estado_resultados_detallado
# from core.planes import obtener_funcionalidades, filtrar_kpis_por_plan
# from core.preparacion_datos import preparar_df_mensual, validar_archivo_usuario
# from core.configuracion import registrar_log
# from secciones.seccion_detallado import mostrar_detallado
# from secciones.seccion_anual import mostrar_anual
# from secciones.seccion_kpi import mostrar_kpis
# from secciones.seccion_analisis import mostrar_analisis
# from secciones.seccion_graficas_inteligente import mostrar_graficas
# from secciones.seccion_exportar import mostrar_exportacion
# from auth.verificacion import mostrar_verificacion_o_reset
# from auth.redireccion_fragmento import redireccionar_fragmento_si_es_necesario
# from auth.manejo_confirmacion import insertar_perfil_post_signup
# from utilidades.mensajes import mostrar_mensaje_confirmacion
# from secciones.seccion_planes import mostrar_interfaz_planes
# from presentacion.layout_base import mostrar_layout
# from secciones.seccion_inicio import mostrar_inicio
# from secciones.seccion_perfil import mostrar_perfil
# # --- Configuración inicial ---
# load_dotenv(override=True)
# openai.api_key = os.getenv("OPENAI_API_KEY")
#
#
# st.set_page_config(page_title="", layout="wide")
#
# # Detectar fragmento y redirigir
# redireccionar_fragmento_si_es_necesario()
#
#
# # --- Leer parámetros desde la URL ---
# params = st.query_params
# params = {k: v[0] if isinstance(v, list) else v for k, v in params.items()}
# token = params.get("access_token")
# recovery_type = params.get("type")
#
# # --- Flujo de recuperación de contraseña ---
# if token and recovery_type == "recovery":
#     mostrar_reset_password(token)
#     st.stop()
#
# # --- Flujo de registro confirmado ---
# elif token and recovery_type == "signup":
#     resultado = insertar_perfil_post_signup()
#
#     if resultado["status"] == "ok":
#         mostrar_mensaje_confirmacion(
#             titulo="¡Registro confirmado!",
#             mensaje="Tu perfil ha sido creado exitosamente. Ya puedes iniciar sesión.",
#             tipo="success",  # Opcional, por defecto es "success"
#             boton_texto="Iniciar sesión",
#             boton_callback= mostrar_login(),  # Esta debe ser una función que lleva al login
#             mensaje_final = "¡ Gracias por unirte a DataSmart Express. Tu análisis financiero inteligente comienza ahora !"
#         )
#
#
#     else:
#         st.error(f"⚠ {resultado['mensaje']}")
#         st.markdown("⬅ [Volver al login](?reload=true)")
#
#     st.stop()
#
# # --- Verificación genérica ---
# elif token:
#     mostrar_verificacion_o_reset(token)
#     st.stop()
#
# # --- Login normal ---
# if "usuario" not in st.session_state:
#     mostrar_login()
#     st.stop()
#
# # --- Mostrar mensaje según plan ---
# usuario = st.session_state["usuario"]
#
#
# if "pagina_actual" not in st.session_state:
#     st.session_state["pagina_actual"] = "Inicio"
#
# # Capturar navegación desde formulario HTML
# form_data = params.get("pagina", None)
# if form_data:
#     st.session_state["pagina_actual"] = form_data
#
#
#
# mostrar_layout(nombre_usuario=usuario["nombre"], plan_usuario=usuario["plan_actual"])
#
#
# pagina = st.session_state["pagina_actual"]
#
# # 👉 Control de navegación
# if pagina == "Inicio":
#     archivo_usuario = mostrar_inicio(usuario["nombre"], usuario["plan_actual"])
#     # if not archivo_usuario:
#     #     mostrar_interfaz_planes("data/Parametros.xlsx")
#     #     st.stop()
# elif pagina == "Planes":
#     mostrar_interfaz_planes("data/Parametros.xlsx")
#     st.stop()
# # elif pagina == "Perfil":
#     # st.subheader("👤 Perfil del usuario")
#     # st.write(usuario)
#     # st.stop()
#
#
# elif pagina == "Perfil":
#     mostrar_perfil(usuario)
#
# elif pagina == "Salir":
#     del st.session_state["usuario"]
#     st.success("Sesión cerrada.")
#     st.stop()
# else:
#     archivo_usuario = mostrar_inicio(usuario["nombre"], usuario["plan_actual"])
#     # if not archivo_usuario:
#     #     mostrar_interfaz_planes("data/Parametros.xlsx")
#     #     st.stop()
#
#
# plan = usuario.get("plan_actual")
# dias_restantes = usuario.get("dias_restantes_trial")
#
# if plan == "Premium_trial" and dias_restantes is not None and dias_restantes > 0:
#     mostrar_mensaje_confirmacion(
#         titulo="¡Estás usando el plan Premium Trial!",
#         mensaje=f"📆 Te quedan {dias_restantes} días para disfrutar todas las funcionalidades.",
#         tipo="info"
#     )
# # elif plan == "Free" and usuario.get("fecha_inicio_trial"):
# #     mostrar_mensaje_confirmacion(
# #         titulo="⛔ Tu periodo de prueba ha finalizado",
# #         mensaje="Has pasado al plan Free. Algunas funcionalidades estarán limitadas.",
# #         tipo="warning"
# #     )
#
#
# # --- Encabezado general ---
# # try:
# #     logo = Image.open("Logo.png")
# #     st.image(logo, width=200)
# # except:
# #     pass
#
# # st.markdown("## 📈 DataSmart Express")
# # st.markdown("_Estado de Resultados Inteligente con KPIs Financieros_", unsafe_allow_html=True)
# # st.markdown(f"👤 Usuario: {st.session_state.usuario['nombre']} | Plan: **{st.session_state.usuario['plan_actual']}**")
#
# #archivo_usuario = st.file_uploader("📂 Carga tu archivo con datos contables y clasificación de cuentas", type=["xlsx"])
# archivo_usuario = mostrar_inicio(usuario["nombre"], usuario["plan_actual"])
#
#
# ruta_parametros = "data/Parametros.xlsx"
#
# if not archivo_usuario:
#     mostrar_interfaz_planes(ruta_parametros)
#     st.stop()
#
# # --- Parámetros generales ---
# df_kpis_param = pd.read_excel(ruta_parametros, sheet_name="KPIS_FINANCIEROS")
# df_tarjetas = pd.read_excel(ruta_parametros, sheet_name="TARJETAS")
# df_tarjetas.columns = df_tarjetas.columns.str.strip().str.upper()
# df_graficas = pd.read_excel(ruta_parametros, sheet_name="GRAFICAS")
# kpis_para_resaltar = df_kpis_param[df_kpis_param["MOSTRAR_EN_PG"] == 1]["KPI"].dropna().str.upper().tolist()
# config_analisis = pd.read_excel(ruta_parametros, sheet_name="EN_ANALISIS", index_col=0)
#
# if archivo_usuario:
#     t_inicio = time.time()
#     df_datos = pd.read_excel(archivo_usuario, sheet_name="DATOS_FINANCIEROS")
#     df_clasificacion = pd.read_excel(archivo_usuario, sheet_name="CLASIFICACION_CUENTAS")
#     registrar_log("Carga archivo", round(time.time() - t_inicio, 2))
#     if not validar_archivo_usuario(df_datos, df_clasificacion): st.stop()
#
#     df_planes = pd.read_excel(ruta_parametros, sheet_name="PLANES", index_col=0)
#     plan_seleccionado = st.session_state.usuario['plan_actual']
#     config_plan = obtener_funcionalidades(plan_seleccionado, ruta_parametros)
#     config = {f: bool(config_analisis.loc[f, plan_seleccionado]) for f in config_analisis.index}
#
#     usar_gpt_graficas = False
#     if config_plan.get("GRAFICAS_INTELIGENTES", 0):
#         usar_gpt_graficas = st.checkbox("💡 Activar análisis GPT en Gráficas (puede consumir créditos)", value=False)
#
#     año = st.selectbox("1️⃣ Selecciona el año", sorted(df_datos["AÑO"].unique(), reverse=True))
#     meses = {i: m for i, m in enumerate(
#         ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"], start=1)}
#     mes_nombre = st.selectbox("2️⃣ Selecciona el mes", list(meses.values()))
#     mes = list(meses.keys())[list(meses.values()).index(mes_nombre)]
#
#     if config_plan.get("FILTRAR_CENTRO_COSTO", 0):
#         centros = ["TODOS"] + sorted(df_datos["CENTRO_COSTOS"].dropna().unique())
#         centro = st.selectbox("3️⃣ Selecciona centro de costos (opcional)", centros)
#     else:
#         st.warning("🔒 Tu plan no permite filtrar por centro de costos. Se analizarán todos.")
#         centro = "TODOS"
#
#     estados = cargar_cache(df_datos, df_clasificacion, ruta_parametros)
#     df_mes, df_mes_ant = obtener_estado_por_mes(estados, año, mes, centro)
#     df_mensual = preparar_df_mensual(df_datos, df_clasificacion, año, mes, centro)
#     df_pg_anual = obtener_estado_anual(estados, df_clasificacion, df_kpis_param, año, centro)
#     df_kpis_filtrados = filtrar_kpis_por_plan(df_kpis_param, plan_seleccionado, ruta_parametros)
#
#     t_estado = time.time()
#     df_estado, df_kpis_tarjeta = generar_estado_resultados_detallado(estados, df_clasificacion, df_tarjetas, año, mes, df_kpis_filtrados, centro)
#     registrar_log("Estado de Resultados Mensual", round(time.time() - t_estado, 2))
#
#     tabs = ["📜 Detallado"]
#     if config_plan.get("PG_ANUAL", 0): tabs.append("📊 Anual")
#     if config_plan.get("TARJETAS_KPI", 0): tabs.append("📌 KPIs")
#     if config_plan.get("ANALISIS_LENGUAJE", 0) or config_plan.get("ANALISIS_AVANZADO", 0): tabs.append("👀 Análisis")
#     if config_plan.get("GRAFICAS", 0): tabs.append("📈 Gráficas")
#     if config_plan.get("EXPORTAR_EXCEL", 0) or config_plan.get("EXPORTAR_PDF", 0): tabs.append("📤 Exportar")
#
#     selected = st.tabs(tabs)
#     for i, tab in enumerate(tabs):
#         with selected[i]:
#             if tab == "📜 Detallado":
#                 mostrar_detallado(df_estado, df_kpis_filtrados)
#             elif tab == "📊 Anual":
#                 mostrar_anual(df_pg_anual, kpis_para_resaltar)
#             elif tab == "📌 KPIs":
#                 mostrar_kpis(df_kpis_tarjeta, df_tarjetas, plan_seleccionado)
#             elif tab == "👀 Análisis":
#                 mostrar_analisis(df_estado, estados, ruta_parametros, año, mes, config_plan,
#                                  df_pg_anual, df_mensual, plan_seleccionado, config)
#             elif tab == "📈 Gráficas":
#                 t_graficas = time.time()
#                 mostrar_graficas(df_graficas, df_pg_anual, df_mensual, plan_seleccionado, usar_gpt_graficas, año, mes_nombre)
#                 registrar_log("Gráficas", round(time.time() - t_graficas, 2))
#             elif tab == "📤 Exportar":
#                 mostrar_exportacion(df_estado, df_kpis_filtrados, año, mes, config_plan)
#
