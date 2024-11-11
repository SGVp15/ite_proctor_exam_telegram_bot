import datetime
import re
import xml.etree.ElementTree as ET

from Contact import Contact
from EXCEL.my_excel import read_excel_file
from config import TEMPLATE_FILE_XLSX


def get_all_courses(xml: str) -> dict:
    root = ET.fromstring(xml)
    courses: dict = {}
    list_courses = []
    for i, group1 in enumerate(root.findall('contentItem')):
        _ = group1.find('contentItemId').text
        list_courses.append({group1.find('title').text: group1.find('contentItemId').text})
    for course_dict in list_courses:
        course_name = list(course_dict.keys())[0]
        if course_name in list(courses.keys()):
            courses[course_name].append(course_dict[course_name])
        else:
            courses[course_name] = [course_dict[course_name]]

    return courses


def get_all_users(xml: str) -> list[dict]:
    root = ET.fromstring(xml)
    users: list[dict] = []
    for i, group1 in enumerate(root.findall('userProfile')):
        users.append({'userId': group1.find('userId').text})
        for group2 in group1.findall('fields'):
            for group3 in group2.findall('field'):
                users[i].update({group3.find('name').text: group3.find('value').text})
    return users


def clean_string(s: str):
    if type(s) is str:
        s = s.replace(',', ', ')
        s = re.sub(r'\s{2,}', ' ', s)
        s = s.strip()
    elif s in ('None', '#N/A', None):
        s = ''
    return s


def get_contact_from_data(filename=TEMPLATE_FILE_XLSX) -> list[Contact]:
    users = []
    sheet_data: dict = read_excel_file(filename=filename, sheet_names=('Экзамены',))
    sheet_data = sheet_data.get('Экзамены')
    for data in sheet_data[1:]:
        user = Contact()

        # LastName_column: str = 'A'	0
        # FirstName_column: str = 'B'	1
        # LastNameEng_column: str = 'C'	2
        # FirstNameEng_column: str = 'D'	3
        # Email_column: str = 'E'	4
        # Password_column: str = 'F'	5
        # Exam_column: str = 'G'	6
        # Date_column: str = 'H'	7
        # Hour_column: str = 'I'	8
        # Minute_column: str = 'J'	9
        # Proctor_column: str = 'K'	10

        if data[0] is None:
            continue
        user.last_name_rus = clean_string(data[0]).capitalize()
        if user.last_name_rus in (None, ''):
            continue
        user.first_name_rus = clean_string(data[1]).capitalize()
        user.last_name_eng = clean_string(data[2]).capitalize()
        user.first_name_eng = clean_string(data[3]).capitalize()
        user.email = clean_string(data[4]).lower()
        user.password = clean_string(data[5])
        user.exam = clean_string(data[6])
        user.date_from_file = clean_string(data[7]).lower()
        hour = int(clean_string(data[8]))
        minute = int(clean_string(data[9]))

        user.proctor = clean_string(data[10])
        t = user.date_from_file
        t = re.sub(r'[^\d.]', '', t)
        t = t.split('.')
        t = list(map(int, t))
        # 2023-02-02T13:29:31Z

        # contact.dateExam = datetime.datetime(2023, 5, 13, hour, minute)
        year = t[2]
        month = t[1]
        day = t[0]
        user.date_exam = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)

        if user.normalize():
            users.append(user)
    return users


def get_contact_from_excel(file):
    contacts: list[Contact] = get_contact_from_data(file)
    if len(contacts) == 0:
        return None
    return contacts
