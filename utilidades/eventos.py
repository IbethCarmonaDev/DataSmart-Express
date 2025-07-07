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
    También ejecuta una función RPC para eliminar eventos antiguos.
    """

    try:
        session = supabase.auth.get_session()
        if not session or not session.access_token or not session.user:
            #st.warning("⚠️ No hay sesión activa. No se registró el evento.")
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
