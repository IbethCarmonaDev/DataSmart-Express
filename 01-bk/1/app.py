# Funcion creada para generar el FrontEnd, la presentación hacia el usuario
# Creada por: Ibeth Carmona - IA
# Fecha de Creación: Junio 7-2025
# All rights reserved

import streamlit as st
import pandas as pd
from analisis_estado_resultados import generar_estado_resultados_detallado
from analisis_lenguaje import generar_conclusiones
from analisis_avanzado import generar_conclusiones_avanzadas
from PIL import Image

st.set_page_config(page_title="DataSmart Express", layout="wide")

# Mostrar logo si existe
try:
    logo = Image.open("Logo.png")
    st.image(logo, width=200)
except:
    st.write("")

st.markdown("## 📈 DataSmart Express")
st.markdown("_Estado de Resultados Inteligente con KPIs Financieros_")

archivo_datos = st.file_uploader("🗅️ Carga el archivo de datos", type=["xlsx"])
archivo_parametros = st.file_uploader("⚙️ Carga el archivo de parámetros", type=["xlsx"])

if archivo_datos and archivo_parametros:
    df_datos = pd.read_excel(archivo_datos, sheet_name=0)
    df_parametros = archivo_parametros

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

    st.markdown("### 📌 Indicadores Financieros Clave")
    df_estado, df_kpis = generar_estado_resultados_detallado(df_datos, df_parametros, año, mes, centro)

    try:
        from analisis_estado_resultados import generar_estado_resultados_todos_los_meses
        df_estado_todos = generar_estado_resultados_todos_los_meses(df_datos, df_parametros, centro)
    except ImportError:
        st.error("❌ No se encontró la función 'generar_estado_resultados_todos_los_meses'. Asegúrate de que está definida en 'analisis_estado_resultados.py'")
        st.stop()

    st.write("✅ df_estado generado:", df_estado.head(10))
    st.write("🕢 Filas:", len(df_estado))

    df_estado["AÑO"] = año
    df_estado["MES"] = mes

    df_estado["GRUPO"] = df_estado["GRUPO"].astype(str).str.strip()
    df_kpis["GRUPO"] = df_kpis["GRUPO"].astype(str).str.strip()

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
                color_acumulado = "#2e8b57"
            elif tipo == "DECIMAL":
                valor_mensual = f"{mensual:,.2f}"
                valor_anual = f"{anual:,.2f}"
                color_acumulado = "#2e8b57"
            else:
                valor_mensual = f"$ {mensual:,.0f}"
                valor_anual = f"$ {anual:,.0f}"
                color_acumulado = "#2e8b57"

            columnas[idx % 4].markdown(
                f"""
                <div style='background-color:#f8f9fa; padding:15px; border-radius:10px;
                            box-shadow: 2px 2px 6px rgba(0,0,0,0.05); margin-bottom:10px'>
                    <h5 style='margin-bottom:0px;'>{row['GRUPO']}</h5>
                    <h2 style='margin:5px 0; color:#0066cc'>{valor_mensual}</h2>
                    <p style='margin:0; font-size:16px; color:{color_acumulado}; font-weight:600'>
                        📈 Acumulado: {valor_anual}
                    </p>
                </div>
                """, unsafe_allow_html=True
            )

    st.markdown("---")
    st.markdown("### 👀 Análisis en Lenguaje Natural")
    resumen = generar_conclusiones(df_kpis)
    st.markdown(resumen)

    st.markdown("### 🚀 Análisis Avanzado (Demo)")
    df_comparativo, resumen_avanzado = generar_conclusiones_avanzadas(df_kpis, df_estado_todos, archivo_parametros, año, mes)

    st.write("**KPIs hoja TARJETAS:**", df_kpis["GRUPO"].unique().tolist())
    st.write("**KPIs disponibles en df_estado:**", df_estado["GRUPO"].unique().tolist())

    st.dataframe(df_comparativo, use_container_width=True)
    st.markdown(resumen_avanzado)

    kpis_tarjeta = set(df_kpis["GRUPO"].unique())
    kpis_estado = set(df_estado["GRUPO"].unique())
    kpis_validos = sorted(kpis_tarjeta.intersection(kpis_estado))
    st.write("**KPIs válidos encontrados para análisis avanzado:**", kpis_validos)
    st.write(f"Cantidad de KPIs válidos: {len(kpis_validos)}")

    st.write("\n---\n### 🔧 DEPURACIÓN AVANZADA")
    st.write("df_estado ejemplo:", df_estado.head(3))
    st.write("df_kpis ejemplo:", df_kpis.head(3))
    st.write("Año seleccionado:", año)
    st.write("Mes seleccionado:", mes)

    mes_anterior = 12 if mes == 1 else mes - 1
    año_anterior = año - 1 if mes == 1 else año
    df_mes_anterior = df_estado_todos[(df_estado_todos["AÑO"] == año_anterior) & (df_estado_todos["MES"] == mes_anterior)]
    st.write(f"\n📅 Datos mes anterior ({mes_anterior}/{año_anterior}):", df_mes_anterior.head(10))

    st.markdown("---")
    st.markdown("### 📜 Estado de Resultados Detallado")
    def aplicar_formato(df, df_kpis_tarjeta):
        tipo_kpis = {row["GRUPO"]: str(row.get("TIPO_DATO", "MONEDA")).upper() for _, row in df_kpis_tarjeta.iterrows()}
        def formatear(valor, grupo):
            tipo = tipo_kpis.get(grupo, "MONEDA")
            if pd.isnull(valor):
                return ""
            if tipo == "PORCENTAJE":
                return f"{valor:.2f}%"
            elif tipo == "DECIMAL":
                return f"{valor:.2f}"
            else:
                return f"${valor:,.0f}"
        df_formateado = df.copy()
        for col in ["MENSUAL", "ANUAL"]:
            df_formateado[col] = df_formateado.apply(lambda row: formatear(row[col], row["GRUPO"]), axis=1)
        return df_formateado

    df_estado_formateado = aplicar_formato(df_estado, df_kpis)
    st.dataframe(df_estado_formateado, use_container_width=True)
