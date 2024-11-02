import datetime
import hashlib
import random

from translit import transliterate, transliterate_error


class Contact():
    def __init__(self):
        self.name_eng: str | None = None
        self.last_name_rus: str | None = None
        self.first_name_rus: str | None = None
        self.last_name_eng: str | None = None
        self.first_name_eng: str | None = None
        self.email: str | None = None
        self.username: str | None = None
        self.password: str | None = None
        self.exam: str | None = None
        self.course: str | None = None
        self.course_small: str | None = None
        self.lector: str | None = None
        self.date_from_file = None
        self.date_exam = None
        self.date_exam_connect: str | None = None
        self.remove_at: str | None = None
        self.deadline: str | None = None
        self.scheduled_at: str | None = None
        self.proctor: str | None = None
        self.subject: str | None = None
        self.date_exam_for_subject = None
        self.url_proctor: str | None = None
        self.url_course: str | None = None
        self.id_ispring: str | None = None
        self.status_ispring: str | None = None
        self.identifier: str | None = None
        self.is_create_enrollment: bool = False
        self.status = 'Error'

    def normalize(self) -> bool:
        if self.first_name_eng == '' or self.first_name_eng is None:
            self.first_name_eng = transliterate(f'{self.first_name_rus}').capitalize()
        else:
            self.first_name_eng = transliterate_error(self.first_name_eng)

        if self.last_name_eng == '' or self.last_name_eng is None:
            self.last_name_eng = transliterate(f'{self.last_name_rus}').capitalize()
        else:
            self.last_name_eng = transliterate_error(self.last_name_eng)

        self.email = transliterate_error(self.email.strip())

        self.name_eng = f'{self.first_name_eng} {self.last_name_eng}'

        if datetime.datetime.now() > self.date_exam:
            return False

        self.date_exam_connect = self.date_exam - datetime.timedelta(minutes=5)
        self.scheduled_at = self.date_exam + datetime.timedelta(hours=-3)
        deadline = self.scheduled_at + datetime.timedelta(hours=2)
        remove_at = self.scheduled_at + datetime.timedelta(days=90)

        pattern_time = "%Y-%m-%dT%H:%M:%SZ"
        self.date_exam_for_subject = self.date_exam.strftime(pattern_time)
        self.deadline = deadline.strftime(pattern_time)
        self.remove_at = remove_at.strftime(pattern_time)

        self.username = self.name_eng.replace(' ', '_')

        if self.proctor == '' or self.proctor is None:
            self.proctor = None

        if self.password == '' or self.password is None:
            self.password = f'{self.username}_{random.randint(1000, 9999)}'

        self.subject = f'{self.date_exam_for_subject}_{self.username}_' \
                       f'{self.exam}_proctor-{self.proctor}'
        self.identifier = to_md5(f'{self.date_from_file.replace(".", "-")}_{self.username}_{self.exam}')
        return True

    def __str__(self) -> str:
        self.s = f'{self.status}\t{datetime.datetime.now()}\tsubject={self.subject}\t' \
                 f'lastName={self.last_name_rus}\tfirstName={self.first_name_rus}\t' \
                 f'email={self.email}\tusername={self.username}\tpassword={self.password}\t' \
                 f'url={self.url_proctor}\n'
        return self.s

    def __eq__(self, other):
        if self.email == other.email:
            return True

        return False


def to_md5(s: str):
    return hashlib.md5(s.encode()).hexdigest()
