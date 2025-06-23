#######################################################################################
# Creado por: Ibeth Carmona. Jun 18-2025
# Aqui van las funciones útiles para la Autenticación de Usuarios
#######################################################################################

import hashlib

def hash_password(password: str) -> str:
    """Convierte una contraseña en un hash SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()
