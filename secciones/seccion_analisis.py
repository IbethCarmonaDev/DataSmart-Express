
import streamlit as st
from core.analisis_lenguaje import generar_conclusiones
from core.analisis_avanzado import generar_conclusiones_avanzadas, generar_tabla_comparativa_html
from core.analisis_mes_anual import analizar_mes_anual

def mostrar_analisis(df_estado, estados, ruta_parametros, año, mes, config_plan, df_pg_anual, df_mensual, plan, config):
    if config_plan.get("ANALISIS_LENGUAJE", 0):
        st.markdown("### 👀 Análisis en Lenguaje Natural")
        st.markdown(generar_conclusiones(df_estado), unsafe_allow_html=True)

    if config_plan.get("ANALISIS_AVANZADO", 0):
        st.markdown("### 🚀 Análisis Avanzado")
        df_comp, resumen = generar_conclusiones_avanzadas(df_estado, estados, ruta_parametros, año, mes)
        st.markdown(generar_tabla_comparativa_html(df_comp), unsafe_allow_html=True)
        st.markdown(resumen, unsafe_allow_html=True)

    # if config.get("Conclusiones mensuales", False):
    #     st.markdown("### 🤖 Conclusiones automáticas (GPT)")
    #     frases_auto = analizar_mes_anual(df_estado, df_mensual, df_pg_anual, plan, config)
    #     for f in frases_auto:
    #         st.markdown(f"- {f}", unsafe_allow_html=True)
