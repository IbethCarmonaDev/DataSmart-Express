# auth/login.py

from auth.conexion_supabase import supabase
from auth.utils import hash_password


def login_usuario(email: str, password: str):
    password_hash = hash_password(password)

    response = supabase.table("usuarios") \
        .select("*") \
        .eq("email", email) \
        .eq("contrasena_hash", password_hash) \
        .execute()

    if response.data:
        return response.data[0]  # Usuario válido
    else:
        return None  # Login fallido
