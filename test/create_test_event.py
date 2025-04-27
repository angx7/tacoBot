# scripts/create_test_event.py

import datetime
import google.auth.transport.requests
import google.oauth2.credentials
import googleapiclient.discovery
from database.mongo_client import doctores_collection
from utils.encryption import (
    decrypt,
)  # Aquí estamos importando tu función de desencriptado


def crear_evento_de_prueba():
    # Traer el primer doctor de la base de datos
    doctor = doctores_collection.find_one()

    if not doctor:
        print("❌ No hay doctores registrados en la base de datos.")
        return

    print(f"✅ Usando la cuenta: {doctor['email']}")

    # Desencriptar los campos necesarios
    access_token = decrypt(doctor["access_token"])
    refresh_token = decrypt(doctor["refresh_token"])
    token_uri = doctor["token_uri"]  # Este no estaba cifrado
    client_id = decrypt(doctor["client_id"])
    client_secret = decrypt(doctor["client_secret"])
    scopes = doctor["scopes"]  # scopes es lista normal

    # Construir las credenciales desencriptadas
    credentials = google.oauth2.credentials.Credentials(
        token=access_token,
        refresh_token=refresh_token,
        token_uri=token_uri,
        client_id=client_id,
        client_secret=client_secret,
        scopes=scopes,
    )

    # Refrescar el token si está expirado
    request = google.auth.transport.requests.Request()
    if credentials.expired:
        print("🔄 Token expirado, refrescando...")
        credentials.refresh(request)

    # Usar la API de Google Calendar
    service = googleapiclient.discovery.build("calendar", "v3", credentials=credentials)

    now = datetime.datetime.utcnow()
    event = {
        "summary": "🛠 Evento de Prueba",
        "location": "Online",
        "description": "Este es un evento de prueba creado automáticamente por el bot.",
        "start": {
            "dateTime": (now + datetime.timedelta(minutes=10)).isoformat() + "Z",
            "timeZone": "UTC",
        },
        "end": {
            "dateTime": (now + datetime.timedelta(minutes=40)).isoformat() + "Z",
            "timeZone": "UTC",
        },
    }

    created_event = service.events().insert(calendarId="primary", body=event).execute()

    print(f"✅ Evento creado: {created_event.get('htmlLink')}")


if __name__ == "__main__":
    crear_evento_de_prueba()
