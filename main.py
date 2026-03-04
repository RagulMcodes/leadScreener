from fastapi import FastAPI, Request, Query, Response
from fastapi.responses import PlainTextResponse
import os
from fastapi import FastAPI, Request
from sqlalchemy.future import select
import dataBase
import models
from datetime import datetime
import json
import logging

app = FastAPI()

PORT = int(os.getenv("PORT", 3000))
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")


logging.basicConfig(level=logging.INFO)

print("App starting...")
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
        if not dataBase.ifNewUser(phone):
            dataBase.addUser(phone)
            await models.send_question(phone, 1)

            # Detect message type
        if "text" in message:
            user_input = message["text"]["body"]

        elif "interactive" in message:
            if "button_reply" in message["interactive"]:
                user_input = message["interactive"]["button_reply"]["id"]
            elif "list_reply" in message["interactive"]:
                user_input = message["interactive"]["list_reply"]["id"]
            else:
                return {"status": "ignored"}

        else:
            return {"status": "ignored"}

        user = dataBase.getUser(phone)
        current_state = user["State"]

        field = models.QUESTIONS[current_state]["field"]
        next_state = current_state + 1
        dataBase.updateUser(phone, field, user_input, next_state)
        await models.send_question(phone, next_state)






