import streamlit as st
from PIL import Image
import base64
from io import BytesIO

def cambiar_pagina(pagina: str):
    st.session_state["pagina_actual"] = pagina

def image_to_base64(image):
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return img_str

def mostrar_layout(nombre_usuario: str, plan_usuario: str):
    logo = Image.open("Logo.png")
    logo_base64 = image_to_base64(logo)

    # CSS sticky + estilos
    st.markdown("""
        <style>
        .sticky-header {
            position: sticky;
            top: 0;
            z-index: 999;
            background-color: #ffffff;
            padding: 0.5rem 1rem;
            border-bottom: 1px solid #ccc;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .usuario-info {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .usuario-texto {
            display: flex;
            flex-direction: column;
            font-size: 1rem;
        }
        .usuario-texto span:first-child {
            font-weight: bold;
            color: #4B0082;
        }
        .botones {
            display: flex;
            gap: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Layout con columnas para mantener el diseño y botones funcionales
    st.markdown(f"""
        <div class="sticky-header">
            <div class="usuario-info">
                <img src="data:image/png;base64,{logo_base64}" width="70"/>
                <div class="usuario-texto">
                    <span>👤 {nombre_usuario}</span>
                    <span>📄 Plan: {plan_usuario}</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        if st.button("🏠 Inicio"):
            cambiar_pagina("Inicio")
    with col2:
        if st.button("💼 Planes"):
            cambiar_pagina("Planes")
    with col3:
        if st.button("👤 Perfil"):
            cambiar_pagina("Perfil")
    with col4:
        if st.button("🚪 Cerrar sesión"):
            cambiar_pagina("Salir")


# import streamlit as st
# from PIL import Image
#
# def cambiar_pagina(pagina: str):
#     st.session_state["pagina_actual"] = pagina
#
# def mostrar_layout(nombre_usuario: str, plan_usuario: str):
#     logo = Image.open("Logo.png")
#     col1, col2, col3 = st.columns([1, 6, 4])
#
#     with col1:
#         st.image(logo, width=90)
#
#     with col2:
#         st.markdown(f"""
#             <div style='display: flex; flex-direction: column; justify-content: center; height: 100%;'>
#                 <span style='font-weight: bold; font-size: 1.1rem; color: #4B0082;'>👤 {nombre_usuario}</span>
#                 <span style='font-weight: bold; font-size: 1.1rem; color: #4B0082;'>📄 Plan: {plan_usuario}</span>
#             </div>
#         """, unsafe_allow_html=True)
#
#     with col3:
#         st.button("Inicio", on_click=cambiar_pagina, args=("Inicio",))
#         st.button("Planes", on_click=cambiar_pagina, args=("Planes",))
#         st.button("Perfil", on_click=cambiar_pagina, args=("Perfil",))
#         st.button("Cerrar sesión", on_click=cambiar_pagina, args=("Salir",))
