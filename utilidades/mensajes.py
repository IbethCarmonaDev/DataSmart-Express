# utilidades/mensajes.py

import streamlit as st
from PIL import Image

def mostrar_mensaje_confirmacion(titulo: str = "✔ Registro confirmado", mensaje: str = "Tu perfil ha sido creado exitosamente. Ya puedes iniciar sesión."):
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
