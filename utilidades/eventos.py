from datetime import datetime

import streamlit

from auth.conexion_supabase import supabase
from datetime import datetime, timedelta, timezone

def registrar_evento_usuario(user_id: str, tipo_evento: str, descripcion: str = ""):
    try:

        streamlit.write("entró a registrar_evento_usuario")

        # evento = {
        #     "user_id": user_id,
        #     "tipo_evento": tipo_evento,
        #     "detalle": {"mensaje": descripcion},
        #     "timestamp": datetime.now(timezone.utc).isoformat()
        # }

        fecha_actual_utc = datetime.now(timezone.utc)
        fecha_actual_str = fecha_actual_utc.isoformat()

        evento = {
            "user_id": "UID_DE_PRUEBA",  # Reemplaza con un UID real de un usuario
            "evento": "prueba_manual",
            "detalle": {"mensaje": "Evento insertado manualmente"},
            "fecha_evento": fecha_actual_str


        }



        respuesta = supabase.table("eventos_usuarios").insert([evento]).execute()

        streamlit.write("antes de write respuesta")
        streamlit.write("respuesta:", respuesta.model_dump())
        print("📤 Supabase response:", respuesta.model_dump())

        if respuesta.status_code != 201:
            streamlit.error(f"❌ Error Supabase: {respuesta.status_code} - {respuesta.data}")
        else:
            streamlit.success("✅ Evento insertado correctamente")

        if respuesta.status_code != 201:
            print("❌ Error registrando evento:", respuesta.data)
        else:
            print(f"✅ Evento '{tipo_evento}' registrado.")


    except Exception as e:
        print(f"❌ Excepción al registrar evento: {e}")
