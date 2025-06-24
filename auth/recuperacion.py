from auth.conexion_supabase import supabase

def OLDenviar_correo_recuperacion(email):
    try:
        respuesta = supabase.auth.reset_password_for_email(email)
        print("Respuesta Supabase:", respuesta)
        return respuesta
    except Exception as e:
        print("❌ Error al enviar recuperación:", e)
        return None

def enviar_correo_recuperacion(email):
    try:
        print("email",email)
        resultado = supabase.auth.api.reset_password_for_email(email)
        print("Resultado:", resultado)
        return resultado
    except Exception as e:
        print("ERROR real:", e)
        raise e  # para que lo veas también en Streamlit