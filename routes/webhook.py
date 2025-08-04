# from flask import Blueprint, request
# from twilio.twiml.messaging_response import MessagingResponse
# from services.whatsapp import handle_incoming_message

# webhook_bp = Blueprint("webhook", __name__)


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
#     # Process the incoming message

#     print(f"Processing message: {incoming_msg}")

#     response_text = handle_incoming_message(incoming_msg, sender)

#     resp = MessagingResponse()
#     msg = resp.message()
#     msg.body(response_text)

#     return str(resp), 200


# routes/webhook.py

from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from services.whatsapp.handler import handle_incoming_message

webhook_bp = Blueprint("webhook", __name__)


@webhook_bp.route("/", methods=["POST"])
@webhook_bp.route("", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")

    print(f"📩 Mensaje recibido de {sender}: {incoming_msg}")

    # Lógica del bot
    response_text = handle_incoming_message(incoming_msg, sender)

    # Responder a Twilio
    twilio_response = MessagingResponse()
    twilio_response.message(response_text)
    return str(twilio_response)
