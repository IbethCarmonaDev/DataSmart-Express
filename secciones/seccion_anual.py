
import streamlit as st
from presentacion.analisis_presentacion import generar_html_estado_resultados_anual

def mostrar_anual(df_pg_anual, kpis_para_resaltar):
    st.markdown("### 📊 Estado de Resultados Anual")
    html = generar_html_estado_resultados_anual(df_pg_anual, kpi_destacados=kpis_para_resaltar)
    st.markdown(html, unsafe_allow_html=True)
