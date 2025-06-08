import streamlit as st
import pandas as pd
from PIL import Image

# --- NUEVAS RUTAS DE IMPORTACIÓN ---
from core.analisis_estado_resultados import generar_estado_resultados_detallado, generar_estado_resultados_todos_los_meses
from core.analisis_lenguaje import generar_conclusiones
from core.analisis_avanzado import generar_conclusiones_avanzadas, generar_tabla_comparativa_html
from presentacion.analisis_presentacion import generar_html_estado_resultados

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="DataSmart Express", layout="wide")

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

if archivo_usuario:
    df_datos = pd.read_excel(archivo_usuario, sheet_name="DATOS_FINANCIEROS")
    df_clasificacion = pd.read_excel(archivo_usuario, sheet_name="CLASIFICACION_CUENTAS")
    df_parametros = ruta_parametros

    año = st.selectbox("1⃣ Selecciona el año", sorted(df_datos["AÑO"].unique(), reverse=True))
    meses = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }
    mes_nombre = st.selectbox("2⃣ Selecciona el mes", list(meses.values()))
    mes = list(meses.keys())[list(meses.values()).index(mes_nombre)]

    centros = ["TODOS"] + sorted(df_datos["CENTRO_COSTOS"].dropna().unique())
    centro = st.selectbox("3⃣ Selecciona centro de costos (opcional)", centros)

    # --- ESTADO COMPLETO PARA ANÁLISIS AVANZADO ---
    if "estado_todos" not in st.session_state or st.session_state.get("año_actual") != año:
        st.session_state.estado_todos = generar_estado_resultados_todos_los_meses(df_datos, df_clasificacion, df_parametros, centro)
        st.session_state.año_actual = año

    df_estado, df_kpis = generar_estado_resultados_detallado(df_datos, df_clasificacion, df_parametros, año, mes, centro)
    df_estado["AÑO"] = año
    df_estado["MES"] = mes

    # --- TARJETAS DE KPI ---
    st.markdown("### 📌 Indicadores Financieros Clave", unsafe_allow_html=True)
    if not df_kpis.empty:
        col1, col2, col3, col4 = st.columns(4)
        columnas = [col1, col2, col3, col4]
        for idx, (_, row) in enumerate(df_kpis.iterrows()):
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

    # --- ANÁLISIS EN LENGUAJE NATURAL ---
    st.markdown("---", unsafe_allow_html=True)
    st.markdown("### 👀 Análisis en Lenguaje Natural", unsafe_allow_html=True)
    st.markdown(generar_conclusiones(df_kpis), unsafe_allow_html=True)

    # --- ANÁLISIS AVANZADO ---
    st.markdown("### 🚀 Análisis Avanzado")
    df_comparativo, resumen_avanzado = generar_conclusiones_avanzadas(df_kpis, st.session_state.estado_todos, df_parametros, año, mes)
    st.markdown(generar_tabla_comparativa_html(df_comparativo), unsafe_allow_html=True)
    st.markdown(resumen_avanzado, unsafe_allow_html=True)

    # --- ESTADO DE RESULTADOS DETALLADO ---
    st.markdown("---", unsafe_allow_html=True)
    st.markdown("### 📜 Estado de Resultados Detallado", unsafe_allow_html=True)
    st.markdown(generar_html_estado_resultados(df_estado, df_kpis), unsafe_allow_html=True)
