from dotenv import load_dotenv

load_dotenv()

from services.whatsapp import enviar_mensaje

if __name__ == "__main__":
    numero_destino = "whatsapp:+5214778398185"  # Reemplaza con tu número
    mensaje = "🧪 ¡Hola! Este es un mensaje de prueba desde el bot Flask + Twilio"

    try:
        sid = enviar_mensaje(numero_destino, mensaje)
        print(f"✅ Mensaje enviado correctamente. SID: {sid}")
    except Exception as e:
        print(f"❌ Error al enviar mensaje: {e}")
