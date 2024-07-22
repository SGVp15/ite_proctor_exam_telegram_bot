import os

from dotenv import dotenv_values, find_dotenv

config = dotenv_values(find_dotenv())

BOT_TOKEN: str | None = config.get('BOT_TOKEN')
ADMIN_ID: list[int] = [int(x) for x in config['ADMIN_ID'].split(',')]
USERS_ID: list[int] = [int(x) for x in config['USERS_ID'].split(',')]

LOG_FILE: str = os.path.join(os.getcwd(), 'data', 'log.txt')

#  ====================================================================================================================
#  -- EXCEL -- EXCEL -- EXCEL -- EXCEL -- EXCEL -- EXCEL -- EXCEL -- EXCEL -- EXCEL -- EXCEL -- EXCEL -- EXCEL -- EXCEL

TEMPLATE_FILE_XLSX: str = os.path.join(os.getcwd(), 'data', 'output', 'template', 'template.xlsx')
PAGE_NAME: str = 'Экзамены'

LastName_column: str = 'A'
FirstName_column: str = 'B'
LastNameEng_column: str = 'C'
FirstNameEng_column: str = 'D'
Email_column: str = 'E'
Password_column: str = 'F'
Exam_column: str = 'G'
Date_column: str = 'H'
Hour_column: str = 'I'
Minute_column: str = 'J'
Proctor_column: str = 'K'

#  == EXCEL == EXCEL == EXCEL == EXCEL == EXCEL == EXCEL == EXCEL == EXCEL == EXCEL == EXCEL == EXCEL == EXCEL == EXCEL
#  ====================================================================================================================

DOCUMENTS: str = os.path.join(os.getcwd(), 'data', 'input', 'documents')

PATH_DOWNLOAD_FILE: str = os.path.join(os.getcwd(), 'data', 'input')
