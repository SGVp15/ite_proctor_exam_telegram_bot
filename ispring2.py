import re
import xml.etree.ElementTree as ET
from datetime import datetime

import requests
from requests.structures import CaseInsensitiveDict

from Contact import Contact
from Config.config import LOGIN_ISPRING, PASSWORD_ISPRING, DOMAIN_ISPRING


class ApiIspringRequest:
    def __init__(self):
        self.url_base = 'https://api-learn.ispringlearn.ru/'
        self.headers = CaseInsensitiveDict()
        self.headers = {'X-Auth-Email': f'{LOGIN_ISPRING}',
                        'X-Auth-Password': f'{PASSWORD_ISPRING}',
                        'X-Auth-Account-Url': f'{DOMAIN_ISPRING}',
                        'Content-Type': 'application/xml'}

    def get_user(self):
        url = self.url_base + 'user'
        response = requests.get(url=url, headers=self.headers)
        return response.text

    def create_user(self, user: Contact, department_id='2745eb28-449c-11ed-8def-3ea1876893eb', role='learner',
                    send_login_email='false',
                    invitation_message='Используйте следующие данные, чтобы войти в Академию iSpring:'):

        xml = f'<?xml version="1.0" encoding="UTF-8"?>' \
              f'<request>' \
              f'    <departmentId>{department_id}</departmentId>' \
              f'    <password>{user.password}</password>' \
              f'    <fields>' \
              f'        <login>{user.username}</login>' \
              f'        <email>{user.email}</email>' \
              f'        <first_name>{user.firstName}</first_name>' \
              f'        <last_name>{user.lastName}</last_name>' \
              f'    </fields>' \
              f'    <role>{role}</role>' \
              f'    <sendLoginEmail>{send_login_email}</sendLoginEmail>' \
              f'    <invitationMessage>{invitation_message}</invitationMessage>' \
              f'</request>'

        url = self.url_base + 'user'
        response = requests.post(url=url, headers=self.headers, data=xml.encode('utf-8'))
        userid = re.findall(r'<response>(.*)</response>', response.text)[0]
        print(f'{__name__} - ok')
        return userid

    def reset_password(self, user: Contact):
        xml = f'<?xml version="1.0" encoding="UTF-8"?>' \
              f'<request>' \
              f'    <password>{user.password}</password>' \
              f'</request>'

        url = self.url_base + f'user/{user.id_ispring}/password'
        response = requests.post(url=url, headers=self.headers, data=xml.encode('utf-8'))
        print(f'{__name__}\t{response.status_code}')

    def get_content(self):
        url = self.url_base + 'content'
        response = requests.get(url=url, headers=self.headers)
        return response.text

    def create_enrollment(self, learner_id: str, course_id: str, access_date: datetime,
                          due_date_type='due_period') -> None:
        """
        :param learner_id:
        :param course_id:
        :param access_date:
        :param due_date_type: 'unlimited','due_date','due_period'
        :return:
        """

        xml = f'<?xml version="1.0" encoding="UTF-8"?>' \
              f'<request>' \
              f'    <courseIds>' \
              f'        <id>{course_id}</id>' \
              f'    </courseIds>' \
              f'    <learnerIds>' \
              f'        <id>{learner_id}</id>' \
              f'    </learnerIds>' \
              f'    <accessDate>{access_date}</accessDate>' \
              f'    <dueDateType>due_period</dueDateType>' \
              f'    <dueDate>2023-12-20 10:30:00</dueDate>' \
              f'    <duePeriod>3</duePeriod>' \
              f'</request>'

        root = ET.fromstring(xml)
        for courseIds in root.iter('courseIds'):
            courseIds.set('id', 'yes')

        url = self.url_base + 'enrollment'
        response = requests.post(url=url, headers=self.headers, data=xml.encode('utf-8'))
        if response.status_code == 201:
            print('Курс назначен')
        else:
            print('Курс не назначен')

    def delete_user(self, userid):
        url = self.url_base + 'user' + f'/{userid}'
        response = requests.delete(url=url, headers=self.headers)
        print(response.status_code)
        print(response.text)

    def create_group(self, name_group, user_ids: list[str]):
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

        url = self.url_base + 'group'
        response = requests.post(url=url, headers=self.headers, data=xml.encode('utf-8'))
        print(response.status_code)
        print(response.text)
        group_id = re.findall(r'<response>(.*)</response>', response.text)[0]
        return group_id
