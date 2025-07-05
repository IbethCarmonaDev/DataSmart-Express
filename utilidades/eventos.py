from datetime import datetime

import streamlit

from auth.conexion_supabase import supabase
from datetime import datetime, timedelta, timezone

def registrar_evento_usuario_test():
    import streamlit as st
    import requests
    from datetime import datetime
    from auth.conexion_supabase import supabase
    import os

    try:
        st.write("🔍 Ejecutando test manual de inserción...")

        # 🔐 Obtener sesión y verificar que esté activa
        session = supabase.auth.get_session()
        if not session or not session.access_token:
            st.error("❌ No se encontró una sesión activa o el token está ausente.")
            return

        access_token = session.access_token
        user_id = session.user.id

        st.write("🧾 user_id:", user_id)

        # 🌍 Leer SUPABASE_URL y SUPABASE_KEY
        if "SUPABASE_URL" in st.secrets:
            SUPABASE_URL = st.secrets["SUPABASE_URL"]
            SUPABASE_KEY = st.secrets["SUPABASE_KEY"]  # ✅ Debe ser la clave `anon`
        else:
            from dotenv import load_dotenv
            load_dotenv()
            SUPABASE_URL = os.getenv("SUPABASE_URL")
            SUPABASE_KEY = os.getenv("SUPABASE_KEY")

        # ⚠️ Validación rápida: advertencia si se usa la clave service_role
        if SUPABASE_KEY and SUPABASE_KEY.startswith("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"):  # solo detecta algunas
            st.warning("⚠️ Asegúrate de usar la API Key 'anon' (pública), no 'service_role'.")

        # 📡 Inserción manual con token
        url = f"{SUPABASE_URL}/rest/v1/eventos_usuarios"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }

        payload = {
            "user_id": user_id,
            "evento": "inicio_sesion",
            "fecha_evento": datetime.now().isoformat()
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code in (200, 201):
            st.success("✅ Inserción con token exitosa")
            st.write(response.json())
        else:
            st.error(f"❌ Error al insertar: {response.status_code}")
            st.code(response.text)

    except Exception as e:
        st.error(f"❌ Excepción: {e}")


def OLD40registrar_evento_usuario_test():
    import streamlit as st
    import requests
    from datetime import datetime
    from auth.conexion_supabase import supabase
    import os

    try:
        st.write("🔍 Ejecutando test manual de inserción...")

        # 🔐 Obtener sesión actual
        session = supabase.auth.get_session()

        if not session or not session.user:
            st.warning("⚠️ No hay sesión activa. Espera unos segundos o vuelve a iniciar sesión.")
            return

        access_token = session.access_token
        user_id = session.user.id

        st.write("📤 user_id:", user_id)

        # 🌍 Leer SUPABASE_URL y SUPABASE_KEY
        if "SUPABASE_URL" in st.secrets:
            SUPABASE_URL = st.secrets["SUPABASE_URL"]
            SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
        else:
            from dotenv import load_dotenv
            load_dotenv()
            SUPABASE_URL = os.getenv("SUPABASE_URL")
            SUPABASE_KEY = os.getenv("SUPABASE_KEY")

        # 📡 Inserción manual con token
        url = f"{SUPABASE_URL}/rest/v1/eventos_usuarios"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }

        payload = {
            "user_id": user_id,
            "evento": "inicio_sesion",
            "fecha_evento": datetime.now().isoformat()
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code in (200, 201):
            st.success("✅ Inserción con token exitosa")
            st.write(response.json())
        else:
            st.error(f"❌ Error al insertar: {response.status_code}")
            st.code(response.text)

    except Exception as e:
        st.error(f"❌ Excepción: {e}")


def OL5registrar_evento_usuario_test():
    import streamlit as st
    import requests
    from datetime import datetime
    from auth.conexion_supabase import supabase
    import os


    try:
        st.write("🔍 Ejecutando test manual de inserción...")

        # 🔐 Obtener sesión y token
        session = supabase.auth.get_session()
        access_token = session.access_token
        user_id = session.user.id

        st.write("📤 user_id:", user_id)

        # 🌍 Leer SUPABASE_URL y SUPABASE_KEY
        if "SUPABASE_URL" in st.secrets:
            SUPABASE_URL = st.secrets["SUPABASE_URL"]
            SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
        else:
            from dotenv import load_dotenv
            load_dotenv()
            SUPABASE_URL = os.getenv("SUPABASE_URL")
            SUPABASE_KEY = os.getenv("SUPABASE_KEY")

        # 📡 Inserción manual con token
        url = f"{SUPABASE_URL}/rest/v1/eventos_usuarios"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }


        payload = {
            "user_id": user_id,
            "evento": "inicio_sesion",
            "fecha_evento": datetime.now().isoformat()
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code in (200, 201):
            st.success("✅ Inserción con token exitosa")
            st.write(response.json())
        else:
            st.error(f"❌ Error al insertar: {response.status_code}")
            st.code(response.text)

    except Exception as e:
        st.error(f"❌ Excepción: {e}")

def OLDregistrar_evento_usuario_test():
    import streamlit as st
    from auth.conexion_supabase import supabase
    from datetime import datetime, timezone

    try:
        st.write("🔍 Ejecutando test manual de inserción...")

        user_id = supabase.auth.get_user().user.id  # ✅ Obtiene el UID del usuario autenticado
        st.write("📤 user_id:", user_id)

        session = supabase.auth.get_session()
        st.write("Rol activo:", session)

        from supabase import create_client


        user_id = session.user.id

        st.write("user_id:", user_id)
        st.write("Tipo:", type(user_id))
        st.write("Rol activo:", supabase.auth.get_session())

        from supabase import create_client

        # Asume que ya hiciste login y tienes la sesión
        session = supabase.auth.get_session()
        access_token = session.access_token

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

        # 💡 Re-crear el cliente con el token activo del usuario
        supabase_autenticado = create_client(SUPABASE_URL, SUPABASE_KEY, options={
            "global": {
                "headers": {
                    "Authorization": f"Bearer {access_token}"
                }
            }
        })

        # ✅ Ahora usa este cliente para insertar
        supabase_autenticado.table("eventos_usuarios").insert({
            "user_id": session.user.id,
            "evento": "inicio_sesion",
            "fecha_evento": datetime.now().isoformat()
        }).execute()

        #
        # evento = {
        #     "user_id": user_id,  # 👈 Usa un user_id real de la tabla usuarios
        #     "evento": "test_insercion_manual",
        #     "detalle": {"mensaje": "Test desde función aislada"},
        #     "fecha_evento": datetime.now(timezone.utc).isoformat()
        # }
        #
        #
        # respuesta = supabase.table("eventos_usuarios").insert([evento]).execute()
        #
        # st.write("📤 Respuesta Supabase:", respuesta.model_dump())

        # if respuesta.status_code != 201:
        #     st.error(f"❌ Error Supabase: {respuesta.status_code} - {respuesta.data}")
        # else:
        #     st.success("✅ Inserción de prueba exitosa")

    except Exception as e:
        st.error(f"❌ Excepción al registrar evento: {e}")


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
