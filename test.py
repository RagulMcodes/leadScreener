import models
import asyncio

phone = "916379805626"

data = {
    "phone": "6379805626",
    "age": "29",
    "loan_type": "Flat",
    "property_approved": "Yes",
    "existing_emi": "Bike loan EMI ₹4000",
    "cibil": "745"
}

async def main():
    await models.send_whatsapp_message(phone)

if __name__ == "__main__":
    # This is the entry point that starts the asynchronous engine
    asyncio.run(main())
