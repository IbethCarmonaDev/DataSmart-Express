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

    # Estilos para encabezado sticky
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
        .botones button {
            background-color: white;
            color: #4B0082;
            border: 1px solid #4B0082;
            border-radius: 6px;
            padding: 5px 12px;
            margin-left: 6px;
            font-weight: bold;
            cursor: pointer;
        }
        </style>
    """, unsafe_allow_html=True)

    # HTML: cabecera sticky con botones
    st.markdown(f"""
        <div class="sticky-header">
            <div class="usuario-info">
                <img src="data:image/png;base64,{logo_base64}" width="70"/>
                <div class="usuario-texto">
                    <span>👤 {nombre_usuario}</span>
                    <span>📄 Plan: {plan_usuario}</span>
                </div>
            </div>
            <div class="botones">
                <form action="" method="get">
                    <button type="submit" name="pagina" value="Inicio">Inicio</button>
                    <button type="submit" name="pagina" value="Planes">Planes</button>
                    <button type="submit" name="pagina" value="Perfil">Perfil</button>
                    <button type="submit" name="pagina" value="Salir">Cerrar sesión</button>
                </form>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Leer query param desde st.query_params
    pagina = st.query_params.get("pagina", None)
    if pagina:
        cambiar_pagina(pagina)


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
