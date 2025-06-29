# auth/reset_password.py

import streamlit as st
import requests
from PIL import Image
from auth.conexion_supabase import SUPABASE_URL, SUPABASE_KEY
from utilidades.errores_supabase import obtener_mensaje_error

def mostrar_reset_password(token):
    idioma = st.session_state.get("idioma", "es")  # por defecto español

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
                st.warning("⚠️ Por favor, completa ambos campos." if idioma == "es" else "⚠️ Please complete both fields.")
            elif nueva != confirmar:
                st.error("❌ Las contraseñas no coinciden." if idioma == "es" else "❌ Passwords do not match.")
            elif len(nueva) < 6:
                st.error(obtener_mensaje_error("weak_password", idioma))
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
                        st.success("✅ Contraseña actualizada exitosamente." if idioma == "es" else "✅ Password successfully updated.")
                        st.balloons()
                        st.markdown("<p style='text-align:center'>Redirigiendo al inicio de sesión...</p>" if idioma == "es" else "<p style='text-align:center'>Redirecting to login...</p>", unsafe_allow_html=True)
                        st.query_params.clear()
                        st.session_state.modo = "login"
                        st.rerun()
                    else:
                        try:
                            resp_json = response.json()
                            msg = resp_json.get("msg", "").lower()

                            # Mapeo de errores
                            if "new password should be different" in msg:
                                st.error(obtener_mensaje_error("password_same_as_old", idioma))
                            elif "token has expired" in msg or "invalid token" in msg:
                                st.error(obtener_mensaje_error("token_invalid_or_expired", idioma))
                            elif "missing token" in msg:
                                st.error(obtener_mensaje_error("missing_token", idioma))
                            else:
                                st.error(f"❌ {msg or obtener_mensaje_error('error_desconocido', idioma)}")

                        except:
                            st.error(f"❌ {response.text}")

                except Exception as e:
                    st.error(f"❌ Error técnico: {e}")


