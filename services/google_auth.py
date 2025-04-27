import os
import pathlib

from flask import Flask, redirect, request
from google_auth_oauthlib.flow import Flow

# Carga de variables de entorno
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/calendar",
]

# Ruta absoluta al archivo client_secret.json descargado de Google Cloud
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, "client_secret.json")


def create_flow():
    return Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE, scopes=SCOPES, redirect_uri=GOOGLE_REDIRECT_URI
    )
