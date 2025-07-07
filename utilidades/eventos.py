from supabase import Client
from typing import Optional, Dict
import datetime
import pytz

# Requiere que tengas un cliente Supabase ya creado en tu app
from auth.conexion_supabase import supabase


def registrar_evento_usuario(
    evento: str,
    detalle: Optional[Dict] = None,
    cliente: Optional[Client] = None,
) -> None:
    """
    Registra un evento en la tabla eventos_usuarios.

    Parámetros:
    - evento: nombre del evento (ej. 'inicio_sesion', 'registro', etc.)
    - detalle: diccionario opcional con información adicional (ej. {"archivo": "data.xlsx"})
    - cliente: cliente Supabase opcional (si no se pasa, se usa el global)
    """

    try:
        supa = cliente or supabase
        user = supa.auth.get_user()
        user_id = user.user.id if user and user.user else None

        if not user_id:
            print("⚠️ No se pudo obtener el user_id para registrar el evento.")
            return

        # Hora UTC con precisión
        now = datetime.datetime.now(pytz.UTC)

        data = {
            "user_id": user_id,
            "evento": evento,
            "fecha_evento": now,
            "detalle": detalle or {}
        }

        resp = supa.table("eventos_usuarios").insert(data).execute()
        if resp.error:
            print("❌ Error al registrar evento:", resp.error)
        else:
            print("✅ Evento registrado:", evento)

    except Exception as e:
        print("❌ Excepción al registrar evento:", str(e))
