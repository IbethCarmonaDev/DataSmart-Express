############################################################
# Creador por: Ibeth Carmona.Jun 25-2025
# Opción para verificar los Usuarios
############################################################
#
# import streamlit as st
# from PIL import Image
# from auth.reset_password import mostrar_reset_password
# from auth.conexion_supabase import supabase
#
#
# # def mostrar_verificacion_exitosa():
# #     # Interfaz amigable con logo
# #     col_logo, col_msg = st.columns([1, 2])
# #
# #     with col_logo:
# #         try:
# #             logo = Image.open("Logo.png")
# #             st.image(logo, width=140)
# #         except:
# #             st.write("")
# #
# #     with col_msg:
# #         st.markdown("## ✅ Correo verificado correctamente")
# #         st.success("Tu cuenta ya está activa. Ahora puedes iniciar sesión.")
# #
# #         if st.button("🔐 Iniciar sesión"):
# #             st.session_state.modo = "login"
# #             st.experimental_set_query_params()  # limpia access_token de la URL
# #             st.rerun()
#
# def usuario_ya_registrado(user_id):
#     try:
#         result = supabase.table("usuarios").select("user_id").eq("user_id", user_id).execute()
#         return len(result.data) > 0
#     except:
#         return False
#
# def mostrar_verificacion_o_reset(token):
#     try:
#         # Obtener info del usuario con el token
#         user = supabase.auth.get_user(token).user
#         user_id = user.id
#
#         if usuario_ya_registrado(user_id):
#             # Es restablecimiento
#             mostrar_reset_password(token)
#         else:
#             # Es verificación de nuevo usuario
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
#                     st.experimental_set_query_params()
#                     st.rerun()
#
#     except Exception as e:
#         st.error(f"❌ Error al obtener información del usuario: {e}")


# auth/verificacion.py

import streamlit as st
from PIL import Image
from auth.reset_password import mostrar_reset_password
from auth.conexion_supabase import supabase


def usuario_ya_registrado(user_id):
    try:
        result = supabase.table("usuarios").select("user_id").eq("user_id", user_id).execute()
        return len(result.data) > 0
    except Exception as e:
        print("Error al verificar si el usuario existe:", e)
        return False


def mostrar_verificacion_o_reset(token):
    try:
        # Obtener información del usuario autenticado con el token
        user = supabase.auth.get_user(token).user
        if not user:
            st.error("❌ Token inválido o expirado.")
            return

        user_id = user.id

        if usuario_ya_registrado(user_id):
            # Si ya está en la tabla usuarios → es restablecimiento
            mostrar_reset_password(token)
        else:
            # Si no está → es confirmación de nuevo usuario
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

    except Exception as e:
        st.error("❌ Error al procesar el token.")
        st.exception(e)
