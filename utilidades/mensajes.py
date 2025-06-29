# utilidades/mensajes.py

import streamlit as st
from PIL import Image

def mostrar_mensaje_confirmacion\
    (titulo, mensaje, tipo="success", boton_texto=None, boton_callback=None):

    """
    Muestra un mensaje estilizado con emoji, color y botón opcional.

    tipo: "success", "warning", "error", "info"
    """
    import streamlit as st

    emojis = {
        "success": "✅",
        "warning": "⚠️",
        "error": "❌",
        "info": "ℹ️"
    }

    colores = {
        "success": "#DFF2BF",
        "warning": "#FFF8C4",
        "error": "#F8D7DA",
        "info": "#D9EDF7"
    }

    bordes = {
        "success": "#4CAF50",
        "warning": "#FFB800",
        "error": "#D8000C",
        "info": "#31708F"
    }

    st.markdown(f"""
    <div style="background-color: {colores[tipo]}; border-left: 5px solid {bordes[tipo]}; padding: 1.5rem; border-radius: 0.5rem; margin: 1rem 0;">
        <h3 style="margin: 0;">{emojis[tipo]} {titulo}</h3>
        <p style="margin-top: 0.5rem; font-size: 1.1rem;">{mensaje}</p>
    </div>
    """, unsafe_allow_html=True)

    if boton_texto and boton_callback:
        st.button(boton_texto, on_click=boton_callback, use_container_width=True)


def OLDmostrar_mensaje_confirmacion(titulo: str = "✔ Registro confirmado", mensaje: str = "Tu perfil ha sido creado exitosamente. Ya puedes iniciar sesión."):
    try:
        logo = Image.open("Logo.png")
        st.image(logo, width=200)
    except:
        pass

    st.markdown(f"<h2 style='text-align: center; color: green;'>{titulo}</h2>", unsafe_allow_html=True)
    st.success(mensaje)

    st.markdown(
        """
        <div style='text-align: center; margin-top: 20px;'>
            <a href='/?reload=true' style='
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
            '>🔑 Iniciar sesión</a>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align: center; margin-top: 30px;'>Gracias por unirte a <strong>DataSmart Express</strong>. Tu análisis financiero inteligente comienza ahora 🚀</p>",
        unsafe_allow_html=True
    )
