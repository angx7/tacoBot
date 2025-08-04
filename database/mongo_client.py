# database/mongo_client.py

from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    raise ValueError("❌ MONGODB_URI no definido en el archivo .env")

client = MongoClient(MONGODB_URI)
db = client["tacobot"]  # o el nombre que hayas configurado en MongoDB

# Colección: Doctores
doctores_collection = db["doctores"]
doctores_collection.create_index("email", unique=True)

# Colección: Conversaciones
conversaciones_collection = db["conversaciones"]
conversaciones_collection.create_index("numero", unique=True)
