import os

from dotenv import dotenv_values, find_dotenv

config = dotenv_values(find_dotenv())

LOGIN_PROCTOREDU = config.get('LOGIN_PROCTOREDU')
PASSWORD_PROCTOREDU = config.get('PASSWORD_PROCTOREDU')

CSV_HEADER_SESSION = {
    'identifier': 'Date_Name_Exam',
    # 'provider': '',
    'subject': 'Date_Name_Exam',
    'locale': 'ru',
    'timezone': '3',
    'attempt': '1',
    'timeout': '10',
    'lifetime': '120',
    'deadline': '',
    # 'rules': '',
    # 'url': 'https://itexpert.ispringlearn.ru/',
    'url': 'https://ururulol.space/',
    'api': '',
    # 'addons': 'check,face,ready,track,record,screen,webrtc,content,preview,chat,finish,toolbox,shared',
    'addons': 'check,face,ready,track,record,screen,webrtc,content,preview,finish,toolbox,shared',
    'metrics': 'b1,b2,b3,c1,c2,c3,c4,c5,k1,m1,m2,n1,n2,s1,s2',
    'weights': '1,1,1,1,1,1,1,1,1,1,0.5,1,1,1,1',
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
    'openAt': '',
    'closeAt': '',

    # 'pausedAt': '',
    # 'signedAt': '',
    # 'error': '',
    # 'duration': '',
    # 'chatAt': '',
    # 'incidents': '',
    # 'conclusion': '',
    # 'comment': '',
}

CSV_HEADER_USER = {
    'nickname': 'email',
    'username': 'username',
    'password': 'password',
    'role': 'student',
    'lang': 'ru',
}

SESSIONS_CSV_FILE: str = os.path.join(os.getcwd(), 'data', 'output', 'csv', 'sessions_import.csv')
USERS_CSV_FILE: str = os.path.join(os.getcwd(), 'data', 'output', 'csv', 'users_import.csv')
