from fastapi import Header, HTTPException
import os
import requests

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

def get_current_user(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    response = requests.get(
        f"{SUPABASE_URL}/auth/v1/user",
        headers={"Authorization": f"Bearer {token}", "apikey": SUPABASE_KEY}
    )
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return response.json()["id"]
