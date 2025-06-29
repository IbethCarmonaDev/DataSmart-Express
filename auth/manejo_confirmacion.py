from auth.conexion_supabase import supabase
from database.usuarios import guardar_perfil_usuario
from datetime import datetime

def insertar_perfil_post_signup():
    try:
        session = supabase.auth.get_session()
        if not session or not session.access_token:
            return {"status": "error", "mensaje": "Sesión inactiva. No se puede crear perfil."}

        # Asegurar sesión activa con token (opcional si ya lo tienes activo)
        token = session.access_token
        supabase.auth.set_session(token, token)

        user = supabase.auth.get_user()
        if not user or not user.user:
            return {"status": "error", "mensaje": "No se pudo obtener el usuario autenticado."}

        user_id = user.user.id
        email = user.user.email
        nombre = user.user.user_metadata.get("nombre", "Usuario")

        # Verificar si ya tiene perfil
        ya_existe = supabase.table("usuarios").select("*").eq("user_id", user_id).execute()
        if ya_existe.data:
            return {"status": "error", "mensaje": "Ya habías confirmado tu cuenta."}

        perfil = {
            "user_id": user_id,
            "nombre": nombre,
            "email": email,
            "plan_actual": "Premium_trial",
            "fecha_inicio_trial": datetime.now().strftime("%Y-%m-%d"),
            "dias_trial": 7
        }

        guardar_perfil_usuario(perfil)
        return {"status": "ok"}

    except Exception as e:
        return {"status": "error", "mensaje": str(e)}
