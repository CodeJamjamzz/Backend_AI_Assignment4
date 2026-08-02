import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Generated Auth API")
security = HTTPBearer()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

class UserAuth(BaseModel):
    email: str
    password: str

@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserAuth):
    try:
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password
        })
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.post("/auth/login")
def login(user: UserAuth):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        return response
    except Exception as e:
        # Note: A common AI mistake is returning 400 instead of 401 here
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid login")

@app.get("/public/info")
def get_public_info():
    return {"message": "This route is completely public!"}

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    # The AI might not wrap this in a try-except, which could cause a 500 server error on invalid tokens
    # instead of a clean 401 Unauthorized, because Supabase raises an exception on invalid tokens.
    user_response = supabase.auth.get_user(token)
    if not user_response.user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return user_response.user

@app.get("/protected/profile")
def get_profile(user = Depends(verify_token)):
    return {"user_id": user.id, "email": user.email}

@app.get("/protected/dashboard")
def get_dashboard(user = Depends(verify_token)):
    return {"message": f"Welcome {user.email}, this is your protected dashboard."}
