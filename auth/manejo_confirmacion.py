from auth.conexion_supabase import supabase
from database.usuarios import guardar_perfil_usuario
from datetime import datetime
import streamlit as st
from utilidades.mensajes import mostrar_mensaje_exito

def insertar_perfil_post_signup():
    try:
        params = st.query_params
        access_token = params.get("access_token")
        recovery_type = params.get("type")

        if not access_token or recovery_type != "signup":
            return {"status": "error", "mensaje": "Token inválido o tipo incorrecto."}

        # ✅ Activar sesión manualmente usando el token
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

        # 🎉 Mostrar mensaje elegante
        mostrar_mensaje_exito(
            titulo="🎉 ¡Registro confirmado!",
            mensaje="Tu perfil ha sido creado exitosamente. Ya puedes iniciar sesión."
        )

        return {"status": "ok"}

    except Exception as e:
        return {"status": "error", "mensaje": str(e)}


# import streamlit as st
# from datetime import datetime
# from PIL import Image
# from auth.conexion_supabase import supabase
# from database.usuarios import guardar_perfil_usuario
#
# def insertar_perfil_post_signup():
#     try:
#         params = st.query_params
#         access_token = params.get("access_token")
#         recovery_type = params.get("type")
#
#         if not access_token or recovery_type != "signup":
#             return {"status": "error", "mensaje": "Token inválido o tipo incorrecto."}
#
#         # ✅ Activar sesión con el token (ambos parámetros son el mismo)
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
#         if not guardar_perfil_usuario(perfil):
#             return {"status": "error", "mensaje": "❌ No se pudo guardar el perfil del usuario."}
#
#         mostrar_mensaje_exito()
#         return {"status": "ok"}
#
#     except Exception as e:
#         return {"status": "error", "mensaje": str(e)}
#
#
# def mostrar_mensaje_exito():
#     col1, col2 = st.columns([1, 4])
#
#     with col1:
#         try:
#             logo = Image.open("Logo.png")
#             st.image(logo, width=100)
#         except:
#             st.write("")
#
#     with col2:
#         st.markdown("""
#         <div style='padding: 1rem; border-radius: 10px; background-color: #e6f7ff; border: 1px solid #91d5ff;'>
#             <h3 style='color: #1890ff;'>✅ Registro confirmado con éxito</h3>
#             <p>Tu cuenta ha sido activada y tu perfil fue creado correctamente.</p>
#             <p>Puedes iniciar sesión con tus credenciales para comenzar a usar DataSmart Express.</p>
#             <a href="?reload=true" style='color: #1890ff; font-weight: bold;'>🔐 Iniciar sesión</a>
#         </div>
#         """, unsafe_allow_html=True)
