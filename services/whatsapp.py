from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def handle_incoming_message(message: str, sender: str) -> str:
    msg = message.lower()

    if "hola" in msg:
        return "¡Hola! Soy tu asistente virtual 🤖. Puedes decir 'cita' para agendar."
    elif "cita" in msg:
        return "Por favor indícame la fecha y hora de tu cita (ej. 26 abril 5pm)."
    else:
        return "No entendí eso 😅. Escribe 'hola' o 'cita'."


def enviar_mensaje(to: str, body: str):
    """Envía un mensaje de WhatsApp usando Twilio."""
    message = client.messages.create(from_=TWILIO_PHONE_NUMBER, body=body, to=to)
    return message.sid
