from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, field_validator

app = FastAPI()
allowed_exams: list = [
    'BAFC',
    'BASRMC',
    'CPIC',
    'Cobit2019C',
    'ICSC',
    'ITAMC',
    'ITHRC',
    'ITIL4FC',
    'OPSC',
    'RCVC',
    'RISKC',
    'SCMC',
    'SOA4C',
    'SYSAC',
]


class User(BaseModel):
    last_name_rus: str
    first_name_rus: str
    email: EmailStr
    last_name_eng: str = ''
    first_name_eng: str = ''
    username: str | None = None
    password: str | None = None
    exam: str
    is_online_exam: bool
    date_exam: datetime

    @field_validator('exam')
    def validate_exam(exam):
        if exam not in allowed_exams:
            raise ValueError(f"Invalid exam: {exam}. Allowed exams are: {allowed_exams}")
        return exam


@app.post("/users_for_exam")
def users(s: User):
    s.allowed_exams = ''
    return s

@app.get("/allowed_exams")
def get_allowed_exams():
    return allowed_exams