import time
from asyncio import sleep
import datetime

from Contact import parser_str_to_contact, Contact

from Email import EmailSending
from Email.config import EMAIL_LOGIN, SMTP_SERVER, SMTP_PORT, EMAIL_PASSWORD, EMAIL_BCC


def get_contacts_from_logs() -> [Contact]:
    rows = ''
    try:
        with open('./data/log.txt', 'r', encoding='utf-8') as f:
            rows = f.read()
    except Exception as e:
        print(e)
    contacts = []
    for row in rows.split('\n'):
        c = parser_str_to_contact(row)
        if c:
            contacts.append(c)
    return contacts


def check_time_interval(check_dt: datetime.datetime, start_dt: datetime.datetime, delta_dt: datetime.datetime) -> bool:
    end_dt = start_dt + delta_dt
    return start_dt <= check_dt <= end_dt


async def check_log_and_send_email():
    # def check_log_and_send_email():
    hour_contacts = []
    while True:
        contact_for_email_ = []
        for c in get_contacts_from_logs():
            c: Contact
            interval_duration = datetime.timedelta(hours=1)
            if check_time_interval(c.date_exam - interval_duration, datetime.datetime.now(),
                                   datetime.timedelta(minutes=1)):
                contact_for_email_.append(c)
                hour_contacts.append(c)
        text = ''
        if contact_for_email_:
            for c in contact_for_email_:
                text += (
                    f'date={c.date_exam}\t'
                    f'exam={c.exam}\t'
                    f'last_name_rus={c.last_name_rus}\t'
                    f'first_name_rus={c.first_name_rus}\t'
                    f'email={c.email}\t'
                    f'username={c.username}\t'
                    f'password={c.password}\t'
                    f'url={c.url_proctor}\t'
                    f'\n\n'
                )
            email = EmailSending(
                subject=f'Экзамены {text}', from_email=EMAIL_LOGIN, to=EMAIL_BCC, cc='', bcc='',
                text=text, html='', smtp_server=SMTP_SERVER, smtp_port=SMTP_PORT,
                login=EMAIL_LOGIN, password=EMAIL_PASSWORD, manager=None)
            email.send_email()
        await sleep(60)


if __name__ == '__main__':
    # check_log_and_send_email()
    # 1. Создание интервала
    start_time = datetime.datetime(2025, 12, 1, 16, 30, 0)
    # Продолжительность: 1 час 30 минут
    interval_duration = datetime.timedelta(hours=1, minutes=30)

    # 2. Время для проверки
    # Время внутри интервала (10:00:00 + 01:30:00 = 11:30:00)
    time_to_check_in = datetime.datetime(2025, 12, 1, 16, 0, 0)
    # Время вне интервала
    time_to_check_out = datetime.datetime(2025, 12, 1, 17, 0, 0)

    # 3. Тестирование
    print(f"Интервал: {start_time} — {start_time + interval_duration}")
    print("-" * 40)
    print(f"Проверка {time_to_check_in}: {check_time_interval(time_to_check_in, start_time, interval_duration)}")
    print(f"Проверка {time_to_check_out}: {check_time_interval(time_to_check_out, start_time, interval_duration)}")
