import streamlit as st
from PIL import Image

def mostrar_layout(nombre_usuario: str, plan_usuario: str):
    st.markdown(
        """
        <style>
        .top-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.5rem 1rem;
            background-color: #f8f9fa;
            border-bottom: 1px solid #ddd;
        }
        .top-bar-left {
            display: flex;
            align-items: center;
        }
        .top-bar-left img {
            height: 50px;
            margin-right: 10px;
        }
        .top-bar-right {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        .top-bar-right span {
            font-weight: bold;
            color: #4B0082;
        }
        .nav-button {
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            background-color: #e9ecef;
            border: none;
            font-size: 0.9rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Logo (usa tu archivo actual o reemplaza la ruta si lo tienes en otra carpeta)
    logo = Image.open("Logo.png")
    # st.image(logo, width=150)

    # Barra superior en columnas
    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(logo, width=150)

    with col2:
        st.markdown(f"""
            <div class='top-bar-right'>
                👤 <span>{nombre_usuario}</span> | 📄 Plan: <span>{plan_usuario}</span> &nbsp;&nbsp;
                <button class='nav-button'>Inicio</button>
                <button class='nav-button'>Planes</button>
                <button class='nav-button'>Perfil</button>
                <button class='nav-button'>Cerrar sesión</button>
            </div>
        """, unsafe_allow_html=True)

# import streamlit as st
# from PIL import Image
# from streamlit_option_menu import option_menu
#
# def mostrar_layout(nombre_usuario: str, plan_usuario: str):
#     # --- Encabezado superior ---
#     col1, col2, col3 = st.columns([1, 5, 2])
#     with col1:
#         try:
#             logo = Image.open("Logo.png")
#             st.image(logo, width=120)
#         except:
#             st.markdown("🧠")
#     with col2:
#         st.markdown(
#             f"<h4 style='margin-top:18px; color:#004080;'>DataSmart Express</h4>",
#             unsafe_allow_html=True
#         )
#
#     with col3:
#         st.markdown(
#             f"<div style='text-align:right; margin-top:22px;'>👤 <strong>{nombre_usuario}</strong><br>🧾 Plan: <strong>{plan_usuario}</strong></div>",
#             unsafe_allow_html=True
#         )
#
#     st.markdown("<hr style='margin-top:0;'>", unsafe_allow_html=True)
#
#     # --- Menú superior horizontal (puede ajustarse a futuro) ---
#     seleccion_superior = option_menu(
#         menu_title="",
#         options=["Inicio", "Planes", "Perfil", "Cerrar sesión"],
#         icons=["house", "list-columns", "person", "box-arrow-right"],
#         orientation="horizontal",
#         default_index=0,
#         styles={
#             "container": {"padding": "0!important", "background-color": "#f0f2f6"},
#             "icon": {"color": "#0d6efd", "font-size": "16px"},
#             "nav-link": {"font-size": "14px", "margin":"0px", "--hover-color": "#eee"},
#             "nav-link-selected": {"background-color": "#0d6efd", "color": "white"},
#         }
#     )
#     return seleccion_superior