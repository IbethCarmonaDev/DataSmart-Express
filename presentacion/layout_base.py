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

    pagina_actual = st.session_state.get("pagina_actual", "Inicio")

    st.markdown(f"""
        <style>
        .sticky-header {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 999;
            background-color: white;
            border-bottom: 1px solid #ccc;
            padding: 0.6rem 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 30px;
        }}
        .usuario-info {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        .usuario-texto {{
            display: flex;
            flex-direction: column;
        }}
        .usuario-texto span:first-child {{
            font-weight: bold;
            color: #4B0082;
            font-size: 1.05rem;
        }}
        .botones-nav {{
            display: flex;
            gap: 8px;
        }}
        .boton {{
            border-radius: 6px;
            padding: 6px 12px;
            font-weight: bold;
            border: 1px solid #bbb;
            color: #4B0082;
            background-color: #f8f8f8;
            cursor: pointer;
        }}
        .boton-activo {{
            background-color: #4B0082;
            color: white;
            border: 1px solid #4B0082;
        }}
        .header-placeholder {{
            height: 85px;
        }}
        </style>

        <div class="sticky-header">
            <div class="usuario-info">
                <img src="data:image/png;base64,{logo_base64}" width="60">
                <div class="usuario-texto">
                    <span>👤 {nombre_usuario}</span>
                    <span>📄 Plan: {plan_usuario}</span>
                </div>
            </div>
            <div class="botones-nav">
                <form method="get">
                    <button name="pagina" value="Inicio" class="boton {'boton-activo' if pagina_actual == 'Inicio' else ''}">🏠 Inicio</button>
                    <button name="pagina" value="Planes" class="boton {'boton-activo' if pagina_actual == 'Planes' else ''}">💼 Planes</button>
                    <button name="pagina" value="Perfil" class="boton {'boton-activo' if pagina_actual == 'Perfil' else ''}">👤 Perfil</button>
                    <button name="pagina" value="Salir" class="boton {'boton-activo' if pagina_actual == 'Salir' else ''}">🚪 Cerrar sesión</button>
                </form>
            </div>
        </div>
        <div class="header-placeholder"></div>
    """, unsafe_allow_html=True)

    # Captura de navegación
    pagina = st.query_params.get("pagina", None)
    if pagina:
        cambiar_pagina(pagina)


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
#     return base64.b64encode(buffer.getvalue()).decode()
#
# def mostrar_layout(nombre_usuario: str, plan_usuario: str):
#     logo = Image.open("Logo.png")
#     logo_base64 = image_to_base64(logo)
#
#     pagina_actual = st.session_state.get("pagina_actual", "Inicio")
#
#     # Estilos para header fijo + botones
#     st.markdown(f"""
#         <style>
#         .fixed-header {{
#             position: fixed;
#             top: 0;
#             left: 0;
#             right: 0;
#             z-index: 1000;
#             background-color: white;
#             border-bottom: 1px solid #ccc;
#             padding: 0.8rem 2rem;
#             display: flex;
#             justify-content: space-between;
#             align-items: center;
#         }}
#         .usuario-info {{
#             display: flex;
#             align-items: center;
#             gap: 15px;
#         }}
#         .usuario-texto {{
#             display: flex;
#             flex-direction: column;
#             font-size: 0.9rem;
#         }}
#         .usuario-texto span:first-child {{
#             font-weight: bold;
#             color: #4B0082;
#             font-size: 1.1rem;
#         }}
#         .header-placeholder {{
#             height: 95px;
#         }}
#         .stButton > button {{
#             border-radius: 8px;
#             padding: 6px 14px;
#             font-weight: bold;
#             color: #4B0082;
#             border: 1px solid #bbb;
#             background-color: #f9f9f9;
#         }}
#         .stButton.active > button {{
#             background-color: #4B0082;
#             color: white;
#             border: 1px solid #4B0082;
#         }}
#         </style>
#     """, unsafe_allow_html=True)
#
#     # Header visual
#     st.markdown(f"""
#         <div class="fixed-header">
#             <div class="usuario-info">
#                 <img src="data:image/png;base64,{logo_base64}" width="65">
#                 <div class="usuario-texto">
#                     <span>👤 {nombre_usuario}</span>
#                     <span>📄 Plan: {plan_usuario}</span>
#                 </div>
#             </div>
#         </div>
#         <div class="header-placeholder"></div>
#     """, unsafe_allow_html=True)
#
#     # Botones con resaltado según sección activa
#     col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
#
#     with col1:
#         b = st.container()
#         with b:
#             if st.button("🏠 Inicio", key="btn_inicio"):
#                 cambiar_pagina("Inicio")
#         if pagina_actual == "Inicio":
#             b.markdown("<style>.stButton button {{ background-color: #4B0082 !important; color: white !important; }}</style>", unsafe_allow_html=True)
#
#     with col2:
#         b = st.container()
#         with b:
#             if st.button("💼 Planes", key="btn_planes"):
#                 cambiar_pagina("Planes")
#         if pagina_actual == "Planes":
#             b.markdown("<style>.stButton button {{ background-color: #4B0082 !important; color: white !important; }}</style>", unsafe_allow_html=True)
#
#     with col3:
#         b = st.container()
#         with b:
#             if st.button("👤 Perfil", key="btn_perfil"):
#                 cambiar_pagina("Perfil")
#         if pagina_actual == "Perfil":
#             b.markdown("<style>.stButton button {{ background-color: #4B0082 !important; color: white !important; }}</style>", unsafe_allow_html=True)
#
#     with col4:
#         b = st.container()
#         with b:
#             if st.button("🚪 Cerrar sesión", key="btn_salir"):
#                 cambiar_pagina("Salir")
#         if pagina_actual == "Salir":
#             b.markdown("<style>.stButton button {{ background-color: #4B0082 !important; color: white !important; }}</style>", unsafe_allow_html=True)


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
#     return base64.b64encode(buffer.getvalue()).decode()
#
# def mostrar_layout(nombre_usuario: str, plan_usuario: str):
#     logo = Image.open("Logo.png")
#     logo_base64 = image_to_base64(logo)
#
#     # --- Estilos globales ---
#     st.markdown("""
#         <style>
#         .fixed-header {
#             position: fixed;
#             top: 0;
#             left: 0;
#             right: 0;
#             z-index: 1000;
#             background-color: white;
#             border-bottom: 1px solid #ccc;
#             padding: 0.8rem 2rem;
#             display: flex;
#             justify-content: space-between;
#             align-items: center;
#         }
#         .usuario-info {
#             display: flex;
#             align-items: center;
#             gap: 15px;
#         }
#         .usuario-texto {
#             display: flex;
#             flex-direction: column;
#             font-size: 0.9rem;
#         }
#         .usuario-texto span:first-child {
#             font-weight: bold;
#             color: #4B0082;
#             font-size: 1.1rem;
#         }
#         .boton {
#             background-color: #f9f9f9;
#             border: 1px solid #bbb;
#             padding: 6px 14px;
#             border-radius: 8px;
#             margin-left: 8px;
#             font-weight: bold;
#             cursor: pointer;
#             color: #4B0082;
#         }
#         .header-placeholder {
#             height: 95px;
#         }
#         </style>
#     """, unsafe_allow_html=True)
#
#     # --- Header fijo con logo, nombre y botones bonitos ---
#     st.markdown(f"""
#         <div class="fixed-header">
#             <div class="usuario-info">
#                 <img src="data:image/png;base64,{logo_base64}" width="65">
#                 <div class="usuario-texto">
#                     <span>👤 {nombre_usuario}</span>
#                     <span>📄 Plan: {plan_usuario}</span>
#                 </div>
#             </div>
#             <div class="botones">
#                 <form method="post" style="display:inline;">
#                     <button name="pagina" value="Inicio" class="boton">🏠 Inicio</button>
#                     <button name="pagina" value="Planes" class="boton">💼 Planes</button>
#                     <button name="pagina" value="Perfil" class="boton">👤 Perfil</button>
#                     <button name="pagina" value="Salir" class="boton">🚪 Cerrar sesión</button>
#                 </form>
#             </div>
#         </div>
#         <div class="header-placeholder"></div>
#     """, unsafe_allow_html=True)
#
#     # Cambiar página según botón presionado
#     form_data = st.query_params.get("pagina", None)
#     if form_data:
#         cambiar_pagina(form_data)


###################################################################################

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
