import os

from dotenv import dotenv_values, find_dotenv

config = dotenv_values(find_dotenv())

BOT_TOKEN = config.get('BOT_TOKEN')
ADMIN_ID = [int(x) for x in config['ADMIN_ID'].split(',')]
USERS_ID = [int(x) for x in config['USERS_ID'].split(',')]

QUEUE = './data/queue.txt'

LOG_FILE = './data/log.txt'
LOG_BACKUP = './data/.history.txt'
COURSES_FILE = './data/.courses.txt'
COURSES_FILE_BACKUP = './data/.courses_backup.txt'
LOG_PROGRAM = './logs.txt'

# ====================================================================================================================
# -- CSV -- CSV -- CSV -- CSV -- CSV -- CSV -- CSV -- CSV -- CSV -- CSV -- CSV -- CSV -- CSV -- CSV -- CSV -- CSV -- CS

SESSIONS_CSV_FILE = os.path.join(os.getcwd(), 'data', 'output', 'csv', 'sessions_import.csv')
USERS_CSV_FILE = os.path.join(os.getcwd(), 'data', 'output', 'csv', 'users_import.csv')

# == CSV == CSV == CSV == CSV == CSV == CSV == CSV == CSV == CSV == CSV == CSV == CSV == CSV == CSV == CSV == CSV ==
# ====================================================================================================================


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


#  ====================================================================================================================
#  -- ISPRING -- ISPRING -- ISPRING -- ISPRING -- ISPRING -- ISPRING -- ISPRING -- ISPRING -- ISPRING -- ISPRING -- ISP

LOGIN_ISPRING = config.get('LOGIN_ISPRING')
PASSWORD_ISPRING = config.get('PASSWORD_ISPRING')
DOMAIN_ISPRING = 'https://itexpert.ispringlearn.ru'

#  == ISPRING == ISPRING == ISPRING == ISPRING == ISPRING == ISPRING == ISPRING == ISPRING == ISPRING == ISPRING == ISP
#  ====================================================================================================================


#  ====================================================================================================================
#  -- PROCTOREDU -- PROCTOREDU -- PROCTOREDU -- PROCTOREDU -- PROCTOREDU -- PROCTOREDU -- PROCTOREDU -- PROCTOREDU -- P

LOGIN_PROCTOREDU = config.get('LOGIN_PROCTOREDU')
PASSWORD_PROCTOREDU = config.get('PASSWORD_PROCTOREDU')

csv_header_session = {
    'identifier': 'Date_Name_Exam',
    # 'provider': '',
    'subject': 'Date_Name_Exam',
    'locale': 'ru',
    'timezone': '3',
    'attempt': '1',
    'timeout': '10',
    'lifetime': '60',
    'deadline': '',
    # 'rules': '',
    'url': 'https://itexpert.ispringlearn.ru/',
    'api': '',
    'addons': 'check,face,ready,track,record,screen,webrtc,content,preview,chat,finish,toolbox,shared',
    'metrics': 'b1,b2,b3,c1,c2,c3,c4,c5,k1,m1,n1,n2,s1,s2,m2',
    'weights': '1,1,1,1,0.5,1,0.5,1,1,1,1,1,1,1,1',
    'threshold': '70',
    'scheduledAt': '',
    'removeAt': '',
    # 'expires': '',
    # 'status': '',
    # 'tags': '',
    'members': 'proctor-1',
    # 'invites': '',
    # 'quorum': '',
    # 'concurrent': '',
    # 'scale': '',
    # 'grade': '',
    # 'student.id': '',
    'student.username': '',
    # 'student.nickname': '',
    # 'student.verified': '',
    # 'proctor.id': '',
    # 'proctor.username': '',
    # 'proctor.nickname': '',
    # 'createdAt': '',
    # 'startedAt': '',
    # 'stoppedAt': '',
    # 'pausedAt': '',
    # 'signedAt': '',
    # 'error': '',
    # 'duration': '',
    # 'chatAt': '',
    # 'incidents': '',
    # 'conclusion': '',
    # 'comment': '',
}

csv_header_user = {
    'nickname': 'email',
    'username': 'username',
    'password': 'password',
    'role': 'student',
    'lang': 'ru',
}
#  == PROCTOREDU == PROCTOREDU == PROCTOREDU == PROCTOREDU == PROCTOREDU == PROCTOREDU == PROCTOREDU == PROCTOREDU == P
#  ====================================================================================================================


#  ====================================================================================================================
#  -- WEBDRIVER -- WEBDRIVER -- WEBDRIVER -- WEBDRIVER -- WEBDRIVER -- WEBDRIVER -- WEBDRIVER -- WEBDRIVER -- WEBDRIVER
EXECUTABLE_PATH_WEBDRIVER = r'./chromedriver.exe'
#  == WEBDRIVER == WEBDRIVER == WEBDRIVER == WEBDRIVER == WEBDRIVER == WEBDRIVER == WEBDRIVER == WEBDRIVER == WEBDRIVER
#  ====================================================================================================================


EMAIL_PASSWORD = config.get('EMAIL_PASSWORD')
EMAIL_LOGIN = config.get('EMAIL_LOGIN')

SMTP_SERVER = 'smtp.yandex.ru'
SMTP_PORT = 465

EMAIL_BCC = ['v.gromakov@itexpert.ru', 'g.savushkin@itexpert.ru', 'o.kuprienko@itexpert.ru']
EMAIL_BCC_course = ['g.savushkin@itexpert.ru', 'a.rybalkin@itexpert.ru', 'kab@itexpert.ru']

email_login_password = {}
template_folder = './Email/template_email/'
