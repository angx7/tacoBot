from database.mongo_client import conversaciones_collection, doctores_collection
from services.whatsapp.estados import EstadoConversacion as Estado
from services.whatsapp.mensajes import *
from services.whatsapp.helpers import (
    es_fecha_valida,
    es_hora_valida,
    es_fecha_habil,
)
from services.calendar import (
    get_horas_disponibles,
    crear_evento_en_calendar,
    buscar_cita_en_calendar,
)
from datetime import datetime, timezone, timedelta

TIEMPO_EXPIRACION = timedelta(minutes=30)


# def procesar_agendamiento(msg, numero):
#     msg = msg.strip().lower()
#     ahora = datetime.now(timezone.utc)
#     conversacion = conversaciones_collection.find_one({"numero": numero})

#     last_updated = conversacion.get("last_updated") if conversacion else None
#     if last_updated and last_updated.tzinfo is None:
#         last_updated = last_updated.replace(tzinfo=timezone.utc)

#     # Nueva conversación o reinicio por inactividad
#     if not conversacion or (last_updated and ahora - last_updated > TIEMPO_EXPIRACION):
#         conversaciones_collection.update_one(
#             {"numero": numero},
#             {
#                 "$set": {"estado": Estado.SELECCION_DOCTOR, "last_updated": ahora},
#                 "$unset": {
#                     "nombre": "",
#                     "fecha": "",
#                     "hora": "",
#                     "doctor": "",
#                     "doctor_email": "",
#                 },
#             },
#             upsert=True,
#         )
#         return mensaje_bienvenida()

#     # Actualizar timestamp cada que haya respuesta
#     conversaciones_collection.update_one(
#         {"numero": numero}, {"$set": {"last_updated": ahora}}
#     )

#     estado = conversacion.get("estado")

#     # -------------------- Paso 1: Selección de doctor --------------------
#     if estado == Estado.SELECCION_DOCTOR:
#         if msg.isdigit():
#             indice = int(msg) - 1
#             doctores = list(
#                 doctores_collection.find({}, {"_id": 0, "name": 1, "email": 1})
#             )
#             if 0 <= indice < len(doctores):
#                 doctor = doctores[indice]
#                 conversaciones_collection.update_one(
#                     {"numero": numero},
#                     {
#                         "$set": {
#                             "estado": Estado.ESPERANDO_NOMBRE_PACIENTE,
#                             "doctor": doctor["name"],
#                             "doctor_email": doctor["email"],
#                         }
#                     },
#                 )
#                 return mensaje_pedir_nombre()
#         return "❌ Opción inválida. Escribe el número del doctor que elijas."

#     # -------------------- Paso 2: Nombre del paciente --------------------
#     if estado == Estado.ESPERANDO_NOMBRE_PACIENTE:
#         conversaciones_collection.update_one(
#             {"numero": numero},
#             {"$set": {"estado": Estado.ESPERANDO_FECHA, "nombre": msg.title()}},
#         )
#         return mensaje_pedir_fecha()

#     # -------------------- Paso 3: Fecha --------------------
#     if estado == Estado.ESPERANDO_FECHA:
#         if not es_fecha_valida(msg):
#             return mensaje_formato_invalido()
#         if not es_fecha_habil(msg):
#             return "📆 Lo siento, no se permiten citas en sábado o domingo. Por favor, elige otro día hábil."

#         horas_disponibles = get_horas_disponibles(
#             doctor_email=conversacion["doctor_email"], fecha_ddmmaaaa=msg
#         )

#         if not horas_disponibles:
#             return "❌ No hay horarios disponibles para esa fecha. ¿Podrías proporcionar otra?"

#         conversaciones_collection.update_one(
#             {"numero": numero},
#             {"$set": {"estado": Estado.ESPERANDO_HORA, "fecha": msg}},
#         )

#         horarios_msg = "\n".join([f"- {hora}" for hora in horas_disponibles])
#         return f"🕒 Estas son las horas disponibles para ese día:\n{horarios_msg}\n\nResponde con la hora exacta (HH:MM)"

#     # -------------------- Paso 4: Hora --------------------
#     if estado == Estado.ESPERANDO_HORA:
#         if not es_hora_valida(msg):
#             return mensaje_formato_invalido()

#         doctor_email = conversacion.get("doctor_email")
#         fecha = conversacion.get("fecha")
#         hora = msg
#         nombre_paciente = conversacion.get("nombre")

#         ok = crear_evento_en_calendar(doctor_email, nombre_paciente, fecha, hora)

#         if not ok:
#             return "⚠️ Ocurrió un error al agendar la cita en el calendario. Inténtalo más tarde."

#         conversaciones_collection.update_one(
#             {"numero": numero},
#             {"$set": {"hora": hora, "estado": Estado.FINALIZADO}},
#         )

#         return mensaje_confirmacion(
#             nombre=nombre_paciente,
#             fecha=fecha,
#             hora=hora,
#             doctor=conversacion.get("doctor"),
#         )

#     # -------------------- Finalizado --------------------
#     if estado == Estado.FINALIZADO:
#         if msg in ["reiniciar", "nueva", "nueva cita", "otra cita"]:
#             conversaciones_collection.update_one(
#                 {"numero": numero},
#                 {
#                     "$set": {
#                         "estado": Estado.SELECCION_DOCTOR,
#                         "last_updated": ahora,
#                     },
#                     "$unset": {
#                         "nombre": "",
#                         "fecha": "",
#                         "hora": "",
#                         "doctor": "",
#                         "doctor_email": "",
#                     },
#                 },
#             )
#             return mensaje_bienvenida()

#         # Mostrar los datos de la última cita agendada
#         return mensaje_confirmacion(
#             nombre=conversacion.get("nombre", "Paciente"),
#             fecha=conversacion.get("fecha", "¿?"),
#             hora=conversacion.get("hora", "¿?"),
#             doctor=conversacion.get("doctor", "¿?"),
#         )

#     return mensaje_formato_invalido()


def procesar_agendamiento(msg, numero):
    msg = msg.strip()
    ahora = datetime.now(timezone.utc)
    conversacion = conversaciones_collection.find_one({"numero": numero})
    last_updated = conversacion.get("last_updated") if conversacion else None
    if last_updated and last_updated.tzinfo is None:
        last_updated = last_updated.replace(tzinfo=timezone.utc)

    # Detectar nuevo flujo
    if not conversacion or (last_updated and ahora - last_updated > TIEMPO_EXPIRACION):
        if msg == "1":
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

        elif msg == "2":
            conversaciones_collection.update_one(
                {"numero": numero},
                {
                    "$set": {
                        "estado": Estado.CONSULTA_SELECCION_DOCTOR,
                        "last_updated": ahora,
                    },
                    "$unset": {
                        "nombre_consulta": "",
                        "doctor_email": "",
                    },
                },
                upsert=True,
            )
            doctores = list(doctores_collection.find({}, {"_id": 0, "name": 1}))
            opciones = "\n".join(
                [f"{i+1}. {doc['name']}" for i, doc in enumerate(doctores)]
            )
            return f"👨‍⚕️ Elige el doctor con quien hiciste la cita:\n{opciones}\n\nResponde con el número correspondiente."

        else:
            return mensaje_bienvenida()

    conversaciones_collection.update_one(
        {"numero": numero}, {"$set": {"last_updated": ahora}}
    )
    estado = conversacion.get("estado")

    if estado == Estado.CONSULTA_SELECCION_DOCTOR:
        if msg.isdigit():
            indice = int(msg) - 1
            doctores = list(
                doctores_collection.find({}, {"_id": 0, "name": 1, "email": 1})
            )
            if 0 <= indice < len(doctores):
                doctor = doctores[indice]
                conversaciones_collection.update_one(
                    {"numero": numero},
                    {
                        "$set": {
                            "estado": Estado.CONSULTA_ESPERANDO_NOMBRE,
                            "doctor_email": doctor["email"],
                        }
                    },
                )
                return "📄 Por favor, dime tu nombre completo para buscar tu cita."
        return "❌ Opción inválida. Escribe el número del doctor que elijas."

    if estado == Estado.CONSULTA_ESPERANDO_NOMBRE:
        nombre_input = msg.title()
        doctor_email = conversacion.get("doctor_email")

        resultado = buscar_cita_en_calendar(doctor_email, nombre_input)

        conversaciones_collection.update_one(
            {"numero": numero}, {"$set": {"estado": Estado.FINALIZADO}}
        )

        if resultado:
            fecha, hora = resultado
            return f"✅ Tu cita está agendada para el {fecha} a las {hora}."
        else:
            return "😕 No encontré ninguna cita registrada con ese nombre."

    # 👇 Aquí va TODO el resto de tu flujo original: agendar (ya lo tienes igual)
    ...
