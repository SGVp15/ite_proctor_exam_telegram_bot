import time
from asyncio import sleep

from Contact import parser_str_to_contact


# from Email import EmailSending
# from Email.config import EMAIL_LOGIN, SMTP_SERVER, SMTP_PORT, EMAIL_PASSWORD, EMAIL_BCC


def exam_date():
    rows = ''
    with open('./data/log.txt', 'r', encoding='utf-8') as f:
        rows = f.read()
    contacts = []
    for row in rows.split('\n'):
        c = parser_str_to_contact(row)
        contacts.append(c)
    return contacts


async def check_log_and_send_email():
# def check_log_and_send_email():
    while True:
        text = exam_date()
        if text:
            print(text)
            # email = EmailSending(
            #     subject=f'Экзамены {text}', from_email=EMAIL_LOGIN, to=EMAIL_BCC, cc='', bcc='',
            #     text=text, html='', smtp_server=SMTP_SERVER, smtp_port=SMTP_PORT,
            #     login=EMAIL_LOGIN, password=EMAIL_PASSWORD, manager=None)
            # email.send_email()
        # time.sleep(60)
        await sleep(60)

if __name__ == '__main__':
    check_log_and_send_email()
