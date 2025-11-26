from asyncio import sleep

from Email import EmailSending
from Email.config import EMAIL_LOGIN, SMTP_SERVER, SMTP_PORT, EMAIL_PASSWORD, EMAIL_BCC


def exam_date():
    data = ''
    return data


async def check_log_and_send_email():
    while True:
        text = exam_date()
        if text:
            email = EmailSending(
                subject=f'Экзамены {text}', from_email=EMAIL_LOGIN, to=EMAIL_BCC, cc='', bcc='',
                text=text, html='', smtp_server=SMTP_SERVER, smtp_port=SMTP_PORT,
                login=EMAIL_LOGIN, password=EMAIL_PASSWORD, manager=None)
            email.send_email()
        await sleep(60)
