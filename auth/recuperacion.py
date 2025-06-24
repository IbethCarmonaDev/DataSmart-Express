from auth.conexion_supabase import supabase

def enviar_correo_recuperacion(email):
    try:
        print("email",email)
        resultado = supabase.auth.reset_password_for_email(email)
        print("Resultado:", resultado)
        return resultado
    except Exception as e:
        print("ERROR real:", e)
        raise e  # para que lo veas también en Streamlit