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
                # No se necesita set_session() si Supabase ya está en modo recuperación

                respuesta = supabase.auth.update_user({"password": nueva})

                if respuesta.user:
                    st.success("✅ Contraseña actualizada correctamente. Redirigiendo al login...")
                    st.balloons()

                    # Redirige después de unos segundos
                    st.markdown("""
                        <script>
                            setTimeout(function() {
                                window.location.href = "/";
                            }, 3000);
                        </script>
                    """, unsafe_allow_html=True)
                else:
                    st.error("❌ No se pudo actualizar la contraseña.")
            except Exception as e:
                st.error(f"❌ Error técnico: {e}")
