import streamlit as st


def mostrar_perfil(usuario: dict):
    st.markdown("## 👤 Perfil del Usuario")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**🧑 Nombre:**")
        st.write(usuario.get("nombre", "No disponible"))

        st.markdown("**📧 Email:**")
        st.write(usuario.get("email", "No disponible"))

        st.markdown("**🗓️ Fecha de registro:**")
        st.write(usuario.get("fecha_registro", "N/D"))

        st.markdown("**🆔 ID de usuario:**")
        st.code(usuario.get("user_id", "N/D"), language="text")

    with col2:
        st.markdown("**📄 Plan actual:**")
        st.success(usuario.get("plan_actual", "N/D"))

        st.markdown("**🗓️ Inicio Trial:**")
        st.write(usuario.get("fecha_inicio_trial", "N/D"))

        st.markdown("**📅 Días de trial:**")
        st.write(usuario.get("dias_trial", "N/D"))

        st.markdown("**📊 Días restantes trial:**")
        st.write(usuario.get("dias_restantes_trial", "N/D"))

    st.markdown("---")
    with st.expander("📋 Ver datos completos (JSON)", expanded=False):
        st.json(usuario)
