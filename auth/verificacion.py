############################################################
# Creador por: Ibeth Carmona.Jun 25-2025
# Opción para verificar los Usuarios
############################################################
from PIL import Image
from auth.reset_password import mostrar_reset_password
from auth.conexion_supabase import supabase
from database.usuarios import guardar_perfil_usuario
from datetime import datetime
import streamlit as st

def mostrar_verificacion_o_reset(token: str):
    params = st.query_params
    tipo = params.get("type")

    st.warning("🛠 Debug flujo")
    st.write("🔐 Token:", token)
    st.write("📦 Tipo:", tipo)
    st.write("🔐 params:", params)

    if tipo == "recovery":
        mostrar_reset_password(token)
    elif tipo == "signup":
        st.success("✅ Confirmación de registro...")
        st.markdown("### ✅ ¡Tu correo ha sido verificado!")
        st.info("Tu cuenta ya está activa. Ahora puedes iniciar sesión.")
        st.button("🔐 Iniciar sesión", on_click=lambda: st.rerun())
    else:
        st.error("❌ Tipo de redirección desconocido. Verifica el enlace.")

# Muestra pantalla de confirmación de correo después del registro y guarda en la tabla usuarios
def manejar_signup(token):
    try:
        user = supabase.auth.get_user(token).user

        if not user:
            st.error("❌ No se pudo recuperar la información del usuario.")
            return

        id_usuario = user.id
        email = user.email
        nombre = user.user_metadata.get("nombre", "")

        # Verificar si ya existe en la tabla 'usuarios'
        existe = supabase.table("usuarios").select("user_id").eq("user_id", id_usuario).execute()
        if existe.data == []:  # 👈 CORREGIDO
            perfil = {
                "user_id": id_usuario,
                "nombre": nombre,
                "email": email,
                "plan_actual": "Premium_trial",
                "fecha_inicio_trial": datetime.now().strftime("%Y-%m-%d"),
                "dias_trial": 7
            }
            guardar_perfil_usuario(perfil)

        mostrar_bienvenida_post_registro()

    except Exception as e:
        st.error(f"❌ Error durante la verificación: {e}")

# Muestra la pantalla de bienvenida tras verificar el correo
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

# Llama a Supabase para guardar la nueva contraseña
def procesar_reset_password(token, nueva_clave):
    try:
        resultado = supabase.auth.update_user({
            "password": nueva_clave
        }, token=token)

        if resultado.user:
            st.success("✅ Tu contraseña ha sido restablecida con éxito.")
            st.markdown("[🔑 Ir al login](./)", unsafe_allow_html=True)
        else:
            st.error("❌ No se pudo actualizar la contraseña. Intenta nuevamente.")
    except Exception as e:
        st.error(f"❌ Error al restablecer la contraseña: {e}")


