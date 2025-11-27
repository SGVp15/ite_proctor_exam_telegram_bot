from fastapi import FastAPI
import uvicorn

from root_config import LOG_FILE, ALLOWED_EXAMS
from fastAPI.user_api import User

app = FastAPI()


@app.get("/allowed_exams")
async def get_allowed_exams():
    return ALLOWED_EXAMS


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

def uvicorn_run():
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
