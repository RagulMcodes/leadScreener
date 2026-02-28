from fastapi import FastAPI, Request, Query, Response
from fastapi.responses import PlainTextResponse
import os
from datetime import datetime
import json

app = FastAPI()

PORT = int(os.getenv("PORT", 3000))
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")


# 🔹 GET route for webhook verification
@app.get("/")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        print("WEBHOOK VERIFIED")
        return PlainTextResponse(content=hub_challenge, status_code=200)
    else:
        return Response(status_code=403)


# 🔹 POST route for receiving messages
@app.post("/")
async def receive_webhook(request: Request):
    body = await request.json()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n\nWebhook received {timestamp}\n")
    print(json.dumps(body, indent=2))

    return Response(status_code=200)