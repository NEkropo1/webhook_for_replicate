import collections
import logging
import os

from fastapi import FastAPI
from pyapns2.apns2.client import APNsClient
from pyapns2.apns2.payload import Payload
from pyapns2.apns2.credentials import TokenCredentials

from clients import ClientsDB

app = FastAPI()

auth_key_path = 'AuthKey2.pem'
auth_key_id = os.getenv("AUTH_KEY_ID")
team_id = os.getenv("TEAM_ID")
token_credentials = TokenCredentials(auth_key_path=auth_key_path, auth_key_id=auth_key_id, team_id=team_id)
client = APNsClient(credentials=token_credentials, use_sandbox=True)

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
    logger.info("Received webhook id: %s", _id)
    if _id and _id in clients.clients:
        device_token = clients.clients[_id]
        payload = Payload(alert=f"Your prediction {_id} is complete!", sound="default", badge=1)
        topic = "com.noname.digital.development"  # Change this to your app's bundle identifier
        Notification = collections.namedtuple("Notification", ["token", "payload"])
        notifications = [Notification(payload=payload, token=device_token)]
        client.send_notification_batch(notifications=notifications, topic=topic)
    else:
        logger.warning("ID %s not found in clients DB.", _id)
    return {"message": "Webhook received successfully!"}
