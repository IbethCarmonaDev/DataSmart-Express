from datetime import datetime

import streamlit

import streamlit as st
import requests
from datetime import datetime
from auth.conexion_supabase import supabase

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

        # 🔐 Obtener sesión actual del usuario autenticado
        session = supabase.auth.get_session()
        if not session or not session.access_token or not session.user:
            st.error("❌ No se encontró una sesión activa válida.")
            return

        access_token = session.access_token
        user_id = session.user.id
        st.write("🧾 user_id:", user_id)
        st.write("🧾 access_token :", access_token )

        st.code(access_token)  # 👈 AQUI



        # Leer las variables desde secrets o .env
        if "SUPABASE_URL" in st.secrets:
            SUPABASE_URL = st.secrets["SUPABASE_URL"]
            SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
        else:
            from dotenv import load_dotenv
            load_dotenv()
            SUPABASE_URL = os.getenv("SUPABASE_URL")
            SUPABASE_KEY = os.getenv("SUPABASE_KEY")

        # Validación rápida
        if SUPABASE_KEY and "service_role" in SUPABASE_KEY:
            st.warning("⚠️ No uses la 'service_role' aquí. Usa la clave pública 'anon'.")

        # 🔁 Payload incluyendo el user_id
        payload = {
            "user_id": user_id,
            "evento": "inicio_sesion",
            "fecha_evento": datetime.now().isoformat()
        }

        # 📡 Realizar inserción
        url = f"{SUPABASE_URL}/rest/v1/eventos_usuarios"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
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

from auth.conexion_supabase import supabase

def registrar_evento_con_lib():
    import streamlit as st
    from datetime import datetime

    try:
        session = supabase.auth.get_session()
        if not session or not session.user:
            st.error("❌ No hay sesión activa.")
            return

        user_id = session.user.id
        st.write("🧾 user_id:", user_id)

        # Inserción usando la librería oficial
        data = {
            "user_id": user_id,
            "evento": "inicio_sesion",
            "fecha_evento": datetime.now().isoformat()
        }

        #result = supabase.table("eventos_usuarios").insert(data).execute()from auth.conexion_supabase import crear_cliente_autenticado

        from auth.conexion_supabase import crear_cliente_autenticado

        session = supabase.auth.get_session()
        if not session or not session.access_token or not session.user:
            st.error("❌ No se encontró una sesión activa válida.")
            return

        access_token = session.access_token

        cliente = crear_cliente_autenticado(access_token)
        result = cliente.table("eventos_usuarios").insert(data).execute()

        if result.status_code in [200, 201]:
            st.success("✅ Inserción con Supabase Client exitosa")
            st.write(result.data)
        else:
            st.error(f"❌ Error al insertar: {result.status_code}")
            st.code(result)

    except Exception as e:
        st.error(f"❌ Excepción: {e}")


def registrar_evento_usuario_requests():
    st.write("🔍 Test de inserción manual con token")

    session = supabase.auth.get_session()
    if not session or not session.access_token or not session.user:
        st.error("❌ No hay sesión válida")
        return

    access_token = session.access_token
    user_id = session.user.id
    st.write("🧾 user_id:", user_id)

    # ⚠️ Cargar URL desde cliente actual (o manual si prefieres)
    SUPABASE_URL = supabase._supabase_url

    payload = {
        "user_id": user_id,
        "evento": "inicio_sesion",
        "fecha_evento": datetime.now().isoformat()
    }

    headers = {
        "Authorization": f"Bearer {access_token}",  # ⚠️ Solo esto, sin apikey
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    url = f"{SUPABASE_URL}/rest/v1/eventos_usuarios"
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code in (200, 201):
        st.success("✅ Inserción exitosa con token")
        st.write(response.json())
    else:
        st.error(f"❌ Error {response.status_code}")
        st.code(response.text)

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
