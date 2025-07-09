
import streamlit as st

def mostrar_inicio(archivo_usuario=None):
    st.subheader("👋 Bienvenido a DataSmart Express")
    usuario = st.session_state["usuario"]
    plan = usuario.get("plan_actual")
    st.markdown(f"👤 Usuario: **{usuario['nombre']}** | Plan: **{plan}**")

    st.markdown("📘 Sigue estos pasos para comenzar:")

    st.markdown("""
    1. 📂 **Carga tu archivo contable**
    2. 📅 Selecciona el año y mes
    3. 📊 Explora las secciones: Detallado, Anual, KPIs, Análisis, Gráficas y Exportar
    """)

    st.divider()

    archivo_nuevo = st.file_uploader("📂 Sube tu archivo con datos contables y clasificación de cuentas", type=["xlsx"])

    if archivo_nuevo:
        return archivo_nuevo
    else:
        return archivo_usuario
