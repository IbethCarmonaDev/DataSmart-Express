import streamlit as st
from auth.conexion_supabase import supabase

def OLDmostrar_reset_password(token):
    st.set_page_config(page_title="Restablecer contraseña", layout="centered")
    st.title("🔐 Restablecer tu contraseña")

    nueva_clave = st.text_input("Nueva contraseña", type="password")
    confirmar_clave = st.text_input("Confirmar nueva contraseña", type="password")

    if st.button("Restablecer contraseña"):
        if nueva_clave != confirmar_clave:
            st.warning("⚠️ Las contraseñas no coinciden.")
        elif len(nueva_clave) < 6:
            st.warning("⚠️ La contraseña debe tener al menos 6 caracteres.")
        else:
            try:
                login = supabase.auth.sign_in_with_otp({"access_token": token})
                if login.user:
                    actualizacion = supabase.auth.update_user({"password": nueva_clave})
                    if actualizacion.user:
                        st.success("✅ Tu contraseña ha sido actualizada. Ahora puedes iniciar sesión.")
                        st.balloons()
                    else:
                        st.error("❌ No se pudo actualizar la contraseña.")
                else:
                    st.error("❌ Token inválido o expirado.")
            except Exception as e:
                st.error(f"❌ Error técnico: {e}")


def old2mostrar_reset_password(token):
    st.markdown("## 🔒 Recuperar contraseña")

    nueva = st.text_input("Nueva contraseña", type="password")
    confirmar = st.text_input("Confirmar contraseña", type="password")

    if st.button("Cambiar contraseña"):
        if nueva != confirmar:
            st.error("Las contraseñas no coinciden.")
            return
        try:
            res = st.session_state.supabase.auth.update_user({"password": nueva})
            st.success("✅ Contraseña actualizada con éxito. Inicia sesión nuevamente.")
        except Exception as e:
            st.error(f"❌ Error al actualizar: {e}")


def old3mostrar_reset_password(token):
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
                # Aplica el token de recuperación
                #supabase.auth.set_session(access_token=token, refresh_token=token)
                supabase.auth.set_session({'access_token': token, 'refresh_token': ''})

                # Actualiza la contraseña del usuario autenticado
                respuesta = supabase.auth.update_user({"password": nueva})

                if respuesta.user:
                    st.success("✅ Contraseña actualizada. Ya puedes iniciar sesión.")
                    st.balloons()
                else:
                    st.error("❌ No se pudo actualizar la contraseña.")
            except Exception as e:
                st.error(f"❌ Error técnico: {e}")

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
                supabase.auth.set_session({'access_token': token, 'refresh_token': ''})

                # Intenta actualizar la contraseña
                respuesta = supabase.auth.update_user({"password": nueva})

                if respuesta.user:
                    st.success("✅ Contraseña actualizada. Ya puedes iniciar sesión.")
                    st.balloons()
                else:
                    st.error("❌ No se pudo actualizar la contraseña.")
            except Exception as e:
                st.error(f"❌ Error técnico: {e}")

