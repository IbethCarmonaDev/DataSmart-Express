
import streamlit as st
from presentacion.exportacion import exportar_excel, exportar_pdf

def mostrar_exportacion(df_estado, df_kpis_filtrados, año, mes, config_plan):
    col1, col2 = st.columns(2)
    with col1:
        if config_plan.get("EXPORTAR_EXCEL", 1) and st.button("📤 Exportar a Excel"):
            exportar_excel(df_estado, df_kpis_filtrados, año, mes)
            st.success("Excel exportado correctamente")
    with col2:
        if config_plan.get("EXPORTAR_PDF", 0) and st.button("📄 Exportar a PDF"):
            exportar_pdf(df_estado, df_kpis_filtrados, año, mes)
            st.success("PDF generado correctamente")
