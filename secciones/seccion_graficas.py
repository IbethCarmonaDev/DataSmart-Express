
import streamlit as st
from core.planes import obtener_graficas_por_plan
from presentacion.graficas import grafico_generico, grafico_participacion_mensual

def mostrar_graficas(df_graficas, df_pg_anual, df_mensual, plan, año=None, mes_nombre=None):
    st.markdown("## 📈 Análisis Gráfico")
    df_graficas_plan = obtener_graficas_por_plan(plan, df_graficas)

    if año and mes_nombre:
        st.markdown(f"📅 <b>Periodo seleccionado:</b> {mes_nombre} {año}", unsafe_allow_html=True)

    for _, fila in df_graficas_plan.iterrows():
        try:
            modo = fila["MODO"].upper()
            titulo = f"{fila['KPI']} - {año}" if modo == "ANUAL" else f"{fila['KPI']} - {mes_nombre} {año}"
            if modo == "ANUAL":
                fig = grafico_generico(df_pg_anual, fila["KPI"], fila["TIPO"], modo,
                                       fila.get("TIPO_DATO", "MONEDA"), fila.get("COLUMNA_TEXTO_EXTRA"))
            else:
                fig = grafico_participacion_mensual(df_mensual, fila["KPI"], fila["TIPO"],
                                                    fila.get("TIPO_DATO", "MONEDA"), fila.get("COLUMNA_TEXTO_EXTRA"))
            fig.update_layout(title=titulo)
            fig.add_annotation(
                text="Solo se muestran meses con datos diferentes de cero",
                showarrow=False,
                xref="paper", yref="paper",
                x=0, y=1.08,
                font=dict(size=11, color="gray")
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"No se pudo generar la gráfica de {fila['KPI']}: {e}")
