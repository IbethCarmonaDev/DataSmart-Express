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
            perfil = validar_plan_trial(perfil)
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

from datetime import datetime

def validar_plan_trial(usuario):
    if usuario.get("plan") == "Premium_trial":
        fecha_inicio_str = usuario.get("fecha_inicio_trial")
        dias_trial = usuario.get("dias_trial", 7)

        if fecha_inicio_str:
            try:
                # Forzar parse de solo la fecha si viene con hora o zona
                fecha_inicio = datetime.fromisoformat(str(fecha_inicio_str).split("T")[0]).date()
                dias_transcurridos = (datetime.today().date() - fecha_inicio).days

                if dias_transcurridos > dias_trial:
                    usuario["plan"] = "Free"
                else:
                    usuario["dias_restantes_trial"] = dias_trial - dias_transcurridos
            except Exception as e:
                usuario["dias_restantes_trial"] = None  # Fallback si falla parseo


    usuario["dias_restantes_trial"] = 0
    usuario["dias_transcurridos"] = dias_transcurridos

    #st.write("Usuario:", st.session_state.usuario)

    return usuario