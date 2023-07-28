from fastapi import FastAPI

app = FastAPI()


@app.post("/your-webhook")
async def receive_webhook(payload: dict):
    # Process the payload received from Replicate webhook here
    print("Received webhook payload:", payload)
    return {"message": "Webhook received successfully!"}
