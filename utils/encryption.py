from cryptography.fernet import Fernet
import os

# Carga la clave de un .env o un entorno seguro
FERNET_KEY = os.environ.get("FERNET_KEY")

if not FERNET_KEY:
    raise Exception("FERNET_KEY no configurada en variables de entorno.")

cipher_suite = Fernet(FERNET_KEY)


def encrypt(text: str) -> str:
    return cipher_suite.encrypt(text.encode()).decode()


def decrypt(token: str) -> str:
    return cipher_suite.decrypt(token.encode()).decode()
