import re
from datetime import datetime
from database.mongo_client import doctores_collection


# Validar fecha: DD/MM/AAAA
def es_fecha_valida(fecha_str):
    try:
        datetime.strptime(fecha_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False


# Validar hora: HH:MM (24h)
def es_hora_valida(hora_str):
    return re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", hora_str) is not None


# Verifica si una hora está disponible en la agenda del doctor
def esta_disponible(doctor_email, fecha_str, hora_str):
    doctor = doctores_collection.find_one({"correo": doctor_email})
    if not doctor:
        return False

    # Buscar disponibilidad exacta por fecha
    disponibilidad = doctor.get("disponibilidad", [])
    for dia in disponibilidad:
        if dia["fecha"] == convertir_a_iso(fecha_str):
            return hora_str in dia.get("horas", [])
    return False


# Utilidad: convertir DD/MM/AAAA → YYYY-MM-DD
def convertir_a_iso(fecha_str):
    try:
        dt = datetime.strptime(fecha_str, "%d/%m/%Y")
        return dt.strftime("%Y-%m-%d")
    except:
        return ""


# Validar si es un día hábil (lunes a viernes)
def es_fecha_habil(fecha_str):
    try:
        fecha = datetime.strptime(fecha_str, "%d/%m/%Y")
        return fecha.weekday() < 5  # 0=Lunes, 6=Domingo
    except ValueError:
        return False
