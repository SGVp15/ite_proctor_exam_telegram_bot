import re
import xml.etree.ElementTree as ET
from datetime import datetime

import requests
from requests.structures import CaseInsensitiveDict

from Contact import Contact
from Ispring.config import LOGIN_ISPRING, PASSWORD_ISPRING, DOMAIN_ISPRING
from Ispring.session import Session
from Utils.xml_to_dict import get_ispring_users, get_ispring_enrollments, get_ispring_contents
from Utils.log import log


class IspringApi:
    def __init__(self):
        self.url_base = 'https://api-learn.ispringlearn.ru'
        self.headers = CaseInsensitiveDict()
        #         self.headers["Host"] = Config.Host
        #         self.headers["X-Auth-Account-Url"] = DOMAIN_ISPRING
        #         self.headers["X-Auth-Email"] = LOGIN_ISPRING
        #         self.headers["X-Auth-Password"] = PASSWORD_ISPRING
        self.headers = {'X-Auth-Email': LOGIN_ISPRING,
                        'X-Auth-Password': PASSWORD_ISPRING,
                        'X-Auth-Account-Url': DOMAIN_ISPRING,
                        'Content-Type': 'application/xml'}

    def get_users(self):
        url = '/'.join([self.url_base, 'user'])
        response = requests.get(url=url, headers=self.headers)
        return response.text

    def get_enrollments(self):
        url = '/'.join([self.url_base, 'enrollment'])
        response = requests.get(url=url, headers=self.headers)
        return response.text

    def create_user(self, user: Contact, department_id='2745eb28-449c-11ed-8def-3ea1876893eb', role='learner',
                    send_login_email='false',
                    invitation_message='Используйте следующие данные, чтобы войти в Академию iSpring:'):
        url = '/'.join([self.url_base, 'user'])
        xml = f'<?xml version="1.0" encoding="UTF-8"?>' \
              f'<request>' \
              f'    <departmentId>{department_id}</departmentId>' \
              f'    <password>{user.password}</password>' \
              f'    <fields>' \
              f'        <login>{user.username}</login>' \
              f'        <email>{user.email}</email>' \
              f'        <first_name>{user.first_name_rus}</first_name>' \
              f'        <last_name>{user.last_name_rus}</last_name>' \
              f'    </fields>' \
              f'    <role>{role}</role>' \
              f'    <sendLoginEmail>{send_login_email}</sendLoginEmail>' \
              f'    <invitationMessage>{invitation_message}</invitationMessage>' \
              f'</request>'

        response = requests.post(url=url, headers=self.headers, data=xml.encode('utf-8'))
        user_id = re.findall(r'<response>(.*)</response>', response.text)[0]
        log.info(f'{__name__} - ok')
        if response.status_code == 201:
            return user_id
        else:
            return response.status_code

    def reset_password(self, user: Contact):
        url = '/'.join([self.url_base, 'user', user.id_ispring, 'password'])
        xml = f'<?xml version="1.0" encoding="UTF-8"?>' \
              f'<request>' \
              f'    <password>{user.password}</password>' \
              f'</request>'
        response = requests.post(url=url, headers=self.headers, data=xml.encode('utf-8'))
        log.info(f'{__name__}\t{response.status_code}')

    def get_content(self):
        url = '/'.join([self.url_base, 'content'])
        response = requests.get(url=url, headers=self.headers)
        return response.text

    def create_enrollment(self, learner_id: str, course_id: str, access_date: str,
                          due_date_type='due_period') -> bool:
        """
        :param learner_id:
        :param course_id:
        :param access_date:
        :param due_date_type: 'unlimited','due_date','due_period'
        :return:
        """
        url = '/'.join([self.url_base, 'enrollment'])
        xml = f'<?xml version="1.0" encoding="UTF-8"?>' \
              f'<request>' \
              f'    <courseIds>' \
              f'        <id>{course_id}</id>' \
              f'    </courseIds>' \
              f'    <learnerIds>' \
              f'        <id>{learner_id}</id>' \
              f'    </learnerIds>' \
              f'    <accessDate>{access_date}</accessDate>' \
              f'    <dueDateType>{due_date_type}</dueDateType>' \
              f'    <duePeriod>3</duePeriod>' \
              f'</request>'

        # f'    <dueDate>2024-12-20 10:30:00</dueDate>' \
        root = ET.fromstring(xml)
        for courseIds in root.iter('courseIds'):
            courseIds.set('id', 'yes')

        response = requests.post(url=url, headers=self.headers, data=xml.encode('utf-8'))
        if 200 <= response.status_code < 300:
            log.info('Курс назначен')
            return True
        else:
            log.info('Курс не назначен')
            return False

    def delete_enrollment(self, enrollment_id: str):
        url = '/'.join([self.url_base, 'enrollment', 'delete'])
        xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<DeleteEnrollments>
    <enrollmentIds>     
    <id>{enrollment_id}</id>
    </enrollmentIds>
</DeleteEnrollments>'''

        response = requests.post(url=url, headers=self.headers, data=xml.encode('utf-8'))
        if 200 <= response.status_code < 300:
            return True
        return False

    def users_deactivate(self, users):
        url = '/'.join([self.url_base, 'users', 'deactivate'])
        ids = ''
        for user in users:
            ids += f"<userIds>{user.id_ispring}</userIds>\n"
        xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<request>
    {ids}
</request>'''
        response = requests.post(url=url, headers=self.headers, data=xml.encode('utf-8'))
        if 200 <= response.status_code < 300:
            return True
        return False

    def user_scheduled_deactivation(self, userId, date):
        url = '/'.join([self.url_base, 'user', userId, 'scheduled_deactivation'])
        xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<request>
    <date>{date}</date>
</request>'''
        response = requests.post(url=url, headers=self.headers, data=xml.encode('utf-8'))
        if 200 <= response.status_code < 300:
            return True
        return False

    def delete_user(self, userid) -> bool:
        url = '/'.join([self.url_base, 'user', userid])
        response = requests.delete(url=url, headers=self.headers)
        if 200 <= response.status_code < 300:
            return True
        else:
            log.info(response.status_code)
            log.info(response.text)
            return False

    def create_group(self, name_group, user_ids: list[str]):
        url = '/'.join([self.url_base, 'group'])
        ids = ''
        if user_ids:
            for user_id in user_ids:
                ids += f'<id>{user_id}</id>'

            ids = f'<userIds>' \
                  f'{ids}' \
                  f'</userIds>'

        xml = f'<?xml version="1.0" encoding="UTF-8"?>' \
              f'<request>' \
              f'<name>{name_group}</name>' \
              f'{ids}' \
              f'</request>'

        response = requests.post(url=url, headers=self.headers, data=xml.encode('utf-8'))
        log.info(response.status_code)
        log.info(response.text)
        group_id = re.findall(r'<response>(.*)</response>', response.text)[0]
        return group_id


def get_session_in_enrollments_users_contents() -> list[Session] | None:
    try:
        sessions: list[Session] = []
        users = get_ispring_users(IspringApi().get_users())
        enrollments = get_ispring_enrollments(IspringApi().get_enrollments())
        courses = get_ispring_contents(IspringApi().get_content())
        for enrollment in enrollments:
            for user in users:
                if enrollment.get('learnerId') == user.get('userId'):
                    for course in courses:
                        if enrollment.get('courseId') == course.get('contentItemId'):
                            sessions.append(Session(enrollment_dict=enrollment, user_dict=user, course_dict=course))
                            break
                    break
    except AttributeError:
        sessions = []
    return sessions
