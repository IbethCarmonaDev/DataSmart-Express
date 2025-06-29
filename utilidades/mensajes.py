import streamlit as st
from PIL import Image

def mostrar_mensaje_exito(titulo="✅ Registro exitoso", mensaje="Tu cuenta ha sido confirmada. Ya puedes iniciar sesión."):
    col1, col2 = st.columns([1, 3])

    with col1:
        try:
            logo = Image.open("Logo.png")
            st.image(logo, width=120)
        except:
            st.write("")

    with col2:
        st.markdown(f"""
        <div style='margin-top: 15px;'>
            <h3 style='color: #2b85ff;'>{titulo}</h3>
            <p style='font-size: 16px; color: #444;'>{mensaje}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("⬅ [Volver al login](?reload=true)")
