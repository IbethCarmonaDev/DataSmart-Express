# test_login.py

from auth.login import login_usuario

email = "ibeth.carmona@gmail.com"
password = "123456"

usuario = login_usuario(email, password)

if usuario:
    print("✅ Login exitoso")
    print("Nombre:", usuario["nombre"])
    print("Plan actual:", usuario["plan_actual"])
else:
    print("❌ Email o contraseña incorrectos")
