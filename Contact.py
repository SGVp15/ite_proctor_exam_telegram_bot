import datetime
import random
import re

from Utils.translit import transliterate, replace_ru_char_to_eng_char
from Utils.utils import to_md5, clean_string


class Contact:
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

        # self.course: str | None = None
        # self.course_small: str | None = None
        # self.lector: str | None = None
        self.date_from_file = None
        self.date_exam: datetime.datetime | None = None
        self.date_exam_connect: str | None = None
        self.open_at: str | None = None
        self.close_at: str | None = None
        self.remove_at: str | None = None
        self.deadline: str | None = None
        self.scheduled_at: str | None = None
        self.proctor: str | None = None
        self.subject: str | None = None
        self.date_exam_for_subject = None
        self.url_proctor: str | None = None
        # self.url_course: str | None = None

        self.identifier: str | None = None
        # self.is_create_enrollment: bool = False
        self.status = 'Error'

        self.ispring_id: str | None = None
        self.ispring_status: str | None = None

        self.id_moodle = None
        self.moodle_id_exam = None
        self.moodle_id_user = None

    def normalize(self) -> bool:
        self.first_name_rus = clean_string(self.first_name_rus).capitalize()
        self.last_name_eng = clean_string(self.last_name_eng).capitalize()
        self.first_name_eng = clean_string(self.first_name_eng).capitalize()
        self.email = replace_ru_char_to_eng_char(clean_string(self.email).lower())
        self.date_from_file = clean_string(self.date_from_file).lower()

        if not self.first_name_eng:
            self.first_name_eng = transliterate(f'{self.first_name_rus}').capitalize()
        else:
            self.first_name_eng = replace_ru_char_to_eng_char(self.first_name_eng)

        if not self.last_name_eng:
            self.last_name_eng = transliterate(f'{self.last_name_rus}').capitalize()
        else:
            self.last_name_eng = replace_ru_char_to_eng_char(self.last_name_eng)

        self.email = replace_ru_char_to_eng_char(self.email.strip())

        self.name_eng = f'{self.first_name_eng} {self.last_name_eng}'

        if datetime.datetime.now() > self.date_exam:
            return False

        self.date_exam_connect = self.date_exam + datetime.timedelta(minutes=-5)
        self.scheduled_at = self.date_exam + datetime.timedelta(hours=-3)
        deadline = self.scheduled_at + datetime.timedelta(hours=2)
        remove_at = self.scheduled_at + datetime.timedelta(days=90)
        open_at = self.scheduled_at - datetime.timedelta(minutes=20)
        close_at = self.scheduled_at + datetime.timedelta(hours=2, minutes=20)

        pattern_time = "%Y-%m-%dT%H:%M:%SZ"
        self.date_exam_for_subject = self.date_exam.strftime(pattern_time)
        self.deadline = deadline.strftime(pattern_time)
        self.open_at = open_at.strftime(pattern_time)
        self.close_at = close_at.strftime(pattern_time)
        self.remove_at = remove_at.strftime(pattern_time)

        self.username = re.sub(r'\s+', '_', self.name_eng.strip().lower())

        if not self.password:
            self.password = f'{self.username}_P{random.randint(0, 9999):04d}'

        self.subject = f'{self.date_exam_for_subject}_{self.username}_' \
                       f'{self.exam}_proctor-{self.proctor}'

        self.identifier = to_md5(f'{self.date_from_file.replace(".", "-")}_{self.username}_{self.exam}')
        return True

    def __str__(self) -> str:
        self.s = (
            f'{self.status}\t'
            f'{datetime.datetime.now()}\t'
            f'subject={self.subject}\t'
            f'last_name_rus={self.last_name_rus}\t'
            f'first_name_rus={self.first_name_rus}\t'
            f'email={self.email}\t'
            f'date_from_file={self.date_from_file}\t'
            f'username={self.username}\t'
            f'password={self.password}\t'
            f'url={self.url_proctor}\t'
            f'exam={self.exam}\t'
            f'moodle_id_exam={self.moodle_id_exam}\t'
            f'moodle_id_user={self.moodle_id_user}\t'
            f'\n'
        )
        return self.s

    def __eq__(self, other):
        if self.email == other.email and self.email:
            return True
        return False


def parser_str_to_contact(log_string: str):
    """
    Парсит строку лога прокторинга, извлекая статус, дату/время и все пары ключ=значение.

    :param log_string: Строка для парсинга.
    :return: Словарь с извлеченными данными.
    """
    if not log_string:
        return {}

    # 1. Разделяем строку по пробелам или табуляциям, сохраняя все части.
    # Используем регулярное выражение для разделения, которое учитывает несколько пробелов/табуляций
    # и не ломается, если URL содержит знаки '='.
    parts = re.split(r'\s+', log_string, maxsplit=2)

    # Инициализация результата
    result = {}

    # 2. Обработка первых двух полей: Статус и Дата/Время
    if len(parts) >= 1:
        result['status'] = parts[0]
    if len(parts) >= 2:
        result['datetime'] = parts[1] + (parts[2].split()[0] if len(parts[2].split()) > 0 else "")
        # Переопределяем parts для правильного парсинга полей ключ=значение
        # parts[1] - время, parts[2] - остаток строки.
        # Мы знаем, что после времени идут поля ключ=значение, разделенные пробелами.
        key_value_string = ' '.join(parts[2:])
    else:
        # Если есть только статус, остальное пусто
        return result

    # 3. Парсинг пар ключ=значение
    # Снова разделяем строку, которая содержит только пары 'ключ=значение',
    # но только по пробелам, чтобы не испортить URL.
    key_value_pairs = key_value_string.split()

    for item in key_value_pairs:
        if '=' in item:
            try:
                key, value = item.split('=', 1)
                result[key.strip()] = value.strip()
            except ValueError:
                continue

    c = Contact()
    if result.get('status', '').lower() == 'ok':
        attributes = c.__dict__
        for attr_name in attributes:
            if attr_name in result.keys():
                setattr(c, attr_name, result.get(attr_name, ''))
        try:
            date_str = re.findall(r'([\d-]+T[\d:]+)Z', c.subject)[0]
            c.date_exam = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
            if not c.url_proctor:
                c.url_proctor = result.get('url', '')
            if not c.exam:
                c.exam = re.findall(r'_([A-Z0-9]+)_', c.subject)[0]
        except IndexError:
            pass
    return c
