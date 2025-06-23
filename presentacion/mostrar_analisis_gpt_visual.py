
import streamlit as st

def mostrar_analisis_gpt_visual(kpi_nombre, comentario):
    with st.expander(f"🧠 Análisis ejecutivo para {kpi_nombre.title()}"):
        st.markdown(
            f'''
            <div style="
                background-color: #f9f9f9;
                padding: 1.2rem;
                border-left: 6px solid #4a90e2;
                border-radius: 0.5rem;
                box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.05);
                font-size: 1rem;
                line-height: 1.6;
                color: #333;">
                {comentario}
            </div>
            ''',
            unsafe_allow_html=True
        )
