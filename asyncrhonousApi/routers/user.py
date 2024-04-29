from fastapi import APIRouter, Depends 
import sqlite3
from models.user import User
from models.task import Task
from passlib.context import CryptContext
from middleware.auth import verify_password, get_password_hash, generate_token, oauth2_scheme, validate_token
from typing_extensions import Annotated
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()



@router.post('/addUser')
async def addUser(user: User):
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    username = user.username
    password = get_password_hash(user.password)
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    if user:
        return {"status": "failed user already exists"}
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    con.commit()
    return {"status": f"success creating user {username}"}

@router.post('/login')
async def login(user: User):
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    username = user.username
    password = user.password
    
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    if not user:
        return {"status": "failed user not found"}
    if not verify_password(password, user[2]):
        return {"status": "failed password incorrect"}
    data = {"username": user[1]}
    token = generate_token(data)
    return {'token': token}

@router.get('/getUser')
async def getUser(token: Annotated[str, Depends(oauth2_scheme)]):
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    username = validate_token(token)
    return {"user": username}
