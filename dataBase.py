
import os
from supabase import create_client, Client
from dotenv import load_dotenv


load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)



def ifNewUser(num) -> bool:
    response = (
        supabase.table("main")
        .select("phone_number")
        .eq("phone_number", num)
        .limit(1)
        .execute()
    )
    return bool(response.data)



def addUser(num) -> None:
    supabase.table("main").insert({"phone_number": num}).execute()

def updateUser(phone: object, data: object) -> None:
    supabase.table("main")\
        .update(data)\
        .eq("phone_number", phone)\
        .execute()
def getUser(phone):
    response = supabase.table("main").select("*").eq("phone_number", phone).execute()
    return response.data[0] if response.data else None