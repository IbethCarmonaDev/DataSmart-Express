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
    st.markdown("#### 📁 Carga tu archivo contable aquí:")
    st.caption("Límite 200MB por archivo • Formato: `.xlsx`")

    # Aquí insertas el uploader real
    archivo = st.file_uploader("Drag and drop file", type=["xlsx"], label_visibility="collapsed")

    return archivo

