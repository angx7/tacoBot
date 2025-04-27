# import datetime
# from flask import Blueprint, redirect, request, render_template, make_response
# from services.google_auth import create_flow
# from database.mongo_client import doctores_collection
# from google.oauth2 import id_token as google_id_token
# from google.auth.transport import requests as google_requests
# import jwt

# auth_bp = Blueprint("auth", __name__)


# @auth_bp.route("/authorize")
# def authorize():
#     flow = create_flow()
#     authorization_url, state = flow.authorization_url(
#         access_type="offline", include_granted_scopes="true", prompt="consent"
#     )
#     return redirect(authorization_url)


# @auth_bp.route("/oauth2callback")
# def oauth2callback():
#     flow = create_flow()
#     flow.fetch_token(authorization_response=request.url)

#     if not flow.credentials:
#         return "No se pudieron obtener las credenciales.", 400

#     credentials = flow.credentials

#     print("\n==== TOKEN RECIBIDO ====")
#     print("Access Token:", credentials.token)
#     print("Refresh Token:", credentials.refresh_token)
#     print("Expiry:", credentials.expiry)
#     print("========================\n")

#     # Decodificar el id_token
#     id_info = credentials.id_token
#     if isinstance(id_info, str):
#         try:
#             id_info = jwt.decode(id_info, options={"verify_signature": False})
#         except Exception as e:
#             print("Error decoding id_token:", e)
#             id_info = {}

#     name = id_info.get("given_name") or id_info.get("name") or "Doctor"

#     existing_doctor = doctores_collection.find_one({"email": id_info.get("email")})

#     # Guardar en Mongo
#     doctor_data = {
#         "access_token": credentials.token,
#         "refresh_token": credentials.refresh_token,
#         "token_uri": credentials.token_uri,
#         "client_id": credentials.client_id,
#         "client_secret": credentials.client_secret,
#         "scopes": credentials.scopes,
#         "email": id_info.get("email"),
#         "name": name,
#         "created_at": datetime.datetime.now(datetime.timezone.utc),
#     }

#     existing_doctor = doctores_collection.find_one({"email": id_info.get("email")})

#     if existing_doctor:
#         # Actualizar solo tokens y expiración
#         doctores_collection.update_one(
#             {"_id": existing_doctor["_id"]},
#             {
#                 "$set": {
#                     "access_token": credentials.token,
#                     "refresh_token": credentials.refresh_token,
#                     "token_uri": credentials.token_uri,
#                     "client_id": credentials.client_id,
#                     "client_secret": credentials.client_secret,
#                     "scopes": credentials.scopes,
#                     "updated_at": datetime.datetime.now(datetime.timezone.utc),
#                 }
#             },
#         )
#         print(f"Tokens actualizados para el doctor: {id_info.get('email')}")
#     else:
#         # Insertar nuevo doctor
#         doctor_data = {
#             "access_token": credentials.token,
#             "refresh_token": credentials.refresh_token,
#             "token_uri": credentials.token_uri,
#             "client_id": credentials.client_id,
#             "client_secret": credentials.client_secret,
#             "scopes": credentials.scopes,
#             "email": id_info.get("email"),
#             "name": name,
#             "created_at": datetime.datetime.now(datetime.timezone.utc),
#         }
#         doctores_collection.insert_one(doctor_data)
#         print(f"Nuevo doctor registrado: {id_info.get('email')}")

#     # doctores_collection.insert_one(doctor_data)

#     # Renderizamos el HTML y forzamos content-type
#     rendered_html = render_template("success.html", name=name)
#     response = make_response(rendered_html)
#     response.headers["Content-Type"] = "text/html"
#     return response


import datetime
from flask import Blueprint, redirect, request, render_template, make_response
from services.google_auth import create_flow
from database.mongo_client import doctores_collection
import jwt

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/authorize")
def authorize():
    flow = create_flow()
    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true", prompt="consent"
    )
    return redirect(authorization_url)


@auth_bp.route("/oauth2callback")
def oauth2callback():
    flow = create_flow()
    flow.fetch_token(authorization_response=request.url)

    if not flow.credentials:
        return "No se pudieron obtener las credenciales.", 400

    credentials = flow.credentials

    print("\n==== TOKEN RECIBIDO ====")
    print("Access Token:", credentials.token)
    print("Refresh Token:", credentials.refresh_token)
    print("Expiry:", credentials.expiry)
    print("========================\n")

    # Decodificar el id_token
    id_info = credentials.id_token
    if isinstance(id_info, str):
        try:
            id_info = jwt.decode(id_info, options={"verify_signature": False})
        except Exception as e:
            print("Error decoding id_token:", e)
            id_info = {}

    name = id_info.get("given_name") or id_info.get("name") or "Doctor"

    existing_doctor = doctores_collection.find_one({"email": id_info.get("email")})

    if existing_doctor:
        # Actualizar tokens
        doctores_collection.update_one(
            {"_id": existing_doctor["_id"]},
            {
                "$set": {
                    "access_token": credentials.token,
                    "refresh_token": credentials.refresh_token,
                    "token_uri": credentials.token_uri,
                    "client_id": credentials.client_id,
                    "client_secret": credentials.client_secret,
                    "scopes": credentials.scopes,
                    "updated_at": datetime.datetime.now(datetime.timezone.utc),
                }
            },
        )
        print(f"✅ Tokens actualizados para el doctor: {id_info.get('email')}")
    else:
        # Insertar nuevo doctor
        doctor_data = {
            "access_token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes,
            "email": id_info.get("email"),
            "name": name,
            "created_at": datetime.datetime.now(datetime.timezone.utc),
        }
        doctores_collection.insert_one(doctor_data)
        print(f"🆕 Nuevo doctor registrado: {id_info.get('email')}")

    # Renderizamos el HTML
    rendered_html = render_template("success.html", name=name)
    response = make_response(rendered_html)
    response.headers["Content-Type"] = "text/html"
    return response
