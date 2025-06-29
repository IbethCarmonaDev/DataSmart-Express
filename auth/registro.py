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

def OLD3registrar_usuario(nombre, correo, password):
    try:
        # 1. Crear usuario en Auth
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
            return {"status": "error", "mensaje": "Error creando el usuario"}

        # 2. Forzar login después del sign_up para activar la sesión
        login_response = supabase.auth.sign_in_with_password({
            "email": correo,
            "password": password
        })

        if not login_response.session:
            return {"status": "error", "mensaje": "Login fallido. No se activó la sesión."}

        # 3. Obtener el user_id con sesión activa (para RLS)
        user = supabase.auth.get_user()
        if not user or not user.user:
            return {"status": "error", "mensaje": "Sesión no activa. No se puede guardar perfil."}

        user_id = user.user.id

        # 4. Guardar en tabla 'usuarios'
        perfil = {
            "user_id": user_id,
            "nombre": nombre,
            "email": correo,
            "plan_actual": "Premium_trial",
            "fecha_inicio_trial": datetime.now().strftime("%Y-%m-%d"),
            "dias_trial": 7
        }

        guardar_perfil_usuario(perfil)

        return {"status": "ok"}

    except Exception as e:
        return {"status": "error", "mensaje": str(e)}


