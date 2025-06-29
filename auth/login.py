from auth.conexion_supabase import supabase
import streamlit as st

def login_usuario(email: str, password: str):
    try:
        st.write(f"📧 Login: {email}")
        st.write("🔒 Intentando autenticación...")

        # Paso 1: Autenticación con Supabase Auth
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        user = auth_response.user
        st.write("📦 Supabase user:")
        st.json(user)

        # Validar si se recibió el usuario correctamente
        if not user:
            st.warning("⚠ No se recibió usuario desde Supabase Auth.")
            return None

        # Paso 2: Obtener user_id de forma segura
        user_id = user.get("id") if isinstance(user, dict) else getattr(user, "id", None)

        if not user_id:
            st.error("❌ No se pudo obtener el ID del usuario autenticado.")
            return None

        st.write("🔑 Buscando perfil asociado con user_id:", user_id)

        # Paso 3: Buscar en la tabla personalizada 'usuarios'
        st.write("🆔 user_id:", user_id)
        st.write("🧪 Tipo de user_id:", type(user_id))

        resultado = supabase.table("usuarios") \
            .select("*") \
            .eq("user_id", user_id) \
            .limit(1) \
            .execute()


        st.write("🔑 Resultado con user_id_str:", resultado)

        st.write("🔍 Buscando por correo en usuarios...")

        resultado_email = supabase.table("usuarios") \
            .select("*") \
            .eq("email", email) \
            .limit(5) \
            .execute()

        st.write("📬 Resultado por email:", resultado_email)


        if resultado.data and len(resultado.data) > 0:
            perfil = resultado.data[0]
            st.success("✅ Perfil encontrado correctamente.")
            st.json(perfil)
            return perfil
        else:
            st.warning("⚠ Usuario autenticado pero no tiene perfil en tabla 'usuarios'.")
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
#         # 1. Autenticación con Supabase Auth
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
#         user_id = user.id
#
#         # 2. Buscar perfil personalizado en tabla 'usuarios'
#         ##resultado = supabase.table("usuarios").select("*").eq("user_id", user_id).limit(1).execute()
#
#         user_id = user.get("id") if isinstance(user, dict) else getattr(user, "id", None)
#
#         if user_id:
#             resultado = supabase.table("usuarios").select("*").eq("user_id", user_id).limit(1).execute()
#             if resultado.data and len(resultado.data) > 0:
#                 return resultado.data[0]
#             else:
#                 st.warning("⚠ Usuario autenticado pero no tiene perfil asociado en tabla 'usuarios'")
#                 return None
#         else:
#             st.error("❌ No se pudo obtener el user_id del usuario autenticado.")
#             return None
#
#         if resultado.data and len(resultado.data) > 0:
#             perfil = resultado.data[0]
#
#             # Enriquecer perfil con info del Auth (opcional)
#             perfil["nombre"] = user.user_metadata.get("nombre", perfil.get("nombre", ""))
#             perfil["email"] = user.email
#
#             st.write("🧾 Perfil encontrado:", perfil)
#             return perfil
#         else:
#             st.warning("⚠ Usuario autenticado pero no tiene perfil asociado.")
#             return None
#
#     except Exception as e:
#         st.error(f"🚨 Error en login_usuario: {e}")
#         print("Error de autenticación:", e)
#         return None
