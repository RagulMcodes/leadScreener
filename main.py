from fastapi import FastAPI, Request, Query, Response
from fastapi.responses import PlainTextResponse
import os
from fastapi import FastAPI, Request
from sqlalchemy.future import select
from dataBase import AsyncSessionLocal
from models import User
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
    print("Mode:", hub_mode)
    print("Received Token:", hub_verify_token)
    print("Expected Token:", VERIFY_TOKEN)

    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        print("WEBHOOK VERIFIED")
        return PlainTextResponse(hub_challenge)

    return Response(status_code=403)



@app.post("/")
async def receive_message(request: Request):
    body = await request.json()

    value = body.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {})

    if "messages" in value:
        message = value["messages"][0]
        phone = message["from"]
        text = message["text"]["body"]

        async with AsyncSessionLocal() as session:
            result = await session.execute(select(User).where(User.phone_number == phone))
            user = result.scalar_one_or_none()

            if not user:
                user = User(phone_number=phone)
                session.add(user)
                await session.commit()
                print("New user created")
            else:
                print("Existing user:", user.state)

    return {"status": "ok"}