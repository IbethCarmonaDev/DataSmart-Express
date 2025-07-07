from supabase import create_client
import os
import streamlit as st

# Detectar entorno y obtener las variables
if "SUPABASE_URL" in st.secrets:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
else:
    from dotenv import load_dotenv
    load_dotenv()
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")


# Crear cliente de Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Crear cliente con token personalizado (para RLS con auth.uid)
def crear_cliente_autenticado(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    return create_client(SUPABASE_URL, SUPABASE_KEY, options={"headers": headers})

