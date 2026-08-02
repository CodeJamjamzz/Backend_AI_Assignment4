import os
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(override=True)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = None
if url and key and url != "your_project_url_here":
    try:
        supabase = create_client(url, key)
    except Exception as e:
        print(f"Error initializing Supabase client: {e}")
else:
    print("Warning: Supabase credentials are not properly set in the .env file.")

app = FastAPI(title="Auth API")

class UserCredentials(BaseModel):
    email: str
    password: str

@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(credentials: UserCredentials):
    if not supabase:
        raise HTTPException(status_code=500, detail="Database client not configured")
    try:
        res = supabase.auth.sign_up({
            "email": credentials.email,
            "password": credentials.password
        })
        return res
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.post("/auth/login")
def login(credentials: UserCredentials):
    if not supabase:
        raise HTTPException(status_code=500, detail="Database client not configured")
    try:
        res = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        return res
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Invalid login credentials"}
        )

@app.get("/public/info")
def public_info():
    return {"message": "Welcome stranger! This info is public."}

@app.get("/protected/profile")
def protected_profile(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Access token required"}
        )
    return {"message": "Token present, but not verified yet."}
