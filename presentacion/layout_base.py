import streamlit as st
from PIL import Image
import base64
from io import BytesIO

def cambiar_pagina(pagina: str):
    st.session_state["pagina_actual"] = pagina

def image_to_base64(image):
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

def mostrar_layout(nombre_usuario: str, plan_usuario: str):
    logo = Image.open("Logo.png")
    logo_base64 = image_to_base64(logo)

    # --- Estilos globales ---
    st.markdown("""
        <style>
        .fixed-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            background-color: white;
            border-bottom: 1px solid #ccc;
            padding: 0.8rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .usuario-info {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .usuario-texto {
            display: flex;
            flex-direction: column;
            font-size: 0.9rem;
        }
        .usuario-texto span:first-child {
            font-weight: bold;
            color: #4B0082;
            font-size: 1.1rem;
        }
        .boton {
            background-color: #f9f9f9;
            border: 1px solid #bbb;
            padding: 6px 14px;
            border-radius: 8px;
            margin-left: 8px;
            font-weight: bold;
            cursor: pointer;
            color: #4B0082;
        }
        .header-placeholder {
            height: 95px;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Header fijo con logo, nombre y botones bonitos ---
    st.markdown(f"""
        <div class="fixed-header">
            <div class="usuario-info">
                <img src="data:image/png;base64,{logo_base64}" width="65">
                <div class="usuario-texto">
                    <span>👤 {nombre_usuario}</span>
                    <span>📄 Plan: {plan_usuario}</span>
                </div>
            </div>
            <div class="botones">
                <form method="post" style="display:inline;">
                    <button name="pagina" value="Inicio" class="boton">🏠 Inicio</button>
                    <button name="pagina" value="Planes" class="boton">💼 Planes</button>
                    <button name="pagina" value="Perfil" class="boton">👤 Perfil</button>
                    <button name="pagina" value="Salir" class="boton">🚪 Cerrar sesión</button>
                </form>
            </div>
        </div>
        <div class="header-placeholder"></div>
    """, unsafe_allow_html=True)

    # Cambiar página según botón presionado
    form_data = st.query_params.get("pagina", None)
    if form_data:
        cambiar_pagina(form_data)

# import streamlit as st
# from PIL import Image
# import base64
# from io import BytesIO
#
# def cambiar_pagina(pagina: str):
#     st.session_state["pagina_actual"] = pagina
#
# def image_to_base64(image):
#     buffer = BytesIO()
#     image.save(buffer, format="PNG")
#     img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
#     return img_str
#
# def mostrar_layout(nombre_usuario: str, plan_usuario: str):
#     logo = Image.open("Logo.png")
#     logo_base64 = image_to_base64(logo)
#
#     # CSS sticky + estilos
#     st.markdown("""
#         <style>
#         .sticky-header {
#             position: sticky;
#             top: 0;
#             z-index: 999;
#             background-color: #ffffff;
#             padding: 0.5rem 1rem;
#             border-bottom: 1px solid #ccc;
#             display: flex;
#             align-items: center;
#             justify-content: space-between;
#         }
#         .usuario-info {
#             display: flex;
#             align-items: center;
#             gap: 15px;
#         }
#         .usuario-texto {
#             display: flex;
#             flex-direction: column;
#             font-size: 1rem;
#         }
#         .usuario-texto span:first-child {
#             font-weight: bold;
#             color: #4B0082;
#         }
#         .botones {
#             display: flex;
#             gap: 10px;
#         }
#         </style>
#     """, unsafe_allow_html=True)
#
#     # Layout con columnas para mantener el diseño y botones funcionales
#     st.markdown(f"""
#         <div class="sticky-header">
#             <div class="usuario-info">
#                 <img src="data:image/png;base64,{logo_base64}" width="70"/>
#                 <div class="usuario-texto">
#                     <span>👤 {nombre_usuario}</span>
#                     <span>📄 Plan: {plan_usuario}</span>
#                 </div>
#             </div>
#         </div>
#     """, unsafe_allow_html=True)
#
#     col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
#
#     with col1:
#         if st.button("🏠 Inicio"):
#             cambiar_pagina("Inicio")
#     with col2:
#         if st.button("💼 Planes"):
#             cambiar_pagina("Planes")
#     with col3:
#         if st.button("👤 Perfil"):
#             cambiar_pagina("Perfil")
#     with col4:
#         if st.button("🚪 Cerrar sesión"):
#             cambiar_pagina("Salir")
#
