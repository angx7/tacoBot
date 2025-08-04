from database.mongo_client import conversaciones_collection
from services.whatsapp.flujo_agendar import procesar_agendamiento
from services.whatsapp.flujo_consulta import procesar_consulta
from services.whatsapp.estados import EstadoConversacion as Estado
from services.whatsapp.mensajes import (
    mensaje_bienvenida,
    mensaje_reiniciar,
    mensaje_cancelacion,
)
from services.whatsapp.mensajes import (
    mensaje_bienvenida,
    mensaje_seleccion_doctor,
    mensaje_cancelacion,
    mensaje_reiniciar,
)


def handle_incoming_message(msg, numero):
    msg = msg.strip().lower()

    # Cancelar conversación
    if msg in ["cancelar", "salir"]:
        conversaciones_collection.delete_one({"numero": numero})
        return mensaje_cancelacion()

    # Iniciar conversación solo con "hola"
    if msg == "hola":
        conversaciones_collection.delete_one(
            {"numero": numero}
        )  # Reiniciar conversación
        conversaciones_collection.insert_one(
            {"numero": numero, "estado": Estado.MENU_PRINCIPAL}
        )
        return mensaje_bienvenida()

    # Obtener estado actual de conversación
    conversacion = conversaciones_collection.find_one({"numero": numero})
    if not conversacion:
        return "✋ Por favor, escribe 'hola' para comenzar."

    estado = conversacion.get("estado")

    # Decisión por estado
    if estado == Estado.MENU_PRINCIPAL:
        if msg == "1":
            doctores = list_doctores()
            if not doctores:
                return "🚫 No hay doctores disponibles en este momento."
            conversaciones_collection.update_one(
                {"numero": numero}, {"$set": {"estado": Estado.SELECCION_DOCTOR}}
            )
            return mensaje_seleccion_doctor(doctores)
        elif msg == "2":
            conversaciones_collection.update_one(
                {"numero": numero}, {"$set": {"estado": Estado.CONSULTAR_NOMBRE}}
            )
            return "🧾 Por favor, dime tu nombre completo para buscar tu cita."
        else:
            return "❌ Opción inválida. Escribe 1 para agendar o 2 para consultar."

    # Delegar a flujo correspondiente
    if estado in [
        Estado.SELECCION_DOCTOR,
        Estado.ESPERANDO_NOMBRE_PACIENTE,
        Estado.ESPERANDO_FECHA,
        Estado.ESPERANDO_HORA,
        Estado.FINALIZADO,
    ]:
        return procesar_agendamiento(msg, numero)

    if estado == Estado.CONSULTAR_NOMBRE:
        return procesar_consulta(msg, numero)

    return mensaje_reiniciar()


# Utilidad para traer doctores
def list_doctores():
    from database.mongo_client import doctores_collection

    return list(doctores_collection.find({}, {"_id": 0, "name": 1, "correo": 1}))
