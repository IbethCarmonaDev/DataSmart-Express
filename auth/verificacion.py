############################################################
# Creador por: Ibeth Carmona.Jun 25-2025
# Opción para verificar los Usuarios
############################################################
import streamlit as st
from PIL import Image
from auth.reset_password import mostrar_reset_password
from auth.conexion_supabase import supabase
from database.usuarios import guardar_perfil_usuario
from datetime import datetime
import streamlit as st

def mostrar_verificacion_o_reset(token):
    try:
        user = supabase.auth.get_user(token).user
        if not user:
            st.error("❌ Token inválido o expirado.")
            return

        user_id = user.id
        email = user.email
        confirmed_at = user.confirmed_at
        email_confirmed_at = user.email_confirmed_at

        # Para depuración (puedes quitar luego)
        st.write("🧾 ID:", user_id)
        st.write("📧 Email:", email)
        st.write("📅 Email confirmado:", email_confirmed_at)
        st.write("🧍 Confirmado:", confirmed_at)

        # ✅ Primera vez que confirma su email
        if confirmed_at == email_confirmed_at:
            mostrar_bienvenida_post_registro()
        else:
            mostrar_reset_password(token)

    except Exception as e:
        st.error("❌ Error al procesar el token.")
        st.exception(e)

def mostrar_bienvenida_post_registro():
    col_logo, col_msg = st.columns([1, 2])

    with col_logo:
        try:
            logo = Image.open("Logo.png")
            st.image(logo, width=140)
        except:
            st.write("")

    with col_msg:
        st.markdown("## ✅ ¡Tu correo ha sido verificado!")
        st.success("Tu cuenta ya está activa. Ahora puedes iniciar sesión.")

        if st.button("🔐 Iniciar sesión"):
            st.session_state.modo = "login"
            st.query_params.clear()

            st.rerun()


def manejar_signup(token):
    try:
        user = supabase.auth.get_user(token).user

        if not user:
            st.error("❌ No se pudo recuperar la información del usuario.")
            return

        id_usuario = user.id
        email = user.email
        nombre = user.user_metadata.get("nombre", "")

        # Verificar si ya existe
        existe = supabase.table("usuarios").select("user_id").eq("user_id", id_usuario).execute()
        if not existe.data:
            perfil = {
                "user_id": id_usuario,
                "nombre": nombre,
                "email": email,
                "plan_actual": "Premium_trial",
                "fecha_inicio_trial": datetime.now().strftime("%Y-%m-%d"),
                "dias_trial": 7
            }
            guardar_perfil_usuario(perfil)

        st.success("✅ ¡Tu cuenta ha sido verificada correctamente! Ya puedes iniciar sesión.")
        st.markdown("[🔑 Ir al login](./)", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error durante la verificación: {e}")


