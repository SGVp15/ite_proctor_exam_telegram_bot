from fastapi import FastAPI

from Telegram.config import LOG_FILE
from config import allowed_exams
from fastAPI.user_api import User

app = FastAPI()


@app.get("/allowed_exams")
async def get_allowed_exams():
    return allowed_exams


@app.get("/show_queue_registration")
async def show_queue_registration():
    return 'show_queue_registration'


@app.get("/log_registration")
async def log_registration():
    with open(LOG_FILE, encoding='utf-8', mode='r') as f:
        return f.read()


@app.post("/registration_for_exam")
async def users(user_list: User):
    return user_list
