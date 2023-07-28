import logging

from fastapi import FastAPI

app = FastAPI()

logger = logging.getLogger("webhook_logger")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(log_format)

# Add the handler to the logger
logger.addHandler(console_handler)


@app.post("/your-webhook")
async def receive_webhook(payload: dict):
    # Process the payload received from Replicate webhook here
    logger.info("Received webhook payload: %s", payload)
    return {"message": "Webhook received successfully!"}
