############################################################
# Creador por: Ibeth Carmona.Jun 25-2025
# Opción para verificar los Usuarios
# auth/verificacion.py
############################################################
import streamlit as st
from PIL import Image
from auth.reset_password import mostrar_reset_password
from auth.conexion_supabase import supabase


def usuario_ya_registrado(user_id: str, email: str) -> bool:
    try:
        # Buscar por user_id
        result_id = supabase.table("usuarios").select("user_id").eq("user_id", user_id).execute()
        st.write("🧪 Buscando por user_id:", user_id)

        if result_id.data and len(result_id.data) > 0:
            return True

        # Buscar por email como respaldo
        st.write("🔍 No se encontró por ID, buscando por email:", email)
        result_email = supabase.table("usuarios").select("user_id").ilike("email", email).execute()

        return result_email.data and len(result_email.data) > 0

    except Exception as e:
        st.error("⚠️ Error al verificar existencia del usuario.")
        st.exception(e)
        return False


def mostrar_verificacion_o_reset(token):
    try:
        user = supabase.auth.get_user(token).user
        if not user:
            st.error("❌ Token inválido o expirado.")
            return

        user_id = user.id
        email = user.email
        st.write("🧾 ID desde token:", user_id)
        st.write("📧 Email desde token:", email)

        if usuario_ya_registrado(user_id, email):
            mostrar_reset_password(token)
        else:
            # UI bonita con logo
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
                    st.experimental_set_query_params()
                    st.rerun()

    except Exception as e:
        st.error("❌ Error al procesar el token.")
        st.exception(e)



# import streamlit as st
# from PIL import Image
# from auth.reset_password import mostrar_reset_password
# from auth.conexion_supabase import supabase
#
#
# def usuario_ya_registrado(user_id):
#     try:
#         result = supabase.table("usuarios").select("user_id").eq("user_id", user_id).execute()
#         return len(result.data) > 0
#     except Exception as e:
#         print("Error al verificar si el usuario existe:", e)
#         return False
#
#
# def mostrar_verificacion_o_reset(token):
#     try:
#         # Obtener información del usuario autenticado con el token
#         user = supabase.auth.get_user(token).user
#         if not user:
#             st.error("❌ Token inválido o expirado.")
#             return
#
#         user_id = user.id
#
#         if usuario_ya_registrado(user_id):
#             # Si ya está en la tabla usuarios → es restablecimiento
#             mostrar_reset_password(token)
#         else:
#             # Si no está → es confirmación de nuevo usuario
#             col_logo, col_msg = st.columns([1, 2])
#
#             with col_logo:
#                 try:
#                     logo = Image.open("Logo.png")
#                     st.image(logo, width=140)
#                 except:
#                     st.write("")
#
#             with col_msg:
#                 st.markdown("## ✅ Correo verificado correctamente")
#                 st.success("Tu cuenta ya está activa. Ahora puedes iniciar sesión.")
#
#                 if st.button("🔐 Iniciar sesión"):
#                     st.session_state.modo = "login"
#                     st.experimental_set_query_params()  # limpia access_token de la URL
#                     st.rerun()
#
#     except Exception as e:
#         st.error("❌ Error al procesar el token.")
#         st.exception(e)
# ############################################################
