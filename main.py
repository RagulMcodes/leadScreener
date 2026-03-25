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

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # restrict later if you want
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
            await models.send_whatsapp_message(phone)




@app.post("/googleForm")
async def google_form(request: Request):
    try:
        data = await request.json()
        print(data)

        phone = data.get("phone_number")

        update_data = {
            "Name": data.get("Name"),
            "age": data.get("age"),
            "Area": data.get("Area"),
            "Loan_Type": data.get("Loan_Type"),
            "Cibil_checked": data.get("Cibil_checked"),
            "is_property_approved": data.get("is_property_approved"),
            "existing_loans": data.get("existing_loans"),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        dataBase.updateUser(phone, update_data)
        dataBase.updateUser(phone, {"form_completed": True})
        return {"status": "ok"}

    except Exception as e:
        print("ERROR:", e)
        body = await request.body()
        print("RAW BODY:", body)
        return {"status": "error"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)