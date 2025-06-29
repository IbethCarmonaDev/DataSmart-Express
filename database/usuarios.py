############################################################
# Creador por: Ibeth Carmona.Jun 25-2025
# Opcion para Insertar el perfil del Usuario en Supabase
############################################################
# database/usuarios.py
import streamlit as st

from auth.conexion_supabase import supabase

def OLDguardar_perfil_usuario(perfil):
    try:
        data = {
            "user_id": perfil["user_id"],
            "nombre": perfil["nombre"],
            "email": perfil["email"],
            "plan_actual": perfil["plan_actual"],
            "fecha_registro": perfil["fecha_inicio_trial"],
            "fecha_inicio_trial": perfil["fecha_inicio_trial"],
            "dias_trial": perfil["dias_trial"]
        }

        response = supabase.table("usuarios").insert([data]).execute()
        st.write(f"🔑 response: {response}")

        if response.status_code != 201:
            raise Exception(f"Error Supabase: {response.status_code} - {response.data}")

        return True

    except Exception as e:
        print("❌ Error al guardar perfil:", e)
        return False

def guardar_perfil_usuario(perfil):
    try:
        data = {
            "user_id": perfil["user_id"],
            "nombre": perfil["nombre"],
            "email": perfil["email"],
            "plan_actual": perfil["plan_actual"],
            "fecha_registro": perfil["fecha_inicio_trial"],
            "fecha_inicio_trial": perfil["fecha_inicio_trial"],
            "dias_trial": perfil["dias_trial"]
        }

        response = supabase.table("usuarios").insert([data]).execute()
        st.write("🔍 Payload insert:", data)
        st.write("📥 Respuesta Supabase:", response)

        if response.status_code != 201:
            raise Exception(f"Error Supabase: {response.status_code} - {response.data}")

        return True

    except Exception as e:
        st.error(f"❌ Error al guardar perfil: {e}")
        return False



