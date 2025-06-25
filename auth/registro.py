############################################################
# Creador por: Ibeth Carmona.Jun 25-2025
# Opcion para registrar los Usuarios nuevos en Supabase
############################################################
from auth.conexion_supabase import supabase
from datetime import datetime
from database.usuarios import guardar_perfil_usuario

def registrar_usuario(nombre, correo, password):
    try:
        # 1. Crear cuenta en Supabase Auth
        response = supabase.auth.sign_up({
            "email": correo,
            "password": password
        })

        if response.user is None:
            return {"status": "error", "mensaje": str(response)}

        user_id = response.user.id

        # 2. Guardar perfil extendido en tabla personalizada
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
