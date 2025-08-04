from database.mongo_client import conversaciones_collection, doctores_collection
from services.whatsapp.estados import EstadoConversacion as Estado
from services.whatsapp.mensajes import *
from services.whatsapp.helpers import (
    es_fecha_valida,
    es_hora_valida,
    es_fecha_habil,
)
from services.calendar import get_horas_disponibles, crear_evento_en_calendar
from datetime import datetime, timezone, timedelta

TIEMPO_EXPIRACION = timedelta(minutes=30)


def procesar_agendamiento(msg, numero):
    msg = msg.strip().lower()
    ahora = datetime.now(timezone.utc)
    conversacion = conversaciones_collection.find_one({"numero": numero})

    # Nueva conversación o reinicio por inactividad
    if not conversacion or (
        conversacion.get("last_updated")
        and ahora - conversacion["last_updated"] > TIEMPO_EXPIRACION
    ):
        conversaciones_collection.update_one(
            {"numero": numero},
            {
                "$set": {"estado": Estado.SELECCION_DOCTOR, "last_updated": ahora},
                "$unset": {
                    "nombre": "",
                    "fecha": "",
                    "hora": "",
                    "doctor": "",
                    "doctor_email": "",
                },
            },
            upsert=True,
        )
        return mensaje_bienvenida()

    # Actualizar timestamp cada que haya respuesta
    conversaciones_collection.update_one(
        {"numero": numero}, {"$set": {"last_updated": ahora}}
    )

    estado = conversacion.get("estado")

    # -------------------- Paso 1: Selección de doctor --------------------
    if estado == Estado.SELECCION_DOCTOR:
        if msg.isdigit():
            indice = int(msg) - 1
            doctores = list(
                doctores_collection.find({}, {"_id": 0, "name": 1, "correo": 1})
            )
            if 0 <= indice < len(doctores):
                doctor = doctores[indice]
                conversaciones_collection.update_one(
                    {"numero": numero},
                    {
                        "$set": {
                            "estado": Estado.ESPERANDO_NOMBRE_PACIENTE,
                            "doctor": doctor["name"],
                            "doctor_email": doctor["correo"],
                        }
                    },
                )
                return mensaje_pedir_nombre()
        return "❌ Opción inválida. Escribe el número del doctor que elijas."

    # -------------------- Paso 2: Nombre del paciente --------------------
    if estado == Estado.ESPERANDO_NOMBRE_PACIENTE:
        conversaciones_collection.update_one(
            {"numero": numero},
            {"$set": {"estado": Estado.ESPERANDO_FECHA, "nombre": msg.title()}},
        )
        return mensaje_pedir_fecha()

    # -------------------- Paso 3: Fecha --------------------
    if estado == Estado.ESPERANDO_FECHA:
        if not es_fecha_valida(msg):
            return mensaje_formato_invalido()
        if not es_fecha_habil(msg):
            return "📆 Lo siento, no se permiten citas en sábado o domingo. Por favor, elige otro día hábil."

        horas_disponibles = get_horas_disponibles(
            doctor_email=conversacion["doctor_email"], fecha_ddmmaaaa=msg
        )

        if not horas_disponibles:
            return "❌ No hay horarios disponibles para esa fecha. ¿Podrías proporcionar otra?"

        conversaciones_collection.update_one(
            {"numero": numero},
            {"$set": {"estado": Estado.ESPERANDO_HORA, "fecha": msg}},
        )

        horarios_msg = "\n".join([f"- {hora}" for hora in horas_disponibles])
        return f"🕒 Estas son las horas disponibles para ese día:\n{horarios_msg}\n\nResponde con la hora exacta (HH:MM)"

    # -------------------- Paso 4: Hora --------------------
    if estado == Estado.ESPERANDO_HORA:
        if not es_hora_valida(msg):
            return mensaje_formato_invalido()

        doctor_email = conversacion.get("doctor_email")
        fecha = conversacion.get("fecha")
        hora = msg
        nombre_paciente = conversacion.get("nombre")

        ok = crear_evento_en_calendar(doctor_email, nombre_paciente, fecha, hora)

        if not ok:
            return "⚠️ Ocurrió un error al agendar la cita en el calendario. Inténtalo más tarde."

        conversaciones_collection.update_one(
            {"numero": numero},
            {"$set": {"hora": hora, "estado": Estado.FINALIZADO}},
        )

        return mensaje_confirmacion(
            nombre=nombre_paciente,
            fecha=fecha,
            hora=hora,
            doctor=conversacion.get("doctor"),
        )

    # -------------------- Finalizado --------------------
    if estado == Estado.FINALIZADO:
        return mensaje_reiniciar()

    return mensaje_formato_invalido()
