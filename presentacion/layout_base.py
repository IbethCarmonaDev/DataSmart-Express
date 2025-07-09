import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu

def mostrar_layout(nombre_usuario: str, plan_usuario: str):
    # --- Encabezado superior ---
    col1, col2, col3 = st.columns([1, 5, 2])
    with col1:
        try:
            logo = Image.open("Logo.png")
            st.image(logo, width=120)
        except:
            st.markdown("🧠")
    with col2:
        st.markdown(
            f"<h4 style='margin-top:18px; color:#004080;'>DataSmart Express</h4>",
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f"<div style='text-align:right; margin-top:22px;'>👤 <strong>{nombre_usuario}</strong><br>🧾 Plan: <strong>{plan_usuario}</strong></div>",
            unsafe_allow_html=True
        )

    st.markdown("<hr style='margin-top:0;'>", unsafe_allow_html=True)

    # --- Menú superior horizontal (puede ajustarse a futuro) ---
    seleccion_superior = option_menu(
        menu_title="",
        options=["Inicio", "Planes", "Perfil", "Cerrar sesión"],
        icons=["house", "list-columns", "person", "box-arrow-right"],
        orientation="horizontal",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#f0f2f6"},
            "icon": {"color": "#0d6efd", "font-size": "16px"},
            "nav-link": {"font-size": "14px", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#0d6efd", "color": "white"},
        }
    )
    return seleccion_superior