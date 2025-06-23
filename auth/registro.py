from auth.conexion_supabase import supabase
from auth.utils import hash_password

def registrar_usuario(nombre, email, password):
    try:
        # 1️⃣ Validar si ya existe en tu tabla personalizada
        respuesta = supabase.table("usuarios").select("email").eq("email", email).execute()
        if respuesta.data and len(respuesta.data) > 0:
            return {"error": "Este correo ya está registrado en el sistema."}

        # 2️⃣ Validar si ya existe en Supabase Auth
        try:
            supabase.auth.sign_in_with_password({
                "email": email,
                "password": password  # Supabase devuelve error si el usuario no existe
            })
            return {"error": "Este correo ya tiene cuenta en Supabase Auth."}
        except Exception:
            pass  # Si lanza error, asumimos que el usuario no existe aún

        # 3️⃣ Crear en Supabase Auth
        auth_response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "nombre": nombre,
                    "plan_actual": "Free"
                }
            }
        })

        if not auth_response.user:
            return {"error": "Error al registrar en Supabase Auth."}

        # 4️⃣ Crear en tu tabla `usuarios`
        password_hash = hash_password(password)
        data = {
            "id_auth": auth_response.user.id,
            "nombre": nombre,
            "email": email,
            "contrasena_hash": password_hash,
            "plan_actual": "Free"
        }

        supabase.table("usuarios").insert(data).execute()
        return {"exito": True, "usuario": auth_response.user}

    except Exception as e:
        print("❌ Error inesperado:", e)
        return {"error": str(e)}
