import streamlit as st
from PIL import Image
import base64
from io import BytesIO

def mostrar_layout(nombre_usuario: str, plan_usuario: str):
    # Convertir logo a base64
    def get_logo_base64(path):
        img = Image.open(path)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()

    logo_base64 = get_logo_base64("Logo.png")

    st.markdown(f"""
        <style>
        .header-sticky {{
            position: sticky;
            top: 0;
            z-index: 999;
            background-color: white;
            padding: 1rem 2rem 0.5rem 2rem;
            border-bottom: 1px solid #eee;
        }}
        .header-container {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .logo-usuario {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        .usuario-info {{
            display: flex;
            flex-direction: column;
        }}
        .usuario-nombre {{
            font-weight: 700;
            color: #8A2BE2;
            font-size: 1rem;
        }}
        .usuario-plan {{
            font-size: 0.9rem;
            color: #444;
        }}
        .nav-buttons {{
            display: flex;
            gap: 1rem;
            justify-content: center;
            padding: 0.7rem 0.5rem;
            flex-wrap: wrap;
        }}
        button[data-testid="base-button"] {{
            border-radius: 10px;
            border: 1px solid #8A2BE2;
        }}
        </style>

        <div class="header-sticky">
            <div class="header-container">
                <div class="logo-usuario">
                    <img src="data:image/png;base64,{logo_base64}" width="50"/>
                    <div class="usuario-info">
                        <div class="usuario-nombre">{nombre_usuario.upper()}</div>
                        <div class="usuario-plan">📄 Plan: <b>{plan_usuario}</b></div>
                    </div>
                </div>
            </div>
            <div class="nav-buttons">
                <form action="?pagina=Inicio" method="get"><button>🏠 Inicio</button></form>
                <form action="?pagina=Planes" method="get"><button>💼 Planes</button></form>
                <form action="?pagina=Perfil" method="get"><button>👤 Perfil</button></form>
                <form action="?pagina=Salir" method="get"><button>📋 Cerrar sesión</button></form>
            </div>
        </div>
    """, unsafe_allow_html=True)

# import streamlit as st
# from PIL import Image
# from pathlib import Path
# from io import BytesIO
#
#
# def mostrar_layout(nombre_usuario: str, plan_usuario: str):
#     # --- Cargar logo ---
#     ruta_logo = Path("presentacion") / "logo_ds.png"
#     if ruta_logo.exists():
#         logo = Image.open(ruta_logo)
#     else:
#         logo = None
#
#     # --- Estilos CSS ---
#     st.markdown("""
#         <style>
#         .header-container {
#             display: flex;
#             align-items: center;
#             justify-content: space-between;
#             padding: 1rem;
#             position: sticky;
#             top: 0;
#             background-color: white;
#             z-index: 999;
#             border-bottom: 1px solid #ccc;
#         }
#         .user-info {
#             display: flex;
#             align-items: center;
#         }
#         .user-info img {
#             height: 50px;
#             margin-right: 1rem;
#         }
#         .botones-container {
#             display: flex;
#             gap: 1rem;
#         }
#         .boton-activo {
#             background-color: #a855f7 !important;
#             color: white !important;
#             font-weight: bold;
#         }
#         .stButton>button {
#             border: 1px solid #a855f7;
#             color: #6b21a8;
#             font-weight: 600;
#         }
#         </style>
#     """, unsafe_allow_html=True)
#
#     # --- Header ---
#     with st.container():
#         st.markdown("<div class='header-container'>", unsafe_allow_html=True)
#
#         # Izquierda: Logo y usuario
#         st.markdown("<div class='user-info'>", unsafe_allow_html=True)
#         cols = st.columns([1, 8])
#         if logo:
#             with cols[0]:
#                 st.image(logo, width=60)
#         with cols[1]:
#             st.markdown(f"""
#                 <span style='font-weight: bold; color: #6b21a8;'>{nombre_usuario.upper()}</span><br>
#                 <span>📄 Plan: <b>{plan_usuario}</b></span>
#             """, unsafe_allow_html=True)
#         st.markdown("</div>", unsafe_allow_html=True)
#
#         # Derecha: Navegación
#         st.markdown("<div class='botones-container'>", unsafe_allow_html=True)
#
#         botones = {
#             "Inicio": "🏠 Inicio",
#             "Planes": "💼 Planes",
#             "Perfil": "👤 Perfil",
#             "Salir": "📋 Cerrar sesión"
#         }
#
#         for clave, texto in botones.items():
#             if st.session_state.get("pagina_actual") == clave:
#                 estilo = "boton-activo"
#             else:
#                 estilo = ""
#             if st.button(texto, key=clave):
#                 st.session_state["pagina_actual"] = clave
#
#         st.markdown("</div>", unsafe_allow_html=True)
#         st.markdown("</div>", unsafe_allow_html=True)
#
#     st.markdown("""<hr style='margin-top: 0;'>""", unsafe_allow_html=True)
#     st.write("")



# import streamlit as st
# from PIL import Image
#
#
# def mostrar_layout(nombre_usuario, plan_usuario):
#     pagina_actual = st.session_state.get("pagina_actual", "Inicio")
#
#     # --- Estilos CSS ---
#     st.markdown("""
#         <style>
#         .header-container {
#             position: sticky;
#             top: 0;
#             z-index: 999;
#             background-color: white;
#             padding: 1rem 1rem 0 1rem;
#             border-bottom: 1px solid #eee;
#         }
#         .user-info {
#             display: flex;
#             align-items: center;
#         }
#         .user-info img {
#             height: 40px;
#             margin-right: 10px;
#         }
#         .menu-buttons {
#             display: flex;
#             justify-content: center;
#             gap: 1rem;
#             margin: 1rem 0;
#         }
#         .menu-buttons a {
#             text-decoration: none;
#             padding: 0.5rem 1rem;
#             border: 1px solid #a559c9;
#             border-radius: 8px;
#             color: #4b0082;
#             font-weight: bold;
#             background-color: white;
#         }
#         .menu-buttons a.active {
#             background-color: #a559c9;
#             color: white;
#         }
#         </style>
#     """, unsafe_allow_html=True)
#
#     # --- Encabezado sticky ---
#     st.markdown(f"""
#         <div class="header-container">
#             <div class="user-info">
#                 <img src="https://i.ibb.co/Xj6Ccn0/Logo.png" alt="Logo">
#                 <div>
#                     <strong style="font-size: 1.1rem; color: #4b0082;">{nombre_usuario.upper()}</strong><br>
#                     <span style="font-size: 0.9rem; color: #555;">📄 Plan: {plan_usuario}</span>
#                 </div>
#             </div>
#             <div class="menu-buttons">
#                 <a href="?pagina=Inicio" class="{ 'active' if pagina_actual == 'Inicio' else '' }">🏠 Inicio</a>
#                 <a href="?pagina=Planes" class="{ 'active' if pagina_actual == 'Planes' else '' }">💼 Planes</a>
#                 <a href="?pagina=Perfil" class="{ 'active' if pagina_actual == 'Perfil' else '' }">👤 Perfil</a>
#                 <a href="?pagina=Salir" class="{ 'active' if pagina_actual == 'Salir' else '' }">🚪 Cerrar sesión</a>
#             </div>
#         </div>
#     """, unsafe_allow_html=True)
#
#     st.markdown("""<br><br>""", unsafe_allow_html=True)


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
#     pagina_actual = st.session_state.get("pagina_actual", "Inicio")
#
#     # --- Estilos sticky + botones alineados ---
#     st.markdown(f"""
#         <style>
#         .sticky-header {{
#             position: fixed;
#             top: 0;
#             left: 0;
#             right: 0;
#             background-color: white;
#             z-index: 1000;
#             padding: 0.6rem 1.5rem;
#             border-bottom: 1px solid #ccc;
#             display: flex;
#             align-items: center;
#             justify-content: space-between;
#         }}
#         .usuario-info {{
#             display: flex;
#             align-items: center;
#             gap: 15px;
#         }}
#         .usuario-texto {{
#             display: flex;
#             flex-direction: column;
#         }}
#         .usuario-texto span:first-child {{
#             font-weight: bold;
#             color: #4B0082;
#             font-size: 1.05rem;
#         }}
#         .header-placeholder {{
#             height: 90px;
#         }}
#         .botones-row {{
#             margin-top: -20px;
#             margin-bottom: 20px;
#             display: flex;
#             justify-content: center;
#             gap: 12px;
#         }}
#         .stButton > button {{
#             border-radius: 6px;
#             padding: 6px 16px;
#             font-weight: bold;
#             border: 1px solid #bbb;
#             color: #4B0082;
#             background-color: #f9f9f9;
#         }}
#         .stButton > button:hover {{
#             background-color: #e8e8ff;
#         }}
#         .activo > button {{
#             background-color: #4B0082 !important;
#             color: white !important;
#             border-color: #4B0082 !important;
#         }}
#         </style>
#     """, unsafe_allow_html=True)
#
#     # Sticky: logo + nombre + plan
#     st.markdown(f"""
#         <div class="sticky-header">
#             <div class="usuario-info">
#                 <img src="data:image/png;base64,{logo_base64}" width="60">
#                 <div class="usuario-texto">
#                     <span>👤 {nombre_usuario}</span>
#                     <span>📄 Plan: {plan_usuario}</span>
#                 </div>
#             </div>
#         </div>
#         <div class="header-placeholder"></div>
#     """, unsafe_allow_html=True)
#
#     # Botones debajo del sticky (funcionales)
#     st.markdown("<div class='botones-row'>", unsafe_allow_html=True)
#     btns = {
#         "Inicio": "🏠 Inicio",
#         "Planes": "💼 Planes",
#         "Perfil": "👤 Perfil",
#         "Salir": "🚪 Cerrar sesión"
#     }
#
#     for clave, texto in btns.items():
#         clase = "activo" if pagina_actual == clave else ""
#         with st.container():
#             with st.columns([1])[0]:
#                 if st.button(texto, key=f"btn_{clave}"):
#                     cambiar_pagina(clave)
#                 if clase:
#                     st.markdown(f"<style>.stButton#{'btn_' + clave} button{{background-color:#4B0082;color:white;border-color:#4B0082;}}</style>", unsafe_allow_html=True)
#     st.markdown("</div>", unsafe_allow_html=True)


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
#     st.markdown(f"""
#         <style>
#         .sticky-header {{
#             position: fixed;
#             top: 0;
#             left: 0;
#             right: 0;
#             z-index: 999;
#             background-color: white;
#             border-bottom: 1px solid #ccc;
#             padding: 0.6rem 1.5rem;
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
#         }}
#         .usuario-texto span:first-child {{
#             font-weight: bold;
#             color: #4B0082;
#             font-size: 1.05rem;
#         }}
#         .header-placeholder {{
#             height: 85px;
#         }}
#         .stButton > button {{
#             border-radius: 6px;
#             padding: 6px 12px;
#             font-weight: bold;
#             border: 1px solid #bbb;
#             color: #4B0082;
#             background-color: #f9f9f9;
#         }}
#         .stButton.active > button {{
#             background-color: #4B0082 !important;
#             color: white !important;
#             border-color: #4B0082 !important;
#         }}
#         </style>
#     """, unsafe_allow_html=True)
#
#     st.markdown(f"""
#         <div class="sticky-header">
#             <div class="usuario-info">
#                 <img src="data:image/png;base64,{logo_base64}" width="60">
#                 <div class="usuario-texto">
#                     <span>👤 {nombre_usuario}</span>
#                     <span>📄 Plan: {plan_usuario}</span>
#                 </div>
#             </div>
#             <div>
#                 <!-- Botones aquí irán por columnas reales -->
#             </div>
#         </div>
#         <div class="header-placeholder"></div>
#     """, unsafe_allow_html=True)
#
#     # Botones con columnas reales (que sí actualizan estado)
#     col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
#     with col1:
#         if st.button("🏠 Inicio", key="btn_inicio"):
#             cambiar_pagina("Inicio")
#         if pagina_actual == "Inicio":
#             st.markdown("<style>.stButton:nth-child(1) button{background-color:#4B0082;color:white;}</style>", unsafe_allow_html=True)
#     with col2:
#         if st.button("💼 Planes", key="btn_planes"):
#             cambiar_pagina("Planes")
#         if pagina_actual == "Planes":
#             st.markdown("<style>.stButton:nth-child(2) button{background-color:#4B0082;color:white;}</style>", unsafe_allow_html=True)
#     with col3:
#         if st.button("👤 Perfil", key="btn_perfil"):
#             cambiar_pagina("Perfil")
#         if pagina_actual == "Perfil":
#             st.markdown("<style>.stButton:nth-child(3) button{background-color:#4B0082;color:white;}</style>", unsafe_allow_html=True)
#     with col4:
#         if st.button("🚪 Cerrar sesión", key="btn_salir"):
#             cambiar_pagina("Salir")



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
#     st.markdown(f"""
#         <style>
#         .sticky-header {{
#             position: fixed;
#             top: 0;
#             left: 0;
#             right: 0;
#             z-index: 999;
#             background-color: white;
#             border-bottom: 1px solid #ccc;
#             padding: 0.6rem 1.5rem;
#             display: flex;
#             justify-content: space-between;
#             align-items: center;
#             gap: 30px;
#         }}
#         .usuario-info {{
#             display: flex;
#             align-items: center;
#             gap: 15px;
#         }}
#         .usuario-texto {{
#             display: flex;
#             flex-direction: column;
#         }}
#         .usuario-texto span:first-child {{
#             font-weight: bold;
#             color: #4B0082;
#             font-size: 1.05rem;
#         }}
#         .botones-nav {{
#             display: flex;
#             gap: 8px;
#         }}
#         .boton {{
#             border-radius: 6px;
#             padding: 6px 12px;
#             font-weight: bold;
#             border: 1px solid #bbb;
#             color: #4B0082;
#             background-color: #f8f8f8;
#             cursor: pointer;
#         }}
#         .boton-activo {{
#             background-color: #4B0082;
#             color: white;
#             border: 1px solid #4B0082;
#         }}
#         .header-placeholder {{
#             height: 85px;
#         }}
#         </style>
#
#         <div class="sticky-header">
#             <div class="usuario-info">
#                 <img src="data:image/png;base64,{logo_base64}" width="60">
#                 <div class="usuario-texto">
#                     <span>👤 {nombre_usuario}</span>
#                     <span>📄 Plan: {plan_usuario}</span>
#                 </div>
#             </div>
#             <div class="botones-nav">
#                 <form method="get">
#                     <button name="pagina" value="Inicio" class="boton {'boton-activo' if pagina_actual == 'Inicio' else ''}">🏠 Inicio</button>
#                     <button name="pagina" value="Planes" class="boton {'boton-activo' if pagina_actual == 'Planes' else ''}">💼 Planes</button>
#                     <button name="pagina" value="Perfil" class="boton {'boton-activo' if pagina_actual == 'Perfil' else ''}">👤 Perfil</button>
#                     <button name="pagina" value="Salir" class="boton {'boton-activo' if pagina_actual == 'Salir' else ''}">🚪 Cerrar sesión</button>
#                 </form>
#             </div>
#         </div>
#         <div class="header-placeholder"></div>
#     """, unsafe_allow_html=True)
#
#     # Captura de navegación
#     pagina = st.query_params.get("pagina", None)
#     if pagina:
#         cambiar_pagina(pagina)


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
