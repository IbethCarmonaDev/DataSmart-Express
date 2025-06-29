from auth.conexion_supabase import supabase
import streamlit as st

def login_usuario(email: str, password: str):
    try:
        # Autenticación con Supabase Auth
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        user = auth_response.user

        # Si no hay usuario, puede deberse a múltiples causas
        if not user:
            # Extrae el mensaje de error si está disponible
            error_msg = getattr(auth_response, "error", None)
            if error_msg and "Email not confirmed" in str(error_msg):
                return {"status": "no_confirmado"}
            else:
                st.warning("Correo o contraseña incorrectos.")
                return None

        # Validar si el correo está confirmado
        if not user.email_confirmed:
            return {"status": "no_confirmado"}

        user_id = user.get("id") if isinstance(user, dict) else getattr(user, "id", None)
        if not user_id:
            st.error("No se pudo obtener el ID del usuario autenticado.")
            return None

        # Buscar perfil en tabla 'usuarios'
        resultado = supabase.table("usuarios") \
            .select("*") \
            .eq("user_id", user_id) \
            .limit(1) \
            .execute()

        if resultado.data and len(resultado.data) > 0:
            perfil = resultado.data[0]
            perfil["status"] = "ok"
            return perfil
        else:
            st.warning("Usuario autenticado pero no tiene perfil registrado.")
            return None

    except Exception as e:
        st.error(f"Error técnico durante el login: {e}")
        return None


def OLD1login_usuario(email: str, password: str):
    try:
        # Autenticación con Supabase Auth
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        user = auth_response.user
        if not user:
            st.warning("Correo o contraseña incorrectos.")
            return None

        user_id = user.get("id") if isinstance(user, dict) else getattr(user, "id", None)
        if not user_id:
            st.error("No se pudo obtener el ID del usuario autenticado.")
            return None

        # Buscar perfil en tabla 'usuarios'
        resultado = supabase.table("usuarios") \
            .select("*") \
            .eq("user_id", user_id) \
            .limit(1) \
            .execute()

        if resultado.data and len(resultado.data) > 0:
            return resultado.data[0]
        else:
            st.warning("Usuario autenticado pero no tiene perfil registrado.")
            return None

    except Exception as e:
        #st.error(f"Error durante el login: {e}")
        return None


