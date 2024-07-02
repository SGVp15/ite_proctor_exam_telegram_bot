import datetime
import random
import hashlib
from translit import transliterate, transliterate_error


class UserIspring:
    def __init__(self):
        '''<?xml version="1.0" encoding="UTF-8"?>
<response>
    <userProfile>
        <role>owner</role>
        <roleId>eaefe76e-2ae1-11e9-b90a-0242ac13000a</roleId>
        <userId>114dba08-a75e-11eb-b4e5-0242ac13002a</userId>
        <departmentId>1141d74c-a75e-11eb-ad56-0242ac13002a</departmentId>
        <status>1</status>
        <fields>
            <field>
                <name>FIRST_NAME</name>
                <value>Account</value>
            </field>
            <field>
                <name>LAST_NAME</name>
                <value>Owner</value>
            </field>
            <field>
                <name>LOGIN</name>
                <value>owner</value>
            </field>
            <field>
                <name>EMAIL</name>
                <value>owner@test.com</value>
            </field>
            <field>
                <name>PHONE</name>
                <value></value>
            </field>
            <field>
                <name>JOB_TITLE</name>
                <value></value>
            </field>
            <field>
                <name>COUNTRY</name>
                <value></value>
            </field>
        </fields>
        <addedDate>2021-04-27</addedDate>
        <lastLoginDate>2021-09-14</lastLoginDate>
        <manageableDepartmentIds>
            <id>1141d74c-a75e-11eb-ad56-0242ac13002a</id>
        </manageableDepartmentIds>
        <userRoles>
            <userRole>
                <roleId>eaefe76e-2ae1-11e9-b90a-0242ac13000a</roleId>
                <roleType>owner</roleType>
                <manageableDepartmentIds>
                    <id>1141d74c-a75e-11eb-ad56-0242ac13002a</id>
                </manageableDepartmentIds>
            </userRole>
            <userRole>
                <roleId>ab513fba-fc2e-11eb-a2f0-0242ac130034</roleId>
                <roleType>custom</roleType>
                <manageableDepartmentIds>
                    <id>1141d74c-a75e-11eb-ad56-0242ac13002a</id>
                </manageableDepartmentIds>
            </userRole>
        </userRoles>
    </userProfile>
</response>'''


#         self.name_eng: str | None = None
#         self.last_name_rus: str | None = None
#         self.first_name_rus: str | None = None
#         self.last_name_eng: str | None = None
#         self.first_name_eng: str | None = None
#         self.email: str | None = None
#         self.username: str | None = None
#         self.password: str | None = None
#         self.exam: str | None = None
#         self.course: str | None = None
#         self.course_small: str | None = None
#         self.lector: str | None = None
#         self.date_from_file = None
#         self.date_exam = None
#         self.date_exam_connect: str | None = None
#         self.remove_at: str | None = None
#         self.deadline: str | None = None
#         self.scheduled_at: str | None = None
#         self.proctor: str | None = None
#         self.subject: str | None = None
#         self.date_exam_for_subject = None
#         self.url_proctor: str | None = None
#         self.url_course: str | None = None
#         self.id_ispring: str | None = None
#         self.status_ispring: str | None = None
#         self.identifier: str | None = None
#         self.is_create_enrollment: bool = False
#         self.status = 'Error'
#
#     def normalize(self) -> bool:
#         if self.first_name_eng == '' or self.first_name_eng is None:
#             self.first_name_eng = transliterate(f'{self.first_name_rus}').capitalize()
#         else:
#             self.first_name_eng = transliterate_error(self.first_name_eng)
#
#         if self.last_name_eng == '' or self.last_name_eng is None:
#             self.last_name_eng = transliterate(f'{self.last_name_rus}').capitalize()
#         else:
#             self.last_name_eng = transliterate_error(self.last_name_eng)
#
#         self.email = transliterate_error(self.email.strip())
#
#         self.name_eng = f'{self.first_name_eng} {self.last_name_eng}'
#
#         if datetime.datetime.now() > self.date_exam:
#             return False
#
#         self.date_exam_connect = self.date_exam - datetime.timedelta(minutes=5)
#         self.scheduled_at = self.date_exam + datetime.timedelta(hours=-3)
#         deadline = self.scheduled_at + datetime.timedelta(hours=2)
#         remove_at = self.scheduled_at + datetime.timedelta(days=90)
#
#         pattern_time = "%Y-%m-%dT%H:%M:%SZ"
#         self.date_exam_for_subject = self.date_exam.strftime(pattern_time)
#         self.deadline = deadline.strftime(pattern_time)
#         self.remove_at = remove_at.strftime(pattern_time)
#
#         self.username = self.name_eng.replace(' ', '_')
#
#         if self.proctor == '' or self.proctor is None:
#             self.proctor = None
#
#         if self.password == '' or self.password is None:
#             self.password = f'{self.username}_{random.randint(1000, 9999)}'
#
#         self.subject = f'{self.date_exam_for_subject}_{self.username}_' \
#                        f'{self.exam}_proctor-{self.proctor}'
#         self.identifier = to_md5(f'{self.date_from_file.replace(".", "-")}_{self.username}_{self.exam}')
#         return True
#
#     def __str__(self) -> str:
#         self.s = f'{self.status}\t{datetime.datetime.now()}\tsubject={self.subject}\t' \
#                  f'lastName={self.last_name_rus}\tfirstName={self.first_name_rus}\t' \
#                  f'email={self.email}\tusername={self.username}\tpassword={self.password}\t' \
#                  f'url={self.url_proctor}\n'
#         return self.s
#
#     def __eq__(self, other):
#         if self.email == other.email:
#             return True
#
#         return False
#
#
# def to_md5(s: str):
#     return hashlib.md5(s.encode()).hexdigest()
