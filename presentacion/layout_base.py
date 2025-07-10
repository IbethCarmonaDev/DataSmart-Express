from PIL import Image
import streamlit as st

def mostrar_layout(nombre_usuario: str, plan_usuario: str):
    st.markdown(
        """
        <style>
        .top-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.5rem 1rem;
            background-color: #f8f9fa;
            border-bottom: 1px solid #ddd;
        }
        .top-bar-left {
            display: flex;
            align-items: center;
        }
        .top-bar-left img {
            height: 120px;
            margin-right: 30px;
        }
        .top-bar-info {
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .top-bar-info span {
            font-weight: bold;
            color: #4B0082;
            font-size: 1.1rem;
        }
        .top-bar-right {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        .nav-button {
            padding: 0.5rem 1rem;
            border-radius: 8px;
            background-color: #e9ecef;
            border: none;
            font-size: 0.95rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    logo = Image.open("Logo.png")

    st.markdown(f"""
        <div class='top-bar'>
            <div class='top-bar-left'>
                <img src='data:image/png;base64,{_image_to_base64(logo)}' alt='Logo DataSmart Express'/>
                <div class='top-bar-info'>
                    <span>👤 {nombre_usuario}</span>
                    <span>📄 Plan: {plan_usuario}</span>
                </div>
            </div>
            <div class='top-bar-right'>
                <button class='nav-button'>Inicio</button>
                <button class='nav-button'>Planes</button>
                <button class='nav-button'>Perfil</button>
                <button class='nav-button'>Cerrar sesión</button>
            </div>
        </div>
    """, unsafe_allow_html=True)

def _image_to_base64(image):
    import base64
    from io import BytesIO
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

