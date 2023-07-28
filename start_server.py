import logging
import os

from fastapi import FastAPI
from pushover.pushover import Pushover

from clients import ClientsDB

po_token = os.getenv("PUSH_APP_TOKEN")
clients = ClientsDB()
po = Pushover(po_token)
app = FastAPI()

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
        clients.add_clients(payload)
        return {"message": "Id's received successfully!"}
    except Exception as e:
        logger.error("Failed to add clients: %s", str(e))
        return {"message": "Unexpected exception: " + str(e)}


@app.post("/receive_prediction_results")
def receive_prediction_results(payload: dict):
    logger.info("Received webhook payload: %s", payload)
    _id = payload.get("id")
    if _id and _id in clients.clients:
        user_token = clients.clients[_id]
        po.user(user_token)
        msg = po.msg(f"You prediction {_id} is complete!")
        msg.set("title", "Nona me dig it all prediction completed!")
        po.send(msg)
    else:
        logger.warning("ID %s not found in clients DB.", _id)
    return {"message": "Webhook received successfully!"}
