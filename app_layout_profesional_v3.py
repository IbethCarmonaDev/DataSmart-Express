import streamlit as st
from streamlit_option_menu import option_menu

def main():
    st.set_page_config(layout="wide", page_title="DataSmart Express")

    # Espaciador lateral (centrar contenido)
    left, center, right = st.columns([1, 10, 1])
    with center:

        # --- MENÚ SUPERIOR HORIZONTAL (Planes, Perfil) ---
        seleccion_superior = option_menu(
            menu_title="", 
            options=["Inicio", "Planes", "Perfil", "Cerrar sesión"],
            icons=["house", "list-columns", "person", "box-arrow-right"],
            orientation="horizontal",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#f0f2f6"},
                "icon": {"color": "#0d6efd", "font-size": "14px"},
                "nav-link": {"font-size": "14px", "margin":"0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#0d6efd", "color": "white"},
            }
        )

        # --- ENCABEZADO SUPERIOR ---
        col1, col2, col3 = st.columns([1, 6, 3])
        with col1:
            try:
                st.image("logo.png", width=300)
            except:
                st.markdown("🧠")
        with col2:
            nombre_usuario = "Ibeth Carmona xx"
            st.markdown(f"<div style='text-align:right; margin-top:16px;'>👤 <strong>{nombre_usuario}</strong></div>", unsafe_allow_html=True)

        st.markdown("---")

        # --- CONTENIDO SEGÚN SELECCIÓN ---
        st.markdown(f"### 🔹 Menú superior: {seleccion_superior}")
        st.markdown(f"### 🔸 Funcionalidad seleccionada: (se verá según implementación)")

    # --- MENÚ LATERAL DE FUNCIONALIDAD ---
    with st.sidebar:
        seleccion_lateral = option_menu(
            menu_title="",
            options=["Estado de Resultados", "KPIs", "Análisis", "Exportar"],
            icons=["bar-chart", "activity", "eye", "cloud-upload"],
            default_index=0,
            orientation="vertical",
            styles={
                "container": {"padding": "5px", "background-color": "#f8f9fa"},
                "icon": {"color": "#0d6efd", "font-size": "14px"},
                "nav-link": {"font-size": "14px", "text-align": "left", "margin": "5px"},
                "nav-link-selected": {"background-color": "#0d6efd", "color": "white"},
            }
        )

if __name__ == "__main__":
    main()