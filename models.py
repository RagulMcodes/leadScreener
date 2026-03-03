import asyncio

QUESTIONS = {
    1: {
        "field": "Name",
        "type": "text",
        "question": "What is your full name?"
    },
    2: {
        "field": "age",
        "type": "text",
        "question": "What is your age?"
    },
    3: {
        "field": "Area",
        "type": "text",
        "question": "Which area are you looking for the loan in?"
    },
    4: {
        "field": "Loan_Type",
        "type": "mcq",
        "question": "Select loan type:",
        "options": [
            {"id": "flat", "label": "Flat"},
            {"id": "plot", "label": "Plot"},
            {"id": "individual_home", "label": "Individual Home"},
            {"id": "construction", "label": "Construction"}
        ]
    },
    5: {
        "field": "employment_type",
        "type": "mcq",
        "question": "Are you salaried or self-employed?",
        "options": [
            {"id": "salaried", "label": "Salaried"},
            {"id": "self_employed", "label": "Self-Employed"}
        ]
    },
    6: {
        "field": "salary_credit_type",
        "type": "mcq",
        "question": "How do you receive salary?",
        "options": [
            {"id": "bank", "label": "Bank Credit"},
            {"id": "cash", "label": "Cash"}
        ]
    },
    7: {
        "field": "is_property_approved",
        "type": "mcq",
        "question": "Is the property approved?",
        "options": [
            {"id": "yes", "label": "Yes"},
            {"id": "no", "label": "No"}
        ]
    },
    8: {
        "field": "existing_loans and EMIs",
        "type": "text",
        "question": "Do you have existing loans and EMIs? Please specify."
    },
    9: {
        "field": "Cibil_checked?",
        "type": "mcq",
        "question": "What are your current EMI details?",
        "options": [
            {"id": "yes", "label": "Yes"},
            {"id": "no", "label": "No"}
        ]
    }
}

import httpx
import os

ACCESS_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

WHATSAPP_URL = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"


async def send_whatsapp_message(payload):
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
            return await send_buttons(phone, q["question"], q["options"])
        else:
            return await send_list(phone, q["question"], q["options"])
