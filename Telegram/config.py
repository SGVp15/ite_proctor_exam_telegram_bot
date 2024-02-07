import os

from dotenv import dotenv_values, find_dotenv

config = dotenv_values(find_dotenv())

BOT_TOKEN: str | None = config.get('BOT_TOKEN')
ADMIN_ID: list[int] = [int(x) for x in config['ADMIN_ID'].split(',')]
USERS_ID: list[int] = [int(x) for x in config['USERS_ID'].split(',')]

LOG_FILE: str = './data/log.txt'

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
