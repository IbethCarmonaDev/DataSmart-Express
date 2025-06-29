############################################################
# Creador por: Ibeth Carmona.Jun 15-2025
# Opcion para Interfaz de Login y registro usuarios.
#
############################################################

import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
from auth.login import login_usuario
from auth.registro import registrar_usuario
from auth.conexion_supabase import supabase

# Cargar .env
load_dotenv(override=True)

def mostrar_login():
    col_logo, col_form = st.columns([1, 2])

    with col_logo:
        try:
            logo = Image.open("Logo.png")
            st.image(logo, width=140)
        except:
            st.write("")

        st.markdown("""
        <div style='margin-top: 20px;'>
            <h4 style='color: #2b85ff; font-weight: bold; margin-bottom: 0;'>Automatiza.</h4>
            <h4 style='color: #2b85ff; font-weight: bold; margin-bottom: 0;'>Visualiza.</h4>
            <h4 style='color: #2b85ff; font-weight: bold;'>Decide con inteligencia.</h4>
        </div>
        """, unsafe_allow_html=True)

    with col_form:
        st.markdown("""
        <style>
        .form-title {
            font-size: 24px;
            font-weight: 700;
            text-align: center;
            color: #2b85ff;
            margin-bottom: 0.5rem;
        }
        .form-subtext {
            font-size: 14px;
            text-align: center;
            color: #666666;
            margin-bottom: 1rem;
        }
        .form-link {
            color: #2b85ff;
            font-weight: 600;
            cursor: pointer;
        }
        div.stButton > button:first-child {
            background-color: #2b85ff !important;
            color: white !important;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.5rem 1.5rem;
            width: 200px;
            display: block;
            margin: 1rem auto;
        }
        </style>
        """, unsafe_allow_html=True)

        if "modo" not in st.session_state:
            st.session_state.modo = "login"

        # --- Login ---
        if st.session_state.modo == "login":
            st.markdown('<div class="form-title">Inicio de sesión</div>', unsafe_allow_html=True)

            email = st.text_input("Correo electrónico", key="login_email")
            password = st.text_input("Contraseña", type="password", key="login_pass")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Ingresar"):
                    # usuario = login_usuario(email, password)
                    # if usuario:
                    #     st.session_state.usuario = usuario
                    #     st.success(f"Bienvenido/a {usuario['nombre']}")
                    #     st.rerun()
                    # else:
                    #     st.error("❌ Correo o contraseña incorrectos. Intenta nuevamente.")

                    with st.spinner("Verificando usuario..."):
                        #st.info(f"🧪 Intentando login con: {email}")
                        usuario = login_usuario(email, password)

                        if usuario:
                            if usuario.get("status") == "no_confirmado":
                                st.info(
                                    "✉ Tu correo aún no ha sido confirmado. Por favor revisa tu bandeja de entrada para confirmar tu cuenta antes de iniciar sesión.")
                            else:
                                st.success(f"✅ Bienvenido/a {usuario['nombre']}")
                                st.session_state.usuario = usuario
                                st.rerun()
                        else:
                            st.error("❌ Correo o contraseña incorrectos. Intenta nuevamente.")

            with col2:
                if st.button("¿Olvidaste tu contraseña?"):
                    st.session_state.modo = "recuperar"
                    st.rerun()

            st.markdown('<div class="form-subtext">¿Aún no tienes una cuenta?</div>', unsafe_allow_html=True)
            if st.button("🔐 Regístrate aquí"):
                st.session_state.modo = "registro"
                st.rerun()

        # --- Registro ---
        elif st.session_state.modo == "registro":
            st.markdown('<div class="form-title">Crear cuenta</div>', unsafe_allow_html=True)

            nombre = st.text_input("Nombre completo", key="reg_nombre")
            email = st.text_input("Correo electrónico", key="reg_email")
            password = st.text_input("Contraseña", type="password", key="reg_pass")

            if st.button("Registrarme"):
                resultado = registrar_usuario(nombre, email, password)

                st.write(f"🔑 resultado: {resultado}")

                if resultado["status"] == "ok":
                    st.success("✅ Registro exitoso. Revisa tu correo.")
                    st.session_state.modo = "login"
                    st.rerun()
                else:
                    st.error(f"❌ Error: {resultado['mensaje']}")

            if st.button("← Ya tengo cuenta. Volver al login"):
                st.session_state.modo = "login"
                st.rerun()

        # --- Recuperación de contraseña ---
        elif st.session_state.modo == "recuperar":
            st.markdown('<div class="form-title">Recuperar contraseña</div>', unsafe_allow_html=True)
            email = st.text_input("Correo registrado", key="recuperar_email")

            if st.button("Enviar enlace de recuperación"):
                redirect_url = os.getenv("RESET_PASSWORD_REDIRECT")
                if not redirect_url:
                    st.error("⚠ La URL de redirección no está configurada en el archivo .env.")
                else:
                    try:
                        supabase.auth.reset_password_for_email(
                            email,
                            options={"redirectTo": redirect_url}
                        )
                        st.success("📧 Si el correo está registrado, se ha enviado un enlace de recuperación.")
                    except Exception as e:
                        st.error(f"❌ Error técnico: {e}")

            if st.button("← Volver al login"):
                st.session_state.modo = "login"
                st.rerun()

        # --- Auto login si ya está autenticado ---
        if st.session_state.get("usuario"):
            usuario = st.session_state.usuario
            st.success(f"Bienvenido/a {usuario['nombre']}")
            st.rerun()

