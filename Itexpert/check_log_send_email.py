import datetime
from asyncio import sleep

from Contact import Contact
from Email import EmailSending
from Email.config import EMAIL_LOGIN, SMTP_SERVER, SMTP_PORT, EMAIL_PASSWORD, EMAIL_BCC
from root_config import LOG_FILE


def get_contacts_from_logs() -> [Contact]:
    rows = ''
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            rows = f.read()
    except Exception as e:
        print(e)
    contacts = []
    for row in rows.split('\n'):
        c = Contact.parser_str_to_contact(row)
        if c:
            contacts.append(c)
    return contacts


def check_time_interval(check_dt: datetime.datetime, start_dt: datetime.datetime, delta_dt: datetime.timedelta) -> bool:
    end_dt = start_dt + delta_dt
    return start_dt <= check_dt <= end_dt


async def check_log_and_send_email():
    contact_for_email_ = []
    contacts = get_contacts_from_logs()
    for c in contacts:
        c: Contact
        if datetime.time(hour=9, minute=0) <= datetime.datetime.now().time() <= datetime.time(hour=9, minute=1,
                                                                                              second=0):
            if datetime.datetime.now().date() == c.date_exam.date():
                contact_for_email_.append(c)
                continue
        try:
            if check_time_interval(
                    check_dt=datetime.datetime.now(),
                    start_dt=c.date_exam - datetime.timedelta(hours=1),
                    delta_dt=datetime.timedelta(minutes=1)
            ):
                contact_for_email_.append(c)
        except TypeError:
            pass

    subject = 'Экзамен '
    if contact_for_email_:
        text = ''
        for c in contact_for_email_:
            if c.proctor:
                text += 'Online '
            else:
                text += 'Offline '
            text += (
                f'{c.date_exam}\n'
                f'{c.exam}\n'
                f'{c.last_name_rus} {c.first_name_rus} {c.email}\n'
                f'Логин={c.username}\n'
                f'Пароль={c.password}\n'
                f'url={c.url_proctor}\n'
                f'\n{"-" * 30}\n'
            )
            subject += f'{c.exam} {c.date_exam} '

        email = EmailSending(
            subject=f'{subject}', from_email=EMAIL_LOGIN, to=EMAIL_BCC, cc='', bcc='',
            text=text, html='', smtp_server=SMTP_SERVER, smtp_port=SMTP_PORT,
            login=EMAIL_LOGIN, password=EMAIL_PASSWORD, manager=None)
        email.send_email()
        await sleep(61)


def parser_to_contact():
    '''Ok	2025-12-23 22:00:59.740490	subject=2030-01-01T11:00:00Z_test_testyy_Cobit2019C_proctor-1	last_name_rus=Тестый	first_name_rus=Тест	email=test@test.tt	date_from_file=01.01.2030	date_exam=2030-01-01 11:00:00	username=test_testyy	password=test_testyy_P9777	url=https://itexpert.proctoring.online?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY5MDExZWYzOWI4MjQ5Y2I1NDllMWRmNyIsImV4cCI6MTc2NjUzODA1NSwiaG9zdCI6Iml0ZXhwZXJ0LnByb2N0b3Jpbmcub25saW5lIiwidXNlcm5hbWUiOiJ0ZXN0X3Rlc3R5eSIsIm5pY2tuYW1lIjoidGVzdEB0ZXN0LnR0Iiwicm9sZSI6InN0dWRlbnQiLCJyb29tIjoiNjk0NGQxNGI3YzYyY2YwMmQ2MjMxY2EzIiwiaWF0IjoxNzY2NTE2NDU1fQ.h77QAHBUNJN4KJZpxN4sw_Xr5vHWHrpmcRlrKq9uo9c	exam=Cobit2019C	moodle_id_exam=21	moodle_id_user=19
    '''
    pass


if __name__ == '__main__':
    contacts = get_contacts_from_logs()
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
