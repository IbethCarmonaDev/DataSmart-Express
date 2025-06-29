import requests

# Solo el subdominio del proyecto (sin "https://")
SUPABASE_PROJECT_ID = "mjstmccvyewdlcariipk"  # ← ojo: solo esto
SERVICE_ROLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1qc3RtY2N2eWV3ZGxjYXJpaXBrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MDI0MDYzNSwiZXhwIjoyMDY1ODE2NjM1fQ.OtClILKD1yVN7RGxuDMMoiHJUiVEhploYoY_M6lBQe4"
email_a_borrar = "ibeth+4@hotmail.com"

headers = {
    "apikey": SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SERVICE_ROLE_KEY}"
}

# 1. Buscar usuario por email
url = f"https://{SUPABASE_PROJECT_ID}.supabase.co/auth/v1/admin/users?email={email_a_borrar}"
res = requests.get(url, headers=headers)

try:
    data = res.json()
    print("🔍 Respuesta Supabase:", data)

    # Si es una lista directamente (API v1)
    if isinstance(data, list) and data:
        user_id = data[0]['id']
    # Si es un diccionario con clave 'users' (API v2)
    elif isinstance(data, dict) and 'users' in data and data['users']:
        user_id = data['users'][0]['id']
    else:
        print("❌ No se encontró el usuario con ese correo.")
        exit()

    print(f"Usuario encontrado: {user_id}")

    # 2. Eliminar
    delete_url = f"https://{SUPABASE_PROJECT_ID}.supabase.co/auth/v1/admin/users/{user_id}"
    delete_res = requests.delete(delete_url, headers=headers)

    if delete_res.status_code == 204:
        print("✅ Usuario eliminado correctamente.")
    else:
        print(f"❌ Error al eliminar: {delete_res.status_code} - {delete_res.text}")

    # 3. Borrar de tabla personalizada 'usuarios'
    from auth.conexion_supabase import supabase  # si ya lo tienes conectado

    # Requiere que tengas una columna 'user_id' en la tabla 'usuarios'
    respuesta = supabase.table("usuarios").delete().eq("user_id", user_id).execute()

    if respuesta.status_code == 200:
        print("🗑 Usuario también eliminado de la tabla usuarios.")
    else:
        print(f"⚠️ Error al borrar en tabla usuarios: {respuesta.status_code} - {respuesta.text}")


except Exception as e:
    print("❌ Error procesando la respuesta:", e)
    print("🔴 Contenido crudo:", res.text)
