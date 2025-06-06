# auth.py
from fastapi import Header, HTTPException
import os
import requests


SUPABASE_URL = os.getenv("VITE_SUPABASE_URL")
SUPABASE_KEY = os.getenv("VITE_SUPABASE_ANON_KEY")

def get_current_user(authorization: str = Header(default=None)):
    if not authorization:
        return "guest"  # ✅ fallback for testing

    token = authorization.replace("Bearer ", "")
    response = requests.get(
        f"{SUPABASE_URL}/auth/v1/user",
        headers={"Authorization": f"Bearer {token}", "apikey": SUPABASE_KEY}
    )
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return response.json()["id"]


