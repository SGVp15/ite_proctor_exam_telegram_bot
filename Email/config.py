import os

from dotenv import dotenv_values, find_dotenv

config = dotenv_values(find_dotenv())

EMAIL_PASSWORD = config.get('EMAIL_PASSWORD')
EMAIL_LOGIN = config.get('EMAIL_LOGIN')
SMTP_SERVER = 'smtp.yandex.ru'
SMTP_PORT = 465
EMAIL_BCC = ['exam@itexpert.ru',]
EMAIL_BCC_course = ['exam@itexpert.ru',]
email_login_password = {}

TEMPLATE_FOLDER: str = os.path.join(os.getcwd(), 'Email', 'template_email')
