from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database.db import Database
from dotenv import load_dotenv
import secrets, uuid, os

load_dotenv("api/.env")

DATABASE_URL = os.getenv("DATABASE_URL")
print(DATABASE_URL)

class RegisterRequest(BaseModel):
    first : str
    last : str
    password : str

class RegisterResponse(BaseModel):
    id : str
    
class LoginRequest(BaseModel):
    id : str
    password : str

class LoginResponse(BaseModel):
    id : str
    token : str

app = FastAPI()
database = Database(DATABASE_URL)
database.init()

@app.get("/api")
def root():
    return "API is online"

@app.post("/api/register", response_model=RegisterResponse)
def register(info : RegisterRequest) -> RegisterResponse:
    
    user_id = str(secrets.randbelow(10**12)).zfill(12)
    register = database.register(user_id, info.first, info.last, info.password, 0.00)
    if register:
        return {
        "id": user_id
        }
    else:
        raise HTTPException(status_code=409, detail="Could not register: user already exists")
        
    

@app.post("/api/login", response_model=LoginResponse)
def login(info : LoginRequest) -> LoginResponse:
    
    checker = check_login(info.id, info.password)
    if checker is True:
        token = str(uuid.uuid4())
        database.set_token(info.id, token)
        return {
            "id" : info.id,
            "token" : token
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid or unmatching credentials")


def check_login(id : str, password : str):
    found_pass = database.get_pass(id)
    if not found_pass:
        return False
    
    if password != found_pass[0]:
        return False
    else:
        return True
