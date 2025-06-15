import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="DataSmart Express", layout="wide")
import pandas as pd
from PIL import Image

import os
from dotenv import load_dotenv
import openai

load_dotenv(override=True)  # recarga el .env actual
print("🔧 Modo actual:", os.getenv("APP_ENV"), "| Clave GPT presente:", bool(os.getenv("OPENAI_API_KEY")))

openai.api_key = os.getenv("OPENAI_API_KEY")
print("🔑 OpenAI Key cargada:", bool(openai.api_key and openai.api_key.startswith("sk-")))

# --- NUEVAS RUTAS DE IMPORTACIÓN ---
from core.analisis_estado_resultados import (generar_estado_resultados_detallado, \
                                             generar_estado_resultados_todos_los_meses)
from core.analisis_estado_resultados_anual import generar_estado_resultados_anual
from core.analisis_lenguaje import generar_conclusiones
from core.analisis_avanzado import generar_conclusiones_avanzadas, generar_tabla_comparativa_html
from presentacion.analisis_presentacion import generar_html_estado_resultados
from presentacion.exportacion import exportar_pdf, exportar_excel
from core.planes import obtener_funcionalidades, filtrar_kpis_por_plan
from presentacion.analisis_presentacion import generar_html_estado_resultados_anual
from core.planes import obtener_graficas_por_plan
from presentacion.graficas import grafico_generico, grafico_participacion_mensual, exportar_grafico_plotly
from core.preparacion_datos import preparar_df_mensual, validar_archivo_usuario
from core.analisis_mes_anual import analizar_mes_anual


# --- CONFIGURACIÓN DE PÁGINA ---

# --- MOSTRAR LOGO ---
try:
    logo = Image.open("Logo.png")
    st.image(logo, width=200)
except:
    st.write("")

st.markdown("## 📈 DataSmart Express", unsafe_allow_html=True)
st.markdown("_Estado de Resultados Inteligente con KPIs Financieros_", unsafe_allow_html=True)

# --- CARGA DE ARCHIVO DEL USUARIO ---
archivo_usuario = st.file_uploader("📂 Carga tu archivo con datos contables y clasificación de cuentas", type=["xlsx"])

# --- CARGA INTERNA DE PARAMETROS ---
ruta_parametros = "data/Parametros.xlsx"
df_kpis_param = pd.read_excel(ruta_parametros, sheet_name="KPIS_FINANCIEROS")
df_tarjetas = pd.read_excel(ruta_parametros, sheet_name="TARJETAS")
df_graficas = pd.read_excel(ruta_parametros, sheet_name="GRAFICAS")
kpis_para_resaltar = df_kpis_param[df_kpis_param["MOSTRAR_EN_PG"] == 1]["KPI"].dropna().astype(str).str.upper().tolist()
config_analisis = pd.read_excel(ruta_parametros, sheet_name="EN_ANALISIS", index_col=0)

load_dotenv()  # busca y carga tu .env
openai.api_key = os.getenv("OPENAI_API_KEY")

if archivo_usuario:
    df_datos = pd.read_excel(archivo_usuario, sheet_name="DATOS_FINANCIEROS")
    df_clasificacion = pd.read_excel(archivo_usuario, sheet_name="CLASIFICACION_CUENTAS")


    if not validar_archivo_usuario(df_datos, df_clasificacion):
        st.stop()


    # --- SELECCION DE PLAN ---
    df_planes = pd.read_excel(ruta_parametros, sheet_name="PLANES", index_col=0)
    planes_disponibles = df_planes.columns.tolist()

    plan_seleccionado = st.selectbox("🌟 Selecciona tu plan de análisis", planes_disponibles)
    config_plan = obtener_funcionalidades(plan_seleccionado, "data/Parametros.xlsx")
    st.session_state["plan"] = plan_seleccionado

    config = {f: bool(config_analisis.loc[f, plan_seleccionado]) for f in config_analisis.index}

    # Crear diccionario de funcionalidades activas para el plan

    config_plan = obtener_funcionalidades(plan_seleccionado, "data/Parametros.xlsx")
    año = st.selectbox("1️⃣ Selecciona el año", sorted(df_datos["AÑO"].unique(), reverse=True))
    meses = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }

    mes_nombre = st.selectbox("2️⃣ Selecciona el mes", list(meses.values()))
    mes = list(meses.keys())[list(meses.values()).index(mes_nombre)]

    # --- Combo Centro de Costos controlado por plan ---
    # --- Centro de Costos por plan ---

    if config_plan.get("FILTRAR_CENTRO_COSTO", 0):
        centros = ["TODOS"] + sorted(df_datos["CENTRO_COSTOS"].dropna().unique())
        centro = st.selectbox("3️⃣ Selecciona centro de costos (opcional)", centros)
    else:
        st.warning("🔒 Tu plan no permite filtrar por centro de costos. Se analizarán todos.")
        centro = "TODOS"

    # --- ESTADO COMPLETO PARA ANÁLISIS AVANZADO ---
    if "estado_todos" not in st.session_state or st.session_state.get("año_actual") != año:
        st.session_state.estado_todos = generar_estado_resultados_todos_los_meses(
            df_datos, df_clasificacion, ruta_parametros)
        st.session_state.año_actual = año

    df_kpis_filtrados = filtrar_kpis_por_plan(df_kpis_param, plan_seleccionado, ruta_parametros)

    df_estado, df_kpis_tarjeta = generar_estado_resultados_detallado(df_datos, df_clasificacion, df_tarjetas, año, mes,
                                                                     df_kpis_filtrados, centro)

    print("df_estado")
    print(df_estado)

    df_estado["AÑO"] = año
    df_estado["MES"] = mes

    # --- TARJETAS DE KPI ---
    if config_plan.get("TARJETAS_KPI", 0):
        st.markdown("### 📌 Indicadores Financieros Clave", unsafe_allow_html=True)
        if not df_kpis_tarjeta.empty:
            col1, col2, col3, col4 = st.columns(4)
            columnas = [col1, col2, col3, col4]
            for idx, (_, row) in enumerate(df_kpis_tarjeta.iterrows()):
                mensual = row["MENSUAL"]
                anual = row["ANUAL"]
                tipo = str(row.get("TIPO_DATO", "MONEDA")).upper()

                if tipo == "PORCENTAJE":
                    valor_mensual = f"{mensual:,.2f}%"
                    valor_anual = f"{anual:,.2f}%"
                elif tipo == "DECIMAL":
                    valor_mensual = f"{mensual:,.2f}"
                    valor_anual = f"{anual:,.2f}"
                else:
                    valor_mensual = f"$ {mensual:,.0f}"
                    valor_anual = f"$ {anual:,.0f}"

                columnas[idx % 4].markdown(
                    f"""
                    <div style='background-color:#f8f9fa; padding:15px; border-radius:10px;
                                box-shadow: 2px 2px 6px rgba(0,0,0,0.05); margin-bottom:10px'>
                        <h5 style='margin-bottom:0px;'>{row['GRUPO']}</h5>
                        <h2 style='margin:5px 0; color:#0066cc'>{valor_mensual}</h2>
                        <p style='margin:0; font-size:16px; color:#2e8b57; font-weight:600'>
                            📈 Acumulado: {valor_anual}
                        </p>
                    </div>
                    """, unsafe_allow_html=True
                )

    # --- VISTA PREVIA DE KPI BLOQUEADOS 🔒 ---
    df_tarjetas = pd.read_excel(ruta_parametros, sheet_name="TARJETAS")
    df_tarjetas.columns = df_tarjetas.columns.str.strip().str.upper()

    if plan_seleccionado.upper() in df_tarjetas.columns:
        kpis_bloqueados = df_tarjetas[df_tarjetas[plan_seleccionado.upper()] != 1]["KPI"].tolist()

        if kpis_bloqueados:
            st.markdown("### 🔒 Indicadores disponibles en planes superiores")
            for kpi in kpis_bloqueados:
                st.markdown(
                    f"<div style='color:gray; padding:5px; margin-left:10px;'>🔒 {kpi}</div>",
                    unsafe_allow_html=True
                )

    # --- ANÁLISIS EN LENGUAJE NATURAL ---
    if config_plan.get("ANALISIS_LENGUAJE", 0):
        st.markdown("---", unsafe_allow_html=True)
        st.markdown("### 👀 Análisis en Lenguaje Natural", unsafe_allow_html=True)
        st.markdown(generar_conclusiones(df_estado), unsafe_allow_html=True)

    # --- ANÁLISIS AVANZADO ---
    if config_plan.get("ANALISIS_AVANZADO", 0):
        st.markdown("### 🚀 Análisis Avanzado")
        df_comparativo, resumen_avanzado = generar_conclusiones_avanzadas(df_estado,
                                                                          st.session_state.estado_todos,
                                                                          ruta_parametros,
                                                                          año, mes)
        st.markdown(generar_tabla_comparativa_html(df_comparativo), unsafe_allow_html=True)
        st.markdown(resumen_avanzado, unsafe_allow_html=True)

    # --- ESTADO DE RESULTADOS ANUAL ---
    if config_plan.get("PG_ANUAL", 0):
        try:
            df_pg_anual = generar_estado_resultados_anual(
                st.session_state.estado_todos,
                df_clasificacion,
                df_kpis_param,
                año,
                centro if centro != "TODOS" else None
            )
            with st.container():
                st.markdown("## 📊 Estado de Resultados Anual (Enero a Diciembre)", unsafe_allow_html=True)

                # html = generar_html_estado_resultados_anual(df_pg_anual)
                # st.markdown(html, unsafe_allow_html=True)
                html = generar_html_estado_resultados_anual(df_pg_anual, kpi_destacados=kpis_para_resaltar)
                st.markdown(html, unsafe_allow_html=True)



        except Exception as e:
            st.error(f"⚠️ Error al generar el Estado de Resultados Anual: {e}")

    # --- ESTADO DE RESULTADOS DETALLADO ---
    st.markdown("---", unsafe_allow_html=True)
    st.markdown("### 📜 Estado de Resultados Detallado", unsafe_allow_html=True)
    st.markdown(generar_html_estado_resultados(df_estado, df_kpis_filtrados), unsafe_allow_html=True)

    # --- EXPORTAR ---
    st.markdown("---")
    st.markdown("### 📂 Exportar Reporte")

    col_export1, col_export2 = st.columns(2)
    if config_plan.get("EXPORTAR_EXCEL", 1):
        with col_export1:
            if st.button("📤 Exportar a Excel"):
                exportar_excel(df_estado, df_kpis_filtrados, año, mes)
                st.success("Reporte Excel exportado correctamente")

    if config_plan.get("EXPORTAR_PDF", 0):
        with col_export2:
            if st.button("📄 Exportar a PDF"):
                exportar_pdf(df_estado, df_kpis_filtrados, año, mes)
                st.success("Reporte PDF generado correctamente")

    # --- GRAFICAS  ---
    if config_plan.get("GRAFICAS", 0):
        st.markdown("---", unsafe_allow_html=True)
        df_graficas = obtener_graficas_por_plan(plan_seleccionado, df_graficas)

        st.markdown("### 👀 Análisis Gráfico", unsafe_allow_html=True)

        ## GRAFICOS ANUALES
        df_para_graficas = df_pg_anual
        df_graficas["MODO"] = df_graficas["MODO"].str.upper()
        df_graficas_anual = df_graficas[df_graficas["MODO"].str.upper() == "ANUAL"]

        ##for graf in df_graficas_anual:
        for _, fila in df_graficas_anual.iterrows():
            try:
                graf = fila.to_dict()  # Para poder usar .get()
                kpi = graf["KPI"]
                tipo = graf["TIPO"]
                descripcion = graf.get("DESCRIPCION", kpi)
                tipo_dato = graf.get("TIPO_DATO", "MONEDA")
                texto_extra = graf.get("COLUMNA_TEXTO_EXTRA", None)

                st.markdown(f"#### 📊 {descripcion}", unsafe_allow_html=True)

                fig = grafico_generico(df_para_graficas, kpi, tipo, "ANUAL", tipo_dato, texto_extra)
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"No se pudo generar la gráfica de {graf.get('KPI')}: {e}")

        # # === GRAFICOS MENSUALES ===
        st.markdown("## 📊 Análisis Gráfico Mensual", unsafe_allow_html=True)

        df_graficas_mensual = df_graficas[df_graficas["MODO"].str.upper() == "MENSUAL"]
        df_mensual = preparar_df_mensual(df_datos, df_clasificacion, año, mes, centro)

        graficos_mensuales = []
        for _, fila in df_graficas_mensual.iterrows():
            graf = fila.to_dict()
            kpi = graf["KPI"]
            tipo_grafico = graf["TIPO"]
            descripcion = graf.get("DESCRIPCION", kpi)
            tipo_dato = graf.get("TIPO_DATO", "MONEDA")
            texto_extra = graf.get("COLUMNA_TEXTO_EXTRA", None)

            try:
                fig = grafico_participacion_mensual(df_mensual, kpi, tipo_grafico, tipo_dato, texto_extra)
                img_bytes = exportar_grafico_plotly(fig, formato="png")
                graficos_mensuales.append((descripcion, fig, img_bytes))
            except Exception as e:
                st.warning(f"No se pudo generar la gráfica de participación de {descripcion}: {e}")

        # Mostrar en filas de dos columnas
        for i in range(0, len(graficos_mensuales), 2):
            cols = st.columns(2)
            for idx, (descripcion, fig, img_bytes) in enumerate(graficos_mensuales[i:i+2]):
                col = cols[idx]
                col.markdown(f"<h4 style='color:black;'>📊 {descripcion}</h4>", unsafe_allow_html=True)
                col.plotly_chart(fig, use_container_width=True)
                col.download_button(
                    label="📥 Descargar PNG",
                    data=img_bytes,
                    file_name=f"grafico_{descripcion.replace(' ', '_')}.png",
                    mime="image/png"
                )

        from openai import OpenAI
        load_dotenv()
        client = OpenAI()  #

        # --- 🔍 ANÁLISIS AUTOMÁTICO CON GPT SI APLICA ---
        if config.get("Conclusiones mensuales", False):
            frases_auto = analizar_mes_anual(df_estado, df_mensual, df_pg_anual,
                                             plan_seleccionado, config)
            st.markdown("---", unsafe_allow_html=True)
            st.markdown("### 🤖 Conclusiones automáticas", unsafe_allow_html=True)
            for f in frases_auto:
                st.markdown(f"- {f}", unsafe_allow_html=True)

