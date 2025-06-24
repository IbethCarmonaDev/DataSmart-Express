import streamlit as st
import requests
from PIL import Image
from auth.conexion_supabase import SUPABASE_URL, SUPABASE_KEY

def mostrar_reset_password(token):
    col_logo, col_form = st.columns([1, 2])

    with col_logo:
        try:
            logo = Image.open("Logo.png")
            st.image(logo, width=140)
        except:
            st.write("")

        st.markdown("""
        <div style='margin-top: 20px;'>
            <h4 style='color: #2b85ff; font-weight: bold; margin-bottom: 0;'>Automatiza.</h4>
            <h4 style='color: #2b85ff; font-weight: bold; margin-bottom: 0;'>Visualiza.</h4>
            <h4 style='color: #2b85ff; font-weight: bold;'>Decide con inteligencia.</h4>
        </div>
        """, unsafe_allow_html=True)

    with col_form:
        st.markdown("<h2 style='color:#2b85ff; text-align:center'>🔒 Restablecer Contraseña</h2>", unsafe_allow_html=True)

        nueva = st.text_input("Nueva contraseña", type="password")
        confirmar = st.text_input("Confirmar contraseña", type="password")

        if st.button("Restablecer"):
            if not nueva or not confirmar:
                st.warning("⚠️ Por favor, completa ambos campos.")
            elif nueva != confirmar:
                st.error("❌ Las contraseñas no coinciden.")
            elif len(nueva) < 6:
                st.error("❌ La contraseña debe tener al menos 6 caracteres.")
            else:
                try:
                    headers = {
                        "apikey": SUPABASE_KEY,
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json"
                    }

                    payload = {
                        "password": nueva
                    }

                    url = f"{SUPABASE_URL}/auth/v1/user"
                    response = requests.put(url, headers=headers, json=payload)

                    if response.status_code == 200:
                        st.success("✅ Contraseña actualizada exitosamente.")
                        st.balloons()
                        st.markdown("<p style='text-align:center'>Redirigiendo al inicio de sesión...</p>", unsafe_allow_html=True)
                        st.experimental_set_query_params()  # limpia los tokens de la URL
                        st.session_state.modo = "login"
                        st.rerun()
                    else:
                        try:
                            resp_json = response.json()
                            if resp_json.get("error_code") == "weak_password":
                                st.error("❌ La contraseña es demasiado débil. Usa al menos 6 caracteres.")
                            else:
                                st.error(f"❌ Error: {resp_json.get('msg', 'Error desconocido')}")
                        except:
                            st.error(f"❌ No se pudo actualizar la contraseña. {response.text}")

                except Exception as e:
                    st.error(f"❌ Error técnico: {e}")