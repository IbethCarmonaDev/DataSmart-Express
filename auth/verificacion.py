############################################################
# Creador por: Ibeth Carmona.Jun 25-2025
# Opción para verificar los Usuarios
############################################################
# auth/verificacion.py

import streamlit as st
from PIL import Image

def mostrar_verificacion_exitosa():
    # Interfaz amigable con logo
    col_logo, col_msg = st.columns([1, 2])

    with col_logo:
        try:
            logo = Image.open("Logo.png")
            st.image(logo, width=140)
        except:
            st.write("")

    with col_msg:
        st.markdown("## ✅ Correo verificado correctamente")
        st.success("Tu cuenta ya está activa. Ahora puedes iniciar sesión.")

        if st.button("🔐 Iniciar sesión"):
            st.session_state.modo = "login"
            st.experimental_set_query_params()  # limpia access_token de la URL
            st.rerun()
