import os

from dotenv import dotenv_values, find_dotenv

config = dotenv_values(find_dotenv())

BOT_TOKEN: str | None = config.get('BOT_TOKEN')
ADMIN_ID: list[int] = [int(x) for x in config['ADMIN_ID'].split(',')]
USERS_ID: list[int] = [int(x) for x in config['USERS_ID'].split(',')]

QUEUE: str = './data/queue.txt'

LOG_FILE: str = './data/log.txt'
LOG_BACKUP: str = './data/.history.txt'
COURSES_FILE: str = './data/.courses.txt'
COURSES_FILE_BACKUP: str = './data/.courses_backup.txt'
LOG_PROGRAM: str = './logs.txt'


#  ====================================================================================================================
#  -- EXCEL -- EXCEL -- EXCEL -- EXCEL -- EXCEL -- EXCEL -- EXCEL -- EXCEL -- EXCEL -- EXCEL -- EXCEL -- EXCEL -- EXCEL

TEMPLATE_FILE_XLSX = os.path.join(os.getcwd(), 'data', 'output', 'template', 'template.xlsx')
PAGE_NAME = 'Экзамены'

LastName_column = 'A'
FirstName_column = 'B'
LastNameEng_column = 'C'
FirstNameEng_column = 'D'
Email_column = 'E'
Password_column = 'F'
Exam_column = 'G'
Date_column = 'H'
Hour_column = 'I'
Minute_column = 'J'
Proctor_column = 'K'
#  == EXCEL == EXCEL == EXCEL == EXCEL == EXCEL == EXCEL == EXCEL == EXCEL == EXCEL == EXCEL == EXCEL == EXCEL == EXCEL
#  ====================================================================================================================

EMAIL_PASSWORD = config.get('EMAIL_PASSWORD')
EMAIL_LOGIN = config.get('EMAIL_LOGIN')

SMTP_SERVER = 'smtp.yandex.ru'
SMTP_PORT = 465

EMAIL_BCC = ['v.gromakov@itexpert.ru', 'g.savushkin@itexpert.ru', 'o.kuprienko@itexpert.ru']
EMAIL_BCC_course = ['g.savushkin@itexpert.ru', 'a.rybalkin@itexpert.ru', 'kab@itexpert.ru']

email_login_password = {}
template_folder = './Email/template_email/'
