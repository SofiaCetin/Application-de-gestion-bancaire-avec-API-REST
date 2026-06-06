from fastapi import FastAPI, HTTPException, Depends, Cookie, Response
from pydantic import BaseModel
from database.db import Database
from dotenv import load_dotenv
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime, timedelta, UTC
import jwt, secrets, os

load_dotenv("api/.env")

SECRET_JWT_KEY = os.getenv("SECRET_JWT_KEY")
ALGORITHM = "HS256"
DATABASE_URL = os.getenv("DATABASE_URL")

password_hash = PasswordHasher()


class RegisterRequest(BaseModel):
    first : str
    last : str
    password : str

class RegisterResponse(BaseModel):
    user_id : str
    
class LoginRequest(BaseModel):
    user_id : str
    password : str

class LoginResponse(BaseModel):
    user_id : str
    token : str

app = FastAPI()
database = Database(DATABASE_URL)
database.init()

@app.get("/api")
def root() -> str:
    return "API is online"

@app.post("/api/register", response_model=RegisterResponse)
def register(info : RegisterRequest) -> RegisterResponse:
    
    user_id = str(secrets.randbelow(10**12)).zfill(12)
    register = database.register(user_id, info.first, info.last, password_hash.hash(info.password), 0.00)
    if register:
        return {
        "user_id" : user_id
        }
    else:
        raise HTTPException(status_code=409, detail="Registration failed")         

@app.post("/api/login")
def login(info : LoginRequest, response : Response):
    
    checker = check_login(info.user_id, info.password)
    if checker is True:
        token = create_access_token(info.user_id)
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=600
            )
        return {
            "user_id" : info.user_id,
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid or unmatching credentials")


def check_login(user_id : str, password : str) -> bool:
    hashed_pass = database.get_pass(user_id)
    
    if not hashed_pass:
        return False
    
    try:
        return password_hash.verify(hashed_pass, password)
    except VerifyMismatchError:
        return False

def create_access_token(user_id : str) -> str:
    token_info = {
        "sub": user_id,
        "exp": datetime.now(UTC) + timedelta(minutes=10)
    }

    token = jwt.encode(token_info, SECRET_JWT_KEY, algorithm=ALGORITHM)
    return token

def get_current_user(access_token : str | None = Cookie(default=None)):
    
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Missing token"
        )

    try:
        token = jwt.decode(
            access_token,
            SECRET_JWT_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = token.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return user_id

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def check_user(user_id : str) -> bool:
    res = database.get_user(user_id)
    if res is None:
        return False
    else:
        return True

@app.get("/api/logged-user")
def logged_user(user_id : str = Depends(get_current_user)):
    return {
        "user_id" : user_id
    }
    
@app.get("/api/balance")
def balance(user_id : str = Depends(get_current_user)):
    balance = database.get_balance(user_id)
    
    return {
        "user_id" : user_id,
        "balance" : balance
    }

@app.post("/api/payment")
def pay(amount : float, receiver_id : str, transmitter_id : str = Depends(get_current_user)):
    transmitter_balance = database.get_balance(transmitter_id)
    if amount <= 5:
        raise HTTPException(status_code=400, detail="Invalid amount")
    
    if transmitter_balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    if check_user(receiver_id) is True:
        database.transfer(transmitter_id, receiver_id, amount)
        new_balance = database.get_balance(transmitter_id)
        
        return {
            "user_id" : transmitter_id,
            "receiver_id" : receiver_id,
            "sent" : amount,
            "new_balance" : new_balance
        }
    else:
        
        raise HTTPException(status_code=400, detail="Could not find receiver's ID")

@app.post("/api/logout")
def logout(response : Response):
    response.delete_cookie("access_token")
    message = "Logged out"
    return {
        "message" : message
    }