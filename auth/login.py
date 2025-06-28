from auth.conexion_supabase import supabase
import streamlit as st

def login_usuario(email: str, password: str):
    try:
        st.write(f"📧 Login: {email}")
        st.write("🔒 Intentando autenticación...")

        # 1. Autenticación con Supabase Auth
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        user = auth_response.user
        st.write("📦 Supabase user:", user)

        if not user:
            st.warning("⚠ No se recibió usuario desde Supabase.")
            return None

        user_id = user.id

        # 2. Buscar perfil personalizado en tabla 'usuarios'
        resultado = supabase.table("usuarios").select("*").eq("user_id", user_id).limit(1).execute()

        if resultado.data and len(resultado.data) > 0:
            perfil = resultado.data[0]

            # Enriquecer perfil con info del Auth (opcional)
            perfil["nombre"] = user.user_metadata.get("nombre", perfil.get("nombre", ""))
            perfil["email"] = user.email

            st.write("🧾 Perfil encontrado:", perfil)
            return perfil
        else:
            st.warning("⚠ Usuario autenticado pero no tiene perfil asociado.")
            return None

    except Exception as e:
        st.error(f"🚨 Error en login_usuario: {e}")
        print("Error de autenticación:", e)
        return None


# from auth.conexion_supabase import supabase
# import streamlit as st
#
# def login_usuario(email: str, password: str):
#     try:
#         st.write(f"📧 Login: {email}")
#         st.write("🔒 Intentando autenticación...")
#
#         # Autenticación con correo y contraseña
#         auth_response = supabase.auth.sign_in_with_password({
#             "email": email,
#             "password": password
#         })
#
#         user = auth_response.user
#         st.write("📦 Supabase user:", user)
#
#         if not user:
#             st.warning("⚠ No se recibió usuario desde Supabase.")
#             return None
#
#         # Buscar datos en la tabla personalizada usando el user_id (no email)
#         ##perfil = supabase.table("usuarios").select("*").eq("user_id", user.id).single().execute()
#
#         resultado = supabase.table("usuarios").select("*").eq("user_id", user.id).limit(1).execute()
#
#         if resultado.data and len(resultado.data) > 0:
#             return resultado.data[0]
#         else:
#             print("⚠ Usuario autenticado pero no tiene perfil asociado.")
#             return None
#
#
#
#         st.write("🧾 Perfil encontrado:", perfil.data)
#
#         if perfil.data:
#             return perfil.data
#         else:
#             st.warning("⚠ Usuario autenticado pero no se encontró en tabla 'usuarios'")
#             return None
#
#
#     except Exception as e:
#         st.error(f"🚨 Error en login_usuario: {e}")
#         print("Error de autenticación:", e)
#         return None
