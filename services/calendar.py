from datetime import datetime, timedelta
import google.auth.transport.requests
import google.oauth2.credentials
import googleapiclient.discovery
from database.mongo_client import doctores_collection
from utils.encryption import decrypt

# Configura aquí la ventana de atención
HORA_INICIO = "09:00"
HORA_FIN = "17:00"
DURACION_MINUTOS = 60
TIMEZONE = "America/Mexico_City"


def get_horas_disponibles(doctor_email, fecha_ddmmaaaa):
    # Paso 1: obtener credenciales desencriptadas
    doctor = doctores_collection.find_one({"email": doctor_email})
    if not doctor:
        return []

    creds = google.oauth2.credentials.Credentials(
        token=decrypt(doctor["access_token"]),
        refresh_token=decrypt(doctor["refresh_token"]),
        token_uri=doctor["token_uri"],
        client_id=decrypt(doctor["client_id"]),
        client_secret=decrypt(doctor["client_secret"]),
        scopes=doctor["scopes"],
    )

    service = googleapiclient.discovery.build("calendar", "v3", credentials=creds)

    # Paso 2: construir la fecha en datetime
    fecha = datetime.strptime(fecha_ddmmaaaa, "%d/%m/%Y")
    fecha_str = fecha.strftime("%Y-%m-%d")

    # Paso 3: definir el rango del día completo
    time_min = f"{fecha_str}T00:00:00"
    time_max = f"{fecha_str}T23:59:59"

    # Paso 4: consultar eventos ocupados
    response = (
        service.freebusy()
        .query(
            body={
                "timeMin": f"{time_min}",
                "timeMax": f"{time_max}",
                "timeZone": TIMEZONE,
                "items": [{"id": doctor_email}],
            }
        )
        .execute()
    )

    busy = response["calendars"][doctor_email]["busy"]
    bloques_ocupados = [
        (parse_google_datetime(b["start"]), parse_google_datetime(b["end"]))
        for b in busy
    ]

    # Paso 5: construir bloques disponibles
    inicio = datetime.strptime(f"{fecha_str}T{HORA_INICIO}", "%Y-%m-%dT%H:%M")
    fin = datetime.strptime(f"{fecha_str}T{HORA_FIN}", "%Y-%m-%dT%H:%M")

    bloques_libres = []
    actual = inicio
    delta = timedelta(minutes=DURACION_MINUTOS)

    while actual + delta <= fin:
        bloque_inicio = actual
        bloque_fin = actual + delta

        ocupado = any(
            bloque_inicio < busy_fin and bloque_fin > busy_inicio
            for busy_inicio, busy_fin in bloques_ocupados
        )

        if not ocupado:
            bloques_libres.append(bloque_inicio.strftime("%H:%M"))

        actual += delta

    return bloques_libres


def parse_google_datetime(dt_str):
    # Maneja formato de datetime con o sin zona horaria
    try:
        return datetime.fromisoformat(dt_str)
    except Exception:
        return datetime.strptime(dt_str.split("+")[0], "%Y-%m-%dT%H:%M:%S")


def crear_evento_en_calendar(doctor_email, paciente_nombre, fecha_ddmmaaaa, hora_str):
    from_zone = TIMEZONE
    duracion = timedelta(minutes=DURACION_MINUTOS)

    # Recuperar credenciales
    doctor = doctores_collection.find_one({"email": doctor_email})
    if not doctor:
        return False

    creds = google.oauth2.credentials.Credentials(
        token=decrypt(doctor["access_token"]),
        refresh_token=decrypt(doctor["refresh_token"]),
        token_uri=doctor["token_uri"],
        client_id=decrypt(doctor["client_id"]),
        client_secret=decrypt(doctor["client_secret"]),
        scopes=doctor["scopes"],
    )

    service = googleapiclient.discovery.build("calendar", "v3", credentials=creds)

    # Convertir fecha y hora a ISO 8601
    fecha = datetime.strptime(fecha_ddmmaaaa, "%d/%m/%Y")
    hora_inicio = datetime.strptime(hora_str, "%H:%M").time()
    dt_inicio = datetime.combine(fecha, hora_inicio)
    dt_fin = dt_inicio + duracion

    evento = {
        "summary": f"Cita con {paciente_nombre}",
        "description": "Cita agendada por el bot de WhatsApp",
        "start": {
            "dateTime": dt_inicio.isoformat(),
            "timeZone": from_zone,
        },
        "end": {
            "dateTime": dt_fin.isoformat(),
            "timeZone": from_zone,
        },
    }

    try:
        created_event = (
            service.events().insert(calendarId="primary", body=evento).execute()
        )
        print(f"✅ Evento creado: {created_event.get('htmlLink')}")
        return True
    except Exception as e:
        print("❌ Error al crear el evento:", e)
        return False
