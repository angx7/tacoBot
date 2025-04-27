from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from services.whatsapp import handle_incoming_message

webhook_bp = Blueprint("webhook", __name__)


@webhook_bp.route("", methods=["POST"])
@webhook_bp.route("/", methods=["POST"])
def whatsapp_webhook():
    resp = MessagingResponse()
    msg = resp.message()
    msg.body("Hola, estoy funcionando")

    return str(resp), 200  # Asegúrate de que Twilio reciba esta respuesta


# def whatsapp_webhook():
#     incoming_msg = request.values.get("Body", "").strip()
#     sender = request.values.get("From", "")

#     print(f"Received message from {sender}: {incoming_msg}")
#     if not incoming_msg:
#         return "No message received", 400
#     if not sender:
#         return "No sender information", 400
#     # Process the incoming message

#     print(f"Processing message: {incoming_msg}")

#     response_text = handle_incoming_message(incoming_msg, sender)

#     print(f"Response text: {response_text}")

#     resp = MessagingResponse()
#     msg = resp.message()
#     msg.body(response_text)

#     return str(resp), 200


# from flask import Blueprint, request
# from twilio.twiml.messaging_response import MessagingResponse
# from services.whatsapp import handle_incoming_message
# import threading

# webhook_bp = Blueprint("webhook", __name__)


# # Función para procesar el mensaje en segundo plano
# def process_message(incoming_msg, sender):
#     print(f"Processing message: {incoming_msg}")
#     response_text = handle_incoming_message(incoming_msg, sender)
#     print(f"Response text: {response_text}")

#     resp = MessagingResponse()
#     msg = resp.message()
#     msg.body(response_text)

#     # Aquí podrías mandar la respuesta de Twilio, pero recuerda que Twilio necesita una respuesta inmediata
#     # En este caso no la mandamos desde aquí porque ya respondimos con 202.


# @webhook_bp.route("", methods=["POST"])
# @webhook_bp.route("/", methods=["POST"])
# def whatsapp_webhook():
#     incoming_msg = request.values.get("Body", "").strip()
#     sender = request.values.get("From", "")

#     print(f"Received message from {sender}: {incoming_msg}")

#     if not incoming_msg:
#         return "No message received", 400
#     if not sender:
#         return "No sender information", 400

#     # Responder inmediatamente a Twilio
#     resp = MessagingResponse()
#     msg = resp.message()
#     msg.body("¡Gracias por tu mensaje! Estoy procesando tu solicitud.")

#     # Llamar a la función de procesamiento en segundo plano
#     threading.Thread(target=process_message, args=(incoming_msg, sender)).start()

#     # Retornar la respuesta a Twilio (rápido)
#     return str(resp), 202  # Respondemos con 202 Accepted
