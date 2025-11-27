from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator

from root_config import ALLOWED_EXAMS


class User(BaseModel):
    last_name_rus: str = 'Иванов'
    first_name_rus: str = 'Иван'
    email: EmailStr
    last_name_eng: str = 'Ivanov'
    first_name_eng: str = 'Ivan'
    exam: str = 'ITIL4FC'
    is_online_exam: bool
    date_exam: datetime

    @field_validator('exam')
    def validate_exam(exam):
        if exam not in ALLOWED_EXAMS:
            raise ValueError(f"Invalid exam: {exam}. Allowed exams are: {ALLOWED_EXAMS}")
        return exam
