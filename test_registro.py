from auth.registro import registrar_usuario

nombre = "Ibeth C"
email = "ibeth.carmona@gmail.com"
password = "123456"

resultado = registrar_usuario(nombre, email, password)
print(resultado)