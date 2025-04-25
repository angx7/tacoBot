from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from services.whatsapp import handle_incoming_message

webhook_bp = Blueprint("webhook", __name__)


@webhook_bp.route("/", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")

    response_text = handle_incoming_message(incoming_msg, sender)

    resp = MessagingResponse()
    msg = resp.message()
    msg.body(response_text)

    return str(resp)
