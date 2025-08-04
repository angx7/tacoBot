# import os
# from dotenv import load_dotenv

import os
from dotenv import load_dotenv


def init_config():
    dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".env"))
    load_dotenv(dotenv_path, override=True)

    # Habilita transporte inseguro solo en desarrollo
    if os.getenv("DEBUG_MODE", "false").lower() == "true":
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        print(
            "⚠️  Modo DEBUG: Transporte inseguro permitido para OAuth (solo desarrollo)"
        )


# def init_config():
#     load_dotenv()


TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
