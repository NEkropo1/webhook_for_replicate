import logging
import os
import jwt
import time

from fastapi import FastAPI

from client import send_notification

from clients import ClientsDB

app = FastAPI()

auth_key_path = 'AuthKey1.pem'
auth_key_id = os.getenv("AUTH_KEY_ID")
team_id = os.getenv("TEAM_ID")
header = {"alg": "ES256", "kid": auth_key_id}
payload = {"iss": team_id, "iat": int(time.time())}
auth_token = jwt.encode(payload, open(auth_key_path, "r").read(), algorithm="ES256", headers=header)

clients = ClientsDB()

logger = logging.getLogger("webhook_logger")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(log_format)

logger.addHandler(console_handler)


@app.post("/receive_client_ids")
def receive_client_ids(payload: dict):
    try:
        result = clients.add_clients(payload)
        logger.info(f"Received id's: {result}")
        return {"message": "Id's received successfully!"}
    except Exception as e:
        logger.error("Failed to add clients: %s", str(e))
        return {"message": "Unexpected exception: " + str(e)}


@app.post("/receive_prediction_results")
def receive_prediction_results(payload: dict):
    _id = payload.get("id")
    status = payload.get("status")
    logger.info("Received webhook id: %s", _id)
    if _id and _id in clients.clients:
        if status == "succeeded":
            device_token = clients.clients[_id]
            bundle_id = "com.noname.digital.development"  # Change this to your app's bundle identifier
            result = send_notification(device_id=device_token, auth_token=auth_token, bundle_id=bundle_id)
            logger.info(f"Result of sent notification {result}")

    else:
        logger.warning("ID %s not found in clients DB.", _id)
    return {"message": "Webhook received successfully!"}
