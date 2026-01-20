import datetime
import random
import re

import dateparser

from Utils.log import log
from Utils.translit import transliterate, replace_ru_char_to_eng_char
from Utils.utils import to_md5, clean_string
from root_config import LOG_FILE


class Contact:
    def __init__(self):
        self.pattern_time = "%Y-%m-%dT%H:%M:%SZ"
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
        self.date_from_file: datetime.datetime | None = None
        self.date_exam: datetime.datetime | None = None
        self.date_exam_connect: datetime.datetime | None = None
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

        self.moodle_id_exam = None
        self.moodle_id_user = None

    def parser_str_to_contact(s: str):
        """
        Парсит строку лога прокторинга, извлекая статус, дату/время и все пары ключ=значение.

        :param s: Строка для парсинга.
        :return: Словарь с извлеченными данными.
        """
        result = {}
        if not s:
            return {}

        # Разделяем строку, которая содержит только пары 'ключ=значение',
        # но только по пробелам, чтобы не испортить URL.
        key_value_pairs = s.split()

        for item in key_value_pairs:
            if '=' in item:
                try:
                    key, value = item.split('=', 1)
                    result[key.strip()] = value.strip()
                except ValueError:
                    continue

        if result.get('status', '').lower() != 'ok':
            return {}

        contact = Contact()
        attributes = contact.__dict__
        for attr_name in attributes:
            if attr_name in result.keys():
                if 'date' in attr_name:
                    setattr(contact, attr_name, dateparser.parse(result.get(attr_name, '')))
                    continue
                setattr(contact, attr_name, result.get(attr_name, ''))
        try:
            if not contact.url_proctor:
                contact.url_proctor = result.get('url', '')
            if not contact.exam:
                contact.exam = re.findall(r'_([A-Z0-9]+)_', contact.subject)[0]
        except IndexError:
            pass
        return contact

    def normalize(self) -> bool:
        self.first_name_rus = clean_string(self.first_name_rus).capitalize()
        self.last_name_eng = clean_string(self.last_name_eng).capitalize()
        self.first_name_eng = clean_string(self.first_name_eng).capitalize()
        self.email = replace_ru_char_to_eng_char(clean_string(self.email).lower())

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

        if not self.date_exam_connect:
            self.date_exam_connect = self.date_exam + datetime.timedelta(minutes=-5)
        if not self.scheduled_at:
            self.scheduled_at = self.date_exam + datetime.timedelta(hours=-3)
        else:
            self.scheduled_at = dateparser.parse(self.scheduled_at)
        deadline = self.scheduled_at + datetime.timedelta(hours=2)
        remove_at = self.scheduled_at + datetime.timedelta(days=90)
        open_at = self.scheduled_at - datetime.timedelta(minutes=20)
        close_at = self.scheduled_at + datetime.timedelta(hours=2, minutes=20)

        self.deadline = deadline.strftime(self.pattern_time)
        self.open_at = open_at.strftime(self.pattern_time)
        self.close_at = close_at.strftime(self.pattern_time)
        self.remove_at = remove_at.strftime(self.pattern_time)

        self.username = re.sub(r'\s+', '_', self.name_eng.strip().lower())

        if not self.password:
            self.password = f'{self.username}_P{random.randint(1000, 9999):04d}'

        self.subject = f'{self.date_exam_for_subject}_{self.username}_' \
                       f'{self.exam}_proctor-{self.proctor}'

        self.identifier = to_md5(f'{self.date_from_file.strftime(self.pattern_time)}_{self.username}_{self.exam}')
        return True

    def __str__(self) -> str:
        return (
            f"status={self.status}\t"
            f"timestamp={datetime.datetime.now().strftime("%Y-%m-%d T%H:%M:%S")}\t"
            f"identifier={self.identifier}\t"
            f"subject={self.subject}\t"
            f"name_eng={self.name_eng}\t"
            f"last_name_rus={self.last_name_rus}\t"
            f"first_name_rus={self.first_name_rus}\t"
            f"last_name_eng={self.last_name_eng}\t"
            f"first_name_eng={self.first_name_eng}\t"
            f"email={self.email}\t"
            f"username={self.username}\t"
            f"password={self.password}\t"
            f"exam={self.exam}\t"
            f"proctor={self.proctor}\t"
            f"url_proctor={self.url_proctor}\t"
            f"date_from_file={self.date_from_file}\t"
            f"date_exam={self.date_exam}\t"
            f"date_exam_connect={self.date_exam_connect}\t"
            f"date_exam_for_subject={self.date_exam_for_subject}\t"
            f"scheduled_at={self.scheduled_at}\t"
            f"open_at={self.open_at}\t"
            f"close_at={self.close_at}\t"
            f"deadline={self.deadline}\t"
            f"remove_at={self.remove_at}\t"
            f"moodle_id_exam={self.moodle_id_exam}\t"
            f"moodle_id_user={self.moodle_id_user}\n"
        )

    def __eq__(self, other):
        try:
            if self.email == other.email and self.exam == other.exam and self.date_exam == other.date_exam:
                return True
        except AttributeError:
            pass
        return False


def load_contacts_from_log_file(file=LOG_FILE, date: datetime.datetime | None = None) -> [Contact]:
    contacts = []
    try:
        with open(file, 'r', encoding='utf-8') as f:
            s = f.read()
        for row in s.split('\n'):
            c: Contact
            c = Contact.parser_str_to_contact(row)
            if not date:
                contacts.append(c)
                continue
            if date.day() == c.date_exam.day():
                contacts.append(c)
                continue
        return contacts
    except Exception as e:
        log.error(e)
        return []


if __name__ == '__main__':
    contacts = load_contacts_from_log_file(LOG_FILE)
    for c in contacts:
        if c:
            c.normalize()
            print(c)

    print(c)
