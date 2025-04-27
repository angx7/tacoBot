# database/mongo_client.py

from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI)
db = client["tacobot"]  # nombre de la base de datos, puedes cambiarlo

# Aquí podemos definir las colecciones:
doctores_collection = db["doctores"]
doctores_collection.create_index("email", unique=True)
