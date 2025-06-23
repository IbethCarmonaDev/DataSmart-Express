# import streamlit as st
# from auth.reset_password import mostrar_reset_password
# from auth.interfaz_login import mostrar_login
#
# # Configuración de la página
# st.set_page_config(page_title="Recuperar Contraseña", layout="centered")
#
# # Leer los parámetros de la URL
# query_params = st.query_params
# params = {k: v[0] for k, v in query_params.items()}  # convierte listas en strings
#
# # Detectar si es flujo de recuperación de contraseña
# token = params.get("access_token") or params.get("token")  # acepta ambos
# recovery_type = params.get("type")
#
# if token and recovery_type == "recovery":
#     mostrar_reset_password(token)
#     st.stop()
#
# # Si no hay token, mostrar pantalla de inicio de sesión
# mostrar_login()

import streamlit as st
from auth.reset_password import mostrar_reset_password
from auth.interfaz_login import mostrar_login

# Configuración de la página
st.set_page_config(page_title="Recuperar Contraseña", layout="centered")

# Leer los parámetros de la URL
query_params = st.query_params
params = {k: v[0] for k, v in query_params.items()}  # convierte listas en strings

# Detectar si es flujo de recuperación de contraseña
token = params.get("access_token") or params.get("token")  # acepta ambos
recovery_type = params.get("type")

# ✅ Caso 1: El token ya está presente → mostrar restablecimiento
if token and recovery_type == "recovery":
    mostrar_reset_password(token)
    st.stop()

# ✅ Caso 2: Si llega con #access_token en la URL → convertirlo en ?access_token y redirigir
elif not params and "redirigiendo" not in st.session_state:
    st.session_state["redirigiendo"] = True  # evitar bucles infinitos

    st.markdown("""
    <h3 style='color:#2b85ff'>🔄 Redirigiendo a recuperación de contraseña...</h3>
    <script>
        const hash = window.location.hash;
        if (hash && hash.includes("access_token")) {
            const query = hash.substring(1);  // elimina el #
            const newUrl = window.location.origin + "/?" + query;
            window.location.replace(newUrl);
        }
    </script>
    """, unsafe_allow_html=True)
    st.stop()

# ✅ Caso 3: Mostrar pantalla de inicio de sesión normal
mostrar_login()
