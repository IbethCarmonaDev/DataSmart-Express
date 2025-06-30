############################################################
# Creador por: Ibeth Carmona.Jun 25-2025
# Opcion para registrar los Usuarios nuevos en Supabase
############################################################
from auth.conexion_supabase import supabase
from datetime import datetime
from database.usuarios import guardar_perfil_usuario

from auth.conexion_supabase import supabase

def registrar_usuario(nombre, correo, password):
    try:
        # 1. Solo crear usuario en Auth y enviar correo de verificación
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
            return {"status": "error", "mensaje": "No se pudo crear el usuario"}

        return {"status": "ok"}

    except Exception as e:
        return {"status": "error", "mensaje": str(e)}



