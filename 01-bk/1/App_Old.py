import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="DataSmart Express", layout="wide")
st.title("📊 DataSmart Express - Estado de Resultados Inteligente")

from analisis_estado_resultados import generar_estado_resultados_detallado

archivo_excel = st.file_uploader("Sube tu archivo de datos contables (Excel)", type=[".xlsx"])
archivo_parametros = st.file_uploader("Sube el archivo de parámetros financieros (Excel con 2 hojas)", type=[".xlsx"])

if archivo_excel and archivo_parametros:
    try:
        df_datos = pd.read_excel(archivo_excel)
        df_datos.columns = df_datos.columns.str.strip().str.upper()

        # Asegurar que PREFIJO sea string
        df_datos["PREFIJO"] = df_datos["COD_CUENTA"].astype(str).str[:2]

        años = df_datos["AÑO"].dropna().unique()
        año_sel = st.selectbox("Selecciona el año", sorted(años))

        meses = df_datos[df_datos["AÑO"] == año_sel]["MES"].dropna().unique()
        mes_sel = st.selectbox("Selecciona el mes", sorted(meses))

        cc_list = df_datos[df_datos["AÑO"] == año_sel]["CENTRO_COSTOS"].dropna().unique()
        cc_sel = st.selectbox("Selecciona el Centro de Costos (opcional)", ["TODOS"] + sorted(cc_list.tolist()))

        df_resultado = generar_estado_resultados_detallado(df_datos, archivo_parametros, año_sel, mes_sel, cc_sel)

        st.subheader("🧾 Estado de Resultados (Mensual y Acumulado Anual con Detalle por Cuenta)")
        st.dataframe(df_resultado.style.format({"MENSUAL": "$ {:,.0f}", "ANUAL": "$ {:,.0f}"}))

        buffer = BytesIO()
        df_resultado.to_excel(buffer, index=False)
        buffer.seek(0)
        st.download_button(
            label="📥 Descargar Excel",
            data=buffer,
            file_name=f"Estado_Resultados_{año_sel}_{str(mes_sel).zfill(2)}_{cc_sel}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"Ocurrió un error al procesar los archivos: {e}")
