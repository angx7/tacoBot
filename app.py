from flask import Flask
from routes.webhook import webhook_bp
from routes.auth import auth_bp
from config import init_config

app = Flask(__name__)
init_config()  # Cargar .env
app.register_blueprint(webhook_bp, url_prefix="/webhook")
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)
