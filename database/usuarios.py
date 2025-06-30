############################################################
# Creador por: Ibeth Carmona.Jun 25-2025
# Opcion para Insertar el perfil del Usuario en Supabase
############################################################
# database/usuarios.py
import streamlit as st

from auth.conexion_supabase import supabase
from datetime import datetime, timedelta
def guardar_perfil_usuario(perfil):
    try:
        user_id = perfil["user_id"]

        # Verificar si ya existe un perfil con este user_id
        check = supabase.table("usuarios").select("user_id").eq("user_id", user_id).execute()
        if check.data:
            print("ℹ Perfil ya existe, no se inserta.")
            return True  # Ya existe, no es error

        # Obtener fecha actual en UTC y calcular fechas trial
        fecha_actual_utc = datetime.utcnow()
        dias_trial = perfil.get("dias_trial", 7)
        fecha_fin_trial = fecha_actual_utc + timedelta(days=dias_trial)

        # Insertar perfil con fechas normalizadas
        data = {
            "user_id": user_id,
            "nombre": perfil["nombre"],
            "email": perfil["email"],
            "plan_actual": perfil["plan_actual"],
            "fecha_registro": fecha_actual_utc,
            "fecha_inicio_trial": fecha_actual_utc,
            "fecha_fin_trial": fecha_fin_trial,
            "dias_trial": dias_trial
        }

        response = supabase.table("usuarios").insert([data]).execute()

        if response.status_code != 201:
            raise Exception(f"Error Supabase: {response.status_code} - {response.data}")

        return True

    except Exception as e:
        st.error(f"❌ Error al guardar perfil: {e}")
        return False

def actualizar_plan_usuario(user_id: str, nuevo_plan: str, fecha_fin_trial: str = None):
    try:
        update_data = {
            "plan_actual": nuevo_plan
        }

        if fecha_fin_trial:
            update_data["fecha_fin_trial"] = fecha_fin_trial

        response = supabase.table("usuarios").update(update_data).eq("user_id", user_id).execute()

        if response.status_code not in (200, 204):
            st.error(f"❌ Error actualizando plan: {response.status_code}")
    except Exception as e:
        st.error(f"❌ Excepción al actualizar plan en Supabase: {e}")


def OLDguardar_perfil_usuario(perfil):
    try:
        user_id = perfil["user_id"]

        # Verificar si ya existe un perfil con este user_id
        check = supabase.table("usuarios").select("user_id").eq("user_id", user_id).execute()
        if check.data:
            print("ℹ Perfil ya existe, no se inserta.")
            return True  # Ya existe, no es error

        # Si no existe, insertamos
        data = {
            "user_id": user_id,
            "nombre": perfil["nombre"],
            "email": perfil["email"],
            "plan_actual": perfil["plan_actual"],
            "fecha_registro": perfil["fecha_inicio_trial"],
            "fecha_inicio_trial": perfil["fecha_inicio_trial"],
            "dias_trial": perfil["dias_trial"]
        }

        response = supabase.table("usuarios").insert([data]).execute()
        #st.write("📥 Insert:", data)

        if response.status_code != 201:
            raise Exception(f"Error Supabase: {response.status_code} - {response.data}")

        return True

    except Exception as e:
        st.error(f"❌ Error al guardar perfil: {e}")
        return False

def OLDactualizar_plan_usuario(user_id, nuevo_plan, fecha_fin_trial=None):
    data_update = {"plan_actual": nuevo_plan}
    if fecha_fin_trial:
        data_update["fecha_fin_trial"] = fecha_fin_trial

    try:
        supabase.table("usuarios").update(data_update).eq("user_id", user_id).execute()
    except Exception as e:
        print(f"Error al actualizar plan: {e}")

