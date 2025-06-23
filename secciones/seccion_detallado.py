
import streamlit as st
from presentacion.analisis_presentacion import generar_html_estado_resultados

def mostrar_detallado(df_estado, df_kpis_filtrados):
    st.markdown("### 📜 Estado de Resultados Detallado")
    st.markdown(generar_html_estado_resultados(df_estado, df_kpis_filtrados), unsafe_allow_html=True)
