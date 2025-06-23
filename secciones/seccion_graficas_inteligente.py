
import streamlit as st
from core.planes import obtener_graficas_por_plan
from presentacion.graficas import grafico_generico, grafico_participacion_mensual
from core.comentarios import generar_comentario_logico_anual, generar_comentario_gpt
from presentacion.mostrar_analisis_gpt_visual import mostrar_analisis_gpt_visual

import pandas as pd

def mostrar_graficas(df_graficas, df_pg_anual, df_mensual, plan, usar_gpt_graficas, año=None, mes_nombre=None):
    st.markdown("## 📈 Análisis Gráfico")
    df_graficas_plan = obtener_graficas_por_plan(plan, df_graficas)

    try:
        df_comentarios = pd.read_excel("data/Parametros.xlsx", sheet_name="COMENTARIOS_GRAFICAS", index_col=0)
        df_comentarios.columns = df_comentarios.columns.str.upper().str.strip()
        plan_mayus = plan.upper()

        permitido_py = df_comentarios.loc["Comentario Python", plan_mayus] == 1
        permitido_gpt = df_comentarios.loc["Comentario GPT", plan_mayus] == 1

    except Exception as e:
        st.warning("No se pudo cargar la hoja COMENTARIOS_GRAFICAS.")
        permitido_py = permitido_gpt = False

    if año and mes_nombre:
        st.markdown(f"📅 <b>Periodo seleccionado:</b> {mes_nombre} {año}", unsafe_allow_html=True)

    for _, fila in df_graficas_plan.iterrows():
        try:
            modo = fila["MODO"].upper()
            kpi_nombre = fila["KPI"]
            titulo = f"{kpi_nombre} - {año}" if modo == "ANUAL" else f"{kpi_nombre} - {mes_nombre} {año}"

            if modo == "ANUAL":
                fig = grafico_generico(df_pg_anual, kpi_nombre, fila["TIPO"], modo,
                                       fila.get("TIPO_DATO", "MONEDA"), fila.get("COLUMNA_TEXTO_EXTRA"))
                st.plotly_chart(fig, use_container_width=True)

                # Comentarios inteligentes ANUAL
                if permitido_py:
                    comentarios = generar_comentario_logico_anual(df_pg_anual, kpi_nombre, mes_actual=mes_nombre, anio_actual=año)
                    for frase in comentarios:
                        st.markdown(f"🧠 <i>{frase}</i>", unsafe_allow_html=True)

                if permitido_gpt and usar_gpt_graficas:
                    comentario = generar_comentario_gpt(df_pg_anual, kpi_nombre, modo="ANUAL", ubicacion=kpi_nombre)

                    if comentario:
                        # st.markdown(f"💬 <i>{comentario}</i>", unsafe_allow_html=True)
                        # st.write(comentario)
                        mostrar_analisis_gpt_visual(kpi_nombre, comentario)


                if not usar_gpt_graficas:
                    st.info("🔌 Comentario Inteligente desactivado por el usuario.")

            else:
                fig = grafico_participacion_mensual(df_mensual, kpi_nombre, fila["TIPO"],
                                                    fila.get("TIPO_DATO", "MONEDA"), fila.get("COLUMNA_TEXTO_EXTRA"))
                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.warning(f"No se pudo generar la gráfica de {fila['KPI']}: {e}")


