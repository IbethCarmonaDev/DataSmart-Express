from supabase import Client
from typing import Optional, Dict
import datetime
import pytz

import requests
from datetime import datetime, timezone
datetime.now(timezone.utc)
from auth.conexion_supabase import supabase, SUPABASE_URL, SUPABASE_KEY
import streamlit as st
from datetime import datetime, timezone



def registrar_evento_usuario(evento: str, detalle: dict = None):
    """
    Registra un evento para el usuario autenticado en Supabase (tabla: eventos_usuarios).
    Requiere:
    - La política RLS debe permitir: user_id = auth.uid()
    - El campo user_id debe estar presente y coincidir con el usuario autenticado
    """

    try:
        session = supabase.auth.get_session()
        if not session or not session.access_token or not session.user:
            st.warning("⚠️ No hay sesión activa. No se registró el evento.")
            return

        access_token = session.access_token
        user_id = session.user.id

        payload = {
            "user_id": user_id,
            "evento": evento,
            "fecha_evento": datetime.now(timezone.utc).isoformat(),
            "detalle": detalle or {}
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "apikey": SUPABASE_KEY,
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }

        url = f"{SUPABASE_URL}/rest/v1/eventos_usuarios"
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code in [200, 201]:
            print(f"✅ Evento '{evento}' registrado con éxito.")
        else:
            st.warning(f"⚠️ No se pudo registrar el evento ({response.status_code})")
            st.code(response.text)

    except Exception as e:
        st.error(f"❌ Error registrando evento: {e}")


def oldregistrar_evento_usuario(
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
