from auth.conexion_supabase import supabase
import streamlit as st
from datetime import datetime

def login_usuario(email: str, password: str):
    try:
        # Autenticación con Supabase Auth
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        user = auth_response.user

        # Validación de usuario obtenido
        if not user:
            error_msg = getattr(auth_response, "error", None)
            if error_msg and "Email not confirmed" in str(error_msg):
                return {"status": "no_confirmado"}
            else:
                st.warning("Correo o contraseña incorrectos.")
                return None

        # Obtener user_id
        user_id = getattr(user, "id", None)
        if not user_id:
            st.error("No se pudo obtener el ID del usuario autenticado.")
            return None

        # Buscar perfil en la tabla 'usuarios'
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
        error_str = str(e)
        if "Email not confirmed" in error_str:
            return {"status": "no_confirmado"}
        #st.error(f"Error técnico durante el login: {e}")
        return None

def validar_plan_trial(usuario):
    if usuario.get("plan") == "Premium_trial":
        fecha_inicio = usuario.get("fecha_inicio_trial")
        dias_trial = usuario.get("dias_trial", 7)

        if fecha_inicio:
            dias_transcurridos = (datetime.today().date() - datetime.fromisoformat(fecha_inicio).date()).days
            if dias_transcurridos > dias_trial:
                usuario["plan"] = "Free"
            else:
                usuario["dias_restantes_trial"] = dias_trial - dias_transcurridos
    return usuario
