from auth.conexion_supabase import supabase

def login_usuario(email: str, password: str):
    try:
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        user = auth_response.user
        if not user:
            return None  # Login fallido

        # Buscar datos adicionales en tu tabla "usuarios"
        perfil = supabase.table("usuarios").select("*").eq("email", email).single().execute()
        if perfil.data:
            return perfil.data  # Usuario válido con datos adicionales
        else:
            return None  # Usuario autenticado pero sin datos en tu tabla personalizada

    except Exception as e:
        print("Error de autenticación:", e)
        return None

# # auth/login.py
#
# from auth.conexion_supabase import supabase
# from auth.utils import hash_password
#
#
# def login_usuario(email: str, password: str):
#     password_hash = hash_password(password)
#
#     response = supabase.table("usuarios") \
#         .select("*") \
#         .eq("email", email) \
#         .eq("contrasena_hash", password_hash) \
#         .execute()
#
#     if response.data:
#         return response.data[0]  # Usuario válido
#     else:
#         return None  # Login fallido



