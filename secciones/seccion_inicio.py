import streamlit as st

def mostrar_inicio(usuario, plan_actual):
    st.markdown("# 👋 Te damos la bienvenida a DataSmart Express")

    # st.markdown(f"""
    # Tu plataforma para visualizar y analizar estados financieros de forma inteligente.
    # #### 🎉 ¡Hola, {usuario}!
    # """)

    st.markdown(f"""    
    Tu plataforma para visualizar y analizar estados financieros de forma inteligente.    
    """)

    # # Aviso de plan Free
    # if plan_actual == "Free":
    #     st.warning("⚠️ Tu período de prueba ha finalizado. Ahora estás en el plan **Free**.\n\nAlgunas funcionalidades estarán limitadas.")


    st.markdown("""
    ---
    ### 🚀 Pasos para comenzar:
    1. 🧾 **Carga tu archivo contable**
    2. 📅 **Selecciona el año y mes**
    3. 📊 **Explora las secciones:** Detallado, KPIs, Análisis, Gráficas y Exportar
    """)

    st.markdown("---")
    st.markdown("#### 📁 Arrastra tu archivo contable aquí:")
    st.caption("Límite 200MB por archivo • Formato: `.xlsx`")

    # Aquí insertas el uploader real
    archivo = st.file_uploader("Drag and drop file", type=["xlsx"], label_visibility="collapsed")

    return archivo


def OLDmostrar_inicio(archivo_usuario=None):
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
