import streamlit as st
from auth.conexion_supabase import supabase

def mostrar_reset_password(token):
    st.markdown("<h2 style='color:#2b85ff'>🔒 Restablecer Contraseña</h2>", unsafe_allow_html=True)

    nueva = st.text_input("Nueva contraseña", type="password")
    confirmar = st.text_input("Confirmar contraseña", type="password")

    if st.button("Restablecer"):
        if not nueva or not confirmar:
            st.warning("Por favor, completa ambos campos.")
        elif nueva != confirmar:
            st.error("Las contraseñas no coinciden.")
        else:
            try:
                # Aplica el token como sesión de recuperación
                session = supabase.auth.set_session(access_token=token, refresh_token="")

                # Verifica que la sesión fue creada correctamente
                if not session or not session.user:
                    st.error("❌ Auth session missing.")
                    return

                # Intenta actualizar la contraseña
                respuesta = supabase.auth.update_user({"password": nueva})

                if respuesta.user:
                    st.success("✅ Contraseña actualizada. Ya puedes iniciar sesión.")
                    st.balloons()
                else:
                    st.error("❌ No se pudo actualizar la contraseña.")
            except Exception as e:
                st.error(f"❌ Error técnico: {e}")
