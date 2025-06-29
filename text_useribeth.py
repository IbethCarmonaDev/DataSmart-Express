from auth.conexion_supabase import supabase
from datetime import datetime

# Datos de prueba
user_id = "ce33854d-7442-485e-acab-aadada5392b0"
nombre = "IBETH CARMONA 22"
correo = "ibethc+22@hotmail.com"

perfil = {
    "user_id": user_id,
    "nombre": nombre,
    "email": correo,
    "plan_actual": "Premium_trial",
    "fecha_inicio_trial": datetime.now().strftime("%Y-%m-%d"),
    "dias_trial": 7
}

# Intentar inserción manual
respuesta = supabase.table("usuarios").insert(perfil).execute()
print("✅ Resultado inserción manual:", respuesta)
