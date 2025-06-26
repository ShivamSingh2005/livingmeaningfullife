from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime

app = FastAPI()

# Allow CORS for frontend on Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use your frontend domain here in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database for simplicity
users_db = {}
time_logs = {}

class User(BaseModel):
    name: str
    email: str
    stage: Optional[str] = "Not Started"

class TimeLog(BaseModel):
    email: str
    start_time: str  # ISO format string
    end_time: str

@app.post("/register")
def register_user(user: User):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.email] = user
    return {"message": "Registered successfully"}

@app.get("/user/{email}")
def get_user(email: str):
    user = users_db.get(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/update-stage")
def update_stage(email: str, stage: str):
    user = users_db.get(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.stage = stage
    return {"message": "Stage updated"}

@app.post("/log-time")
def log_time(entry: TimeLog):
    logs = time_logs.setdefault(entry.email, [])
    logs.append({
        "start": entry.start_time,
        "end": entry.end_time,
        "date": datetime.now().strftime("%Y-%m-%d")
    })
    return {"message": "Time logged successfully"}

@app.get("/logs/{email}")
def get_logs(email: str):
    return time_logs.get(email, [])
