from auth.conexion_supabase import supabase
from database.usuarios import guardar_perfil_usuario
from datetime import datetime
import streamlit as st
from utilidades.mensajes import mostrar_mensaje_confirmacion

def insertar_perfil_post_signup():
    try:
        params = st.query_params
        access_token = params.get("access_token")
        recovery_type = params.get("type")

        if not access_token or recovery_type != "signup":
            return {"status": "error", "mensaje": "Token inválido o tipo incorrecto."}

        session_response = supabase.auth.set_session(access_token, access_token)

        if not session_response.session:
            return {"status": "error", "mensaje": "⚠ Sesión inactiva. No se pudo crear perfil."}

        user = session_response.user
        if not user:
            return {"status": "error", "mensaje": "⚠ No se obtuvo el usuario."}

        perfil = {
            "user_id": user.id,
            "nombre": user.user_metadata.get("nombre", "Sin nombre"),
            "email": user.email,
            "plan_actual": "Premium_trial",
            "fecha_inicio_trial": datetime.now().strftime("%Y-%m-%d"),
            "dias_trial": 7
        }

        exito = guardar_perfil_usuario(perfil)
        if not exito:
            return {"status": "error", "mensaje": "❌ No se pudo guardar el perfil."}

        mostrar_mensaje_confirmacion(
            titulo="🎉 ¡Registro confirmado!",
            mensaje="Tu perfil ha sido creado exitosamente. Ya puedes iniciar sesión."
        )

        return {"status": "ok"}

    except Exception as e:
        return {"status": "error", "mensaje": str(e)}


# from auth.conexion_supabase import supabase
# from database.usuarios import guardar_perfil_usuario
# from datetime import datetime
# import streamlit as st
# from utilidades.mensajes import mostrar_mensaje_exito
#
# def insertar_perfil_post_signup():
#     try:
#         params = st.query_params
#         access_token = params.get("access_token")
#         recovery_type = params.get("type")
#
#
#         if not access_token or recovery_type != "signup":
#             return {"status": "error", "mensaje": "Token inválido o tipo incorrecto."}
#
#         # ✅ Activar sesión manualmente usando el token
#         session_response = supabase.auth.set_session(access_token, access_token)
#
#         if not session_response.session:
#             return {"status": "error", "mensaje": "⚠ Sesión inactiva. No se pudo crear perfil."}
#
#         user = session_response.user
#         if not user:
#             return {"status": "error", "mensaje": "⚠ No se obtuvo el usuario."}
#
#         perfil = {
#             "user_id": user.id,
#             "nombre": user.user_metadata.get("nombre", "Sin nombre"),
#             "email": user.email,
#             "plan_actual": "Premium_trial",
#             "fecha_inicio_trial": datetime.now().strftime("%Y-%m-%d"),
#             "dias_trial": 7
#         }
#
#         exito = guardar_perfil_usuario(perfil)
#
#         if not exito:
#             return {"status": "error", "mensaje": "❌ No se pudo guardar el perfil."}
#
#         # 🎉 Mostrar mensaje elegante
#         mostrar_mensaje_exito(
#             titulo="🎉 ¡Registro confirmado!",
#             mensaje="Tu perfil ha sido creado exitosamente. Ya puedes iniciar sesión."
#         )
#
#         return {"status": "ok"}
#
#     except Exception as e:
#         return {"status": "error", "mensaje": str(e)}
#
