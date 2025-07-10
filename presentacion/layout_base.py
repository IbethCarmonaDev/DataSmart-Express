import streamlit as st
from PIL import Image

def cambiar_pagina(pagina: str):
    st.session_state["pagina_actual"] = pagina

def mostrar_layout(nombre_usuario: str, plan_usuario: str):
    logo = Image.open("Logo.png")

    st.markdown("""
        <style>
        .encabezado {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.5rem 1rem;
            background-color: #f9f9f9;
            border-bottom: 1px solid #ccc;
            border-radius: 8px;
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
        .botones button {
            background-color: white;
            color: #4B0082;
            border: 1px solid #4B0082;
            border-radius: 6px;
            padding: 4px 10px;
            font-weight: bold;
            cursor: pointer;
        }
        </style>
    """, unsafe_allow_html=True)

    # HTML que construye el layout visual
    st.markdown(f"""
        <div class="encabezado">
            <div class="usuario-info">
                <img src="data:image/png;base64,{image_to_base64(logo)}" width="70"/>
                <div class="usuario-texto">
                    <span>👤 {nombre_usuario}</span>
                    <span>📄 Plan: {plan_usuario}</span>
                </div>
            </div>
            <div class="botones">
                <form method="post"><button name="pagina" value="Inicio">Inicio</button></form>
                <form method="post"><button name="pagina" value="Planes">Planes</button></form>
                <form method="post"><button name="pagina" value="Perfil">Perfil</button></form>
                <form method="post"><button name="pagina" value="Salir">Cerrar sesión</button></form>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Detectar cambio de página desde formulario POST
    if st.session_state.get("_form_data"):
        pagina = st.session_state["_form_data"].get("pagina")
        if pagina:
            cambiar_pagina(pagina)

def image_to_base64(image):
    import base64
    from io import BytesIO
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return img_str


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
