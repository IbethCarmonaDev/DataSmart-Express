# utilidades/errores_supabase.py

from typing import Literal

Idioma = Literal["es", "en"]

errores_supabase = {
    "weak_password": {
        "es": "❌ La contraseña es demasiado débil. Usa al menos 6 caracteres.",
        "en": "❌ Password is too weak. Use at least 6 characters."
    },
    "password_same_as_old": {
        "es": "❌ La nueva contraseña debe ser diferente a la anterior.",
        "en": "❌ New password must be different from the old one."
    },
    "token_invalid_or_expired": {
        "es": "❌ El enlace ha expirado o es inválido. Solicita uno nuevo.",
        "en": "❌ The link has expired or is invalid. Please request a new one."
    },
    "missing_token": {
        "es": "❌ Falta el token de recuperación. Usa el enlace del correo.",
        "en": "❌ Recovery token is missing. Use the email link."
    },
    "invalid_credentials": {
        "es": "❌ Correo o contraseña incorrectos. Intenta nuevamente.",
        "en": "❌ Incorrect email or password. Please try again."
    },
    "user_exists": {
        "es": "❌ Ya existe una cuenta con ese correo. Usa otro o inicia sesión.",
        "en": "❌ An account with this email already exists. Use another or sign in."
    }
}

def obtener_mensaje_error(clave: str, idioma: Idioma = "es") -> str:
    return errores_supabase.get(clave, {}).get(idioma, "❌ Error desconocido.")
