from datetime import datetime
from auth.conexion_supabase import supabase
from datetime import datetime, timedelta, timezone

def registrar_evento_usuario(user_id: str, tipo_evento: str, descripcion: str = ""):
    try:
        evento = {
            "user_id": user_id,
            "tipo_evento": tipo_evento,
            "descripcion": descripcion,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        respuesta = supabase.table("eventos_usuarios").insert([evento]).execute()

        if respuesta.status_code != 201:
            print("❌ Error registrando evento:", respuesta.data)
        else:
            print(f"✅ Evento '{tipo_evento}' registrado.")
    except Exception as e:
        print(f"❌ Excepción al registrar evento: {e}")
