import datetime
from pathlib import Path

from .config_cert_exam import DIR_CERTS, TEMPLATE_FOLDER


class CertContact:
    def __init__(self, number: int = 0, abr_exam: str = '', email: str = '',
                 name_rus: str = '', name_eng: str = '', date_exam: datetime.datetime | None = None,
                 exam_rus: str = '', exam_eng: str = '', file_out_png: Path = '',
                 template: str = ''):
        self.can_create_cert = 0
        self.number = number
        self.abr_exam: str = abr_exam.upper()
        self.email: str = email.lower()
        self.name_rus: str = name_rus
        self.name_eng: str = name_eng
        self.date_exam: datetime.datetime = date_exam
        self.exam_rus: str = exam_rus
        self.exam_eng: str = exam_eng
        self.file_out_png: Path = file_out_png
        self.template: str = template

    def create_path_file(self):
        self.template = self.abr_exam + '.png'
        if not Path(TEMPLATE_FOLDER, self.template).exists():
            raise FileNotFoundError
        date_exam = f"{self.date_exam.strftime('%Y.%m.%d')}"
        self.file_out_png = Path(DIR_CERTS, self.date_exam.strftime('%Y'),
                                 self.date_exam.strftime('%m'),
                                 f"{self.abr_exam}_{date_exam}_{self.name_rus}"
                                 f"_{self.number}_{self.email}.png")

    def __eq__(self, other):
        try:
            if (
                    self.number == other.number and
                    self.abr_exam == other.abr_exam and
                    self.email == other.email and
                    self.name_rus == other.name_rus and
                    self.name_eng == other.name_eng and
                    self.date_exam == other.date_exam
            ):
                return True
        except AttributeError:
            pass
        return False
