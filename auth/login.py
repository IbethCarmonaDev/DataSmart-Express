from auth.conexion_supabase import supabase

def login_usuario(email: str, password: str):
    try:
        # Autenticación con correo y contraseña
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        user = auth_response.user
        if not user:
            return None  # Login fallido

        # Buscar datos en la tabla personalizada usando el user_id (no email)
        perfil = supabase.table("usuarios").select("*").eq("user_id", user.id).single().execute()
        if perfil.data:
            return perfil.data
        else:
            return None  # Usuario autenticado pero sin perfil asociado

    except Exception as e:
        print("Error de autenticación:", e)
        return None


# from auth.conexion_supabase import supabase
#
# def login_usuario(email: str, password: str):
#     try:
#         auth_response = supabase.auth.sign_in_with_password({
#             "email": email,
#             "password": password
#         })
#
#         user = auth_response.user
#         if not user:
#             return None  # Login fallido
#
#         # Buscar datos adicionales en tu tabla "usuarios"
#         perfil = supabase.table("usuarios").select("*").eq("email", email).single().execute()
#         if perfil.data:
#             return perfil.data  # Usuario válido con datos adicionales
#         else:
#             return None  # Usuario autenticado pero sin datos en tu tabla personalizada
#
#     except Exception as e:
#         print("Error de autenticación:", e)
#         return None
#
