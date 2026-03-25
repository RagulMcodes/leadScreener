from dotenv import load_dotenv
import httpx
import os
import requests

load_dotenv()
ACCESS_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

async def send_whatsapp_message(phone: object) -> None:

    WHATSAPP_URL = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {
            "body": "please fill this form: https://rococo-salmiakki-9a4773.netlify.app/"
        }
    }

    response = requests.post(WHATSAPP_URL, headers=headers, json=payload)

    print(response.status_code)
    print(response.text)

















'''async def send_whatsapp_message(payload):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            WHATSAPP_URL,
            headers=headers,
            json=payload
        )

    print(response.status_code, response.text)
    return response.json()

async def send_text(phone, text):
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {
            "body": text
        }
    }

    return await send_whatsapp_message(payload)

async def send_buttons(phone, question, options):
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": question},
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": opt["id"],
                            "title": opt["label"]
                        }
                    }
                    for opt in options
                ]
            }
        }
    }

    return await send_whatsapp_message(payload)

async def send_list(phone, question, options):
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": {"text": question},
            "action": {
                "button": "Select",
                "sections": [
                    {
                        "title": "Options",
                        "rows": [
                            {
                                "id": opt["id"],
                                "title": opt["label"]
                            }
                            for opt in options
                        ]
                    }
                ]
            }
        }
    }

    return await send_whatsapp_message(payload)


async def send_question(phone, state):
    q = QUESTIONS[state]

    if q["type"] == "text":
        return await send_text(phone, q["question"])

    if q["type"] == "mcq":
        if len(q["options"]) <= 3:
             await send_buttons(phone, q["question"], q["options"])
        else:
             await send_list(phone, q["question"], q["options"])'''
