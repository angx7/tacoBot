from database.mongo_client import conversaciones_collection
from services.whatsapp.estados import EstadoConversacion as Estado
from services.whatsapp.mensajes import *


def procesar_consulta(msg, numero):
    msg = msg.strip().lower()
    conversacion = conversaciones_collection.find_one({"numero": numero})

    # Paso 1: Si no hay conversación, inicia flujo
    if not conversacion:
        conversaciones_collection.insert_one(
            {"numero": numero, "estado": Estado.CONSULTAR_NOMBRE}
        )
        return mensaje_consulta_nombre()

    estado = conversacion.get("estado")

    # Paso 2: Esperando nombre del paciente
    if estado == Estado.CONSULTAR_NOMBRE:
        nombre = msg.title()
        cita = conversaciones_collection.find_one(
            {"nombre": nombre, "estado": Estado.FINALIZADO}
        )

        if cita:
            return mensaje_cita_encontrada(
                nombre=cita["nombre"],
                fecha=cita["fecha"],
                hora=cita["hora"],
                doctor=cita["doctor"],
            )
        else:
            return mensaje_cita_no_encontrada()

    return mensaje_reiniciar()
