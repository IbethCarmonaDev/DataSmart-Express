import streamlit as st

def mostrar_mensaje_confirmacion(
    titulo: str,
    mensaje: str,
    tipo: str = "success",
    boton_texto: str = None,
    boton_callback=None,
    mensaje_final: str = ""
):
    emojis = {
        "success": "🎉",
        "warning": "⚠️",
        "error": "❌",
        "info": "ℹ️"
    }

    colores_fondo = {
        "success": "#e6f8ec",
        "warning": "#fffbe6",
        "error": "#fdecea",
        "info": "#e8f4fd"
    }

    colores_borde = {
        "success": "#2ecc71",
        "warning": "#f1c40f",
        "error": "#e74c3c",
        "info": "#3498db"
    }

    # Título centrado
    st.markdown(f"""
    <h2 style="text-align: center; color: {colores_borde[tipo]}; margin-top: 2rem;">
        {emojis[tipo]} {titulo}
    </h2>
    """, unsafe_allow_html=True)

    # Recuadro de mensaje
    st.markdown(f"""
    <div style="
        background-color: {colores_fondo[tipo]};
        border-left: 5px solid {colores_borde[tipo]};
        padding: 1rem 1.5rem;
        margin: 1.5rem auto;
        border-radius: 8px;
        width: 80%;
        color: #333;
        font-size: 1.1rem;
        ">
        {mensaje}
    </div>
    """, unsafe_allow_html=True)

    # Botón centrado
    if boton_texto and boton_callback:
        st.markdown(
            """
            <div style="text-align: center; margin-top: 1.5rem;">
                <style>
                div.stButton > button:first-child {
                    background-color: #2b85ff;
                    color: white;
                    font-weight: bold;
                    padding: 0.6rem 1.5rem;
                    border-radius: 6px;
                    font-size: 1rem;
                    width: 160px;
                }
                </style>
            """, unsafe_allow_html=True)
        st.button(boton_texto, on_click=boton_callback)
        st.markdown("</div>", unsafe_allow_html=True)

    # Mensaje final opcional
    if mensaje_final:
        st.markdown(f"""
        <div style="text-align: center; margin-top: 2rem; font-size: 0.95rem; color: #555;">
            {mensaje_final}
        </div>
        """, unsafe_allow_html=True)


