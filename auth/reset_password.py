import streamlit as st
import requests
import os

def mostrar_reset_password(token):
    st.markdown("<h2 style='color:#2b85ff'>🔒 Restablecer Contraseña</h2>", unsafe_allow_html=True)

    nueva = st.text_input("Nueva contraseña", type="password")
    confirmar = st.text_input("Confirmar contraseña", type="password")

    if st.button("Restablecer"):
        if not nueva or not confirmar:
            st.warning("⚠️ Por favor, completa ambos campos.")
        elif nueva != confirmar:
            st.error("❌ Las contraseñas no coinciden.")
        else:
            try:
                SUPABASE_URL = os.getenv("SUPABASE_URL")
                SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")

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
                    st.success("✅ Contraseña actualizada exitosamente. Ya puedes iniciar sesión.")
                    st.balloons()
                else:
                    st.error(f"❌ No se pudo actualizar la contraseña. {response.text}")

            except Exception as e:
                st.error(f"❌ Error técnico: {e}")
