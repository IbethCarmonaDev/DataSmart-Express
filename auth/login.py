# from auth.conexion_supabase import supabase
#
# def login_usuario(email: str, password: str):
#     try:
#         # Intentar autenticación
#         auth_response = supabase.auth.sign_in_with_password({
#             "email": email,
#             "password": password
#         })
#
#         # 👉 NUEVO: Mostrar detalles del auth_response para debug
#         print("🔐 Auth Response:")
#         print(auth_response)
#         print("📧 Email:", email)
#
#
#
#         user = auth_response.user
#         if not user:
#             print("⛔ Usuario no autenticado")
#             return None
#
#         # Buscar perfil personalizado por user_id
#         perfil = supabase.table("usuarios").select("*").eq("user_id", user.id).single().execute()
#
#         if perfil.data:
#             return perfil.data
#         else:
#             print("⚠ Usuario autenticado pero sin perfil")
#             return None
#
#     except Exception as e:
#         print("❌ Error de autenticación:", e)
#         return None

from auth.conexion_supabase import supabase
import streamlit as st

def login_usuario(email: str, password: str):
    try:
        st.write(f"📧 Login: {email}")
        st.write("🔒 Intentando autenticación...")

        # Autenticación con correo y contraseña
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        user = auth_response.user
        st.write("📦 Supabase user:", user)

        if not user:
            st.warning("⚠ No se recibió usuario desde Supabase.")
            return None

        # Buscar datos en la tabla personalizada usando el user_id (no email)
        perfil = supabase.table("usuarios").select("*").eq("user_id", user.id).single().execute()
        st.write("🧾 Perfil encontrado:", perfil.data)

        if perfil.data:
            return perfil.data
        else:
            st.warning("⚠ Usuario autenticado pero no se encontró en tabla 'usuarios'")
            return None

    except Exception as e:
        st.error(f"🚨 Error en login_usuario: {e}")
        print("Error de autenticación:", e)
        return None
