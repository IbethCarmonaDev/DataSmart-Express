from database.usuarios import actualizar_plan_usuario
from datetime import datetime
import streamlit as st
from auth.conexion_supabase import supabase
from utilidades.eventos import registrar_evento_usuario


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
                registrar_evento_usuario("login_fallido_no_confirmado", {"email": email})
                return {"status": "no_confirmado"}
            else:
                registrar_evento_usuario("login_fallido_credenciales", {"email": email})
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

            registrar_evento_usuario("login_exitoso", {"email": email, "plan": perfil.get("plan_actual", "Desconocido")})

            # 🔄 Validar plan (y posiblemente actualizarlo si expiró)
            perfil = validar_plan_trial(perfil)

            return perfil
        else:
            registrar_evento_usuario("login_sin_perfil", {"user_id": user_id, "email": email})
            st.warning("Usuario autenticado pero no tiene perfil registrado.")
            return None

    except Exception as e:
        error_str = str(e)

        if "Email not confirmed" in error_str:
            registrar_evento_usuario("login_fallido_no_confirmado", {"email": email})
            return {"status": "no_confirmado"}

        registrar_evento_usuario("login_error_tecnico", {"email": email, "error": error_str})
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

                    actualizar_plan_usuario(
                        user_id=usuario["user_id"],
                        nuevo_plan="Free",
                        fecha_fin=hoy.isoformat()
                    )

                    registrar_evento_usuario("trial_expirado", {
                        "user_id": usuario["user_id"],
                        "dias_trial": dias_trial,
                        "fecha_expiracion": hoy.isoformat()
                    })

                else:
                    usuario["dias_restantes_trial"] = dias_trial - dias_transcurridos

            except Exception as e:
                st.warning(f"⚠️ Error en el cálculo de días de trial: {e}")
                usuario["dias_restantes_trial"] = None
                usuario["dias_transcurridos"] = None
                usuario["fecha_fin_trial"] = None

    return usuario
