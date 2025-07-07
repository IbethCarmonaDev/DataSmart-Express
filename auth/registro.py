############################################################
# Registro de nuevos usuarios en Supabase con validaciones
# Creado por Ibeth Carmona - Mejorado con mensajes visuales y eventos
############################################################
import re
import streamlit as st
from auth.conexion_supabase import supabase
from database.usuarios import guardar_perfil_usuario
from utilidades.errores_supabase import obtener_mensaje_error
from utilidades.eventos import registrar_evento_usuario
from utilidades.mensajes import mostrar_mensaje_confirmacion

# -------------------- Validaciones --------------------

def es_email_valido(email: str) -> bool:
    patron = r"^[\w\.\+-]+@[\w\.-]+\.\w+$"
    return re.match(patron, email) is not None

def es_password_valida(password: str) -> bool:
    return len(password) >= 6  # Puedes hacerla más exigente si deseas

# -------------------- Registro --------------------

def registrar_usuario(nombre, correo, password, idioma="es"):
    try:
        # 🛡 Validar formato de correo
        if not es_email_valido(correo):
            registrar_evento_usuario("registro_email_invalido", {"email": correo})
            mostrar_mensaje_confirmacion(
                titulo="Correo inválido",
                mensaje=obtener_mensaje_error("invalid_email_format", idioma),
                tipo="warning"
            )
            return {"status": "error"}

        # 🔐 Validar fortaleza mínima de contraseña
        if not es_password_valida(password):
            registrar_evento_usuario("registro_password_debil", {"email": correo})
            mostrar_mensaje_confirmacion(
                titulo="Contraseña débil",
                mensaje=obtener_mensaje_error("weak_password", idioma),
                tipo="warning"
            )
            return {"status": "error"}

        # 🚀 Crear usuario en Supabase Auth
        signup_response = supabase.auth.sign_up({
            "email": correo,
            "password": password,
            "options": {
                "data": {
                    "nombre": nombre
                }
            }
        })

        if signup_response.user is None:
            registrar_evento_usuario("registro_usuario_duplicado", {"email": correo})
            mostrar_mensaje_confirmacion(
                titulo="Usuario ya registrado",
                mensaje=obtener_mensaje_error("user_exists", idioma),
                tipo="warning"
            )
            return {"status": "error"}

        registrar_evento_usuario("registro_exitoso", {"email": correo})
        mostrar_mensaje_confirmacion(
            titulo="Registro exitoso",
            mensaje="🎉 Tu cuenta ha sido creada correctamente. Revisa tu correo para confirmar tu email.",
            tipo="success"
        )
        return {"status": "ok"}

    except Exception as e:
        # 🧠 Mapear errores conocidos
        error_str = str(e).lower()
        if "invalid email" in error_str or "invalid format" in error_str:
            clave = "invalid_email_format"
        elif "user already registered" in error_str or "user exists" in error_str:
            clave = "user_exists"
        elif "weak password" in error_str:
            clave = "weak_password"
        else:
            clave = None

        registrar_evento_usuario("registro_error", {"email": correo, "error": error_str})

        mensaje = obtener_mensaje_error(clave, idioma) if clave else f"❌ Error: {e}"
        mostrar_mensaje_confirmacion(
            titulo="Error en el registro",
            mensaje=mensaje,
            tipo="error"
        )
        return {"status": "error"}


# ############################################################
# # Registro de nuevos usuarios en Supabase con validaciones
# # Creado por Ibeth Carmona - Mejorado con validaciones
# ############################################################
# import streamlit
#
# from auth.conexion_supabase import supabase
# from database.usuarios import guardar_perfil_usuario
# from utilidades.errores_supabase import obtener_mensaje_error
# import re
#
# def es_email_valido(email: str) -> bool:
#     patron = r"^[\w\.\+-]+@[\w\.-]+\.\w+$"
#     return re.match(patron, email) is not None
#
# def es_password_valida(password: str) -> bool:
#     return len(password) >= 6  # Puedes hacerla más exigente si quieres
#
#
# def registrar_usuario(nombre, correo, password, idioma="es"):
#     try:
#         # 🛡 Validar formato de correo
#         if not es_email_valido(correo):
#             return {"status": "error", "mensaje": obtener_mensaje_error("invalid_email_format", idioma)}
#
#         # 🔐 Validar fortaleza mínima de contraseña
#         if not es_password_valida(password):
#             return {"status": "error", "mensaje": obtener_mensaje_error("weak_password", idioma)}
#
#         # 🚀 Crear usuario en Supabase Auth
#         signup_response = supabase.auth.sign_up({
#             "email": correo,
#             "password": password,
#             "options": {
#                 "data": {
#                     "nombre": nombre
#                 }
#             }
#         })
#
#         if signup_response.user is None:
#             return {"status": "error", "mensaje": obtener_mensaje_error("user_exists", idioma)}
#
#         return {"status": "ok"}
#
#     except Exception as e:
#         # 🧠 Mapear errores conocidos
#         error_str = str(e).lower()
#         if "invalid email" in error_str or "invalid format" in error_str:
#             clave = "invalid_email_format"
#         elif "user already registered" in error_str or "user exists" in error_str:
#             clave = "user_exists"
#         elif "weak password" in error_str:
#             clave = "weak_password"
#         else:
#             clave = None
#
#         mensaje = obtener_mensaje_error(clave, idioma) if clave else f"❌ Error: {e}"
#         return {"status": "error", "mensaje": mensaje}
