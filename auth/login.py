from database.usuarios import actualizar_plan_usuario  # Asegúrate de tener este import
from datetime import datetime, timezone
import streamlit as st
from auth.conexion_supabase import supabase
##from auth.login import validar_plan_trial

from utilidades.eventos import registrar_evento_usuario, registrar_evento_usuario_test  # Asegúrate que esta función esté lista

def login_usuario(email: str, password: str):
    try:
        # 🔐 Autenticación con Supabase Auth
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        user = auth_response.user

        # ❌ Si no se retorna usuario, validar tipo de error
        if not user:
            error_msg = getattr(auth_response, "error", None)
            if error_msg and "Email not confirmed" in str(error_msg):
                # 📝 Registrar evento de error: email no confirmado
                registrar_evento_usuario(None, "error_login", f"Email no confirmado: {email}")
                return {"status": "no_confirmado"}
            else:
                registrar_evento_usuario(None, "error_login", f"Login fallido para: {email}")
                st.warning("Correo o contraseña incorrectos.")
                return None

        # ✅ Obtener el ID del usuario autenticado
        user_id = getattr(user, "id", None)
        if not user_id:
            st.error("No se pudo obtener el ID del usuario autenticado.")
            registrar_evento_usuario(None, "error_login", f"Error al obtener user_id para: {email}")
            return None

        # 📦 Buscar el perfil del usuario en la tabla 'usuarios'
        resultado = supabase.table("usuarios") \
            .select("*") \
            .eq("user_id", user_id) \
            .limit(1) \
            .execute()

        if resultado.data:
            perfil = resultado.data[0]
            perfil["status"] = "ok"

            # 🔄 Validar plan (y posiblemente actualizarlo si expiró)
            perfil = validar_plan_trial(perfil)

            # 📝 Registrar evento de login exitoso
            registrar_evento_usuario(user_id, "inicio_sesion", "Inicio de sesión exitoso")
            registrar_evento_usuario_test()

            st.write("despues de registrar_evento_usuario")
            st.stop()

            return perfil
        else:
            st.warning("Usuario autenticado pero no tiene perfil registrado.")
            registrar_evento_usuario(user_id, "error_login", "Usuario sin perfil en tabla usuarios")
            return None

    except Exception as e:
        error_str = str(e)
        registrar_evento_usuario(None, "error_login", f"Excepción técnica: {error_str}")

        if "Email not confirmed" in error_str:
            return {"status": "no_confirmado"}

        st.error(f"Error técnico durante el login: {e}")
        return None

def validar_plan_trial(usuario):
    usuario["dias_restantes_trial"] = None
    usuario["dias_transcurridos"] = None
    usuario["fecha_fin_trial"] = None

    if usuario.get("plan_actual") == "Premium_trial":
        fecha_inicio_str = usuario.get("fecha_inicio_trial")
        dias_trial = usuario.get("dias_trial", 7)

        if fecha_inicio_str:
            try:
                # Parseo robusto compatible con ISO 8601 y timestamptz
                fecha_inicio = datetime.fromisoformat(str(fecha_inicio_str)).date()
                hoy = datetime.utcnow().date()

                dias_transcurridos = (hoy - fecha_inicio).days
                usuario["dias_transcurridos"] = dias_transcurridos

                if dias_transcurridos > dias_trial:
                    usuario["plan_actual"] = "Free"
                    usuario["dias_restantes_trial"] = 0
                    usuario["fecha_fin_trial"] = hoy.isoformat()

                    # ✅ Actualiza en Supabase la expiración
                    actualizar_plan_usuario(
                        user_id=usuario["user_id"],
                        nuevo_plan="Free",
                        fecha_fin=hoy.isoformat()
                    )
                else:
                    usuario["dias_restantes_trial"] = dias_trial - dias_transcurridos

            except Exception as e:
                st.warning(f"⚠️ Error en el cálculo de días de trial: {e}")
                usuario["dias_restantes_trial"] = None
                usuario["dias_transcurridos"] = None
                usuario["fecha_fin_trial"] = None

    return usuario

def OLD3login_usuario(email: str, password: str):
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

def OLDvalidar_plan_trial(usuario):
    usuario["dias_restantes_trial"] = None
    usuario["dias_transcurridos"] = None

    if usuario.get("plan_actual") == "Premium_trial":
        fecha_inicio_str = usuario.get("fecha_inicio_trial")
        dias_trial = usuario.get("dias_trial", 7)

        if fecha_inicio_str:
            try:
                fecha_inicio = datetime.fromisoformat(str(fecha_inicio_str).split("T")[0]).date()
                hoy = datetime.today().date()
                dias_transcurridos = (hoy - fecha_inicio).days

                usuario["dias_transcurridos"] = dias_transcurridos

                if dias_transcurridos > dias_trial:
                    usuario["plan_actual"] = "Free"
                    usuario["dias_restantes_trial"] = 0
                    usuario["fecha_fin_trial"] = hoy.isoformat()

                    # ✅ Actualiza en Supabase
                    actualizar_plan_usuario(usuario["user_id"], "Free", hoy.isoformat())
                else:
                    usuario["dias_restantes_trial"] = dias_trial - dias_transcurridos

            except Exception as e:
                usuario["dias_restantes_trial"] = None
                usuario["dias_transcurridos"] = None
                usuario["fecha_fin_trial"] = None
        else:
            usuario["fecha_fin_trial"] = None
    else:
        usuario["fecha_fin_trial"] = None

    return usuario

def OLD5login_usuario(email: str, password: str):
    try:
        # 🔐 Autenticación con Supabase Auth
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        user = auth_response.user

        # ❌ Si no se retorna usuario, validar tipo de error
        if not user:
            error_msg = getattr(auth_response, "error", None)
            if error_msg and "Email not confirmed" in str(error_msg):
                return {"status": "no_confirmado"}
            else:
                st.warning("Correo o contraseña incorrectos.")
                return None

        # ✅ Obtener el ID del usuario autenticado
        user_id = getattr(user, "id", None)
        if not user_id:
            st.error("No se pudo obtener el ID del usuario autenticado.")
            return None

        # 📦 Buscar el perfil del usuario en la tabla 'usuarios'
        resultado = supabase.table("usuarios") \
            .select("*") \
            .eq("user_id", user_id) \
            .limit(1) \
            .execute()

        if resultado.data:
            perfil = resultado.data[0]
            perfil["status"] = "ok"

            # 🔄 Validar plan (y posiblemente actualizarlo si expiró)
            perfil = validar_plan_trial(perfil)

            return perfil
        else:
            st.warning("Usuario autenticado pero no tiene perfil registrado.")
            return None

    except Exception as e:
        error_str = str(e)
        if "Email not confirmed" in error_str:
            return {"status": "no_confirmado"}

        st.error(f"Error técnico durante el login: {e}")
        return None
