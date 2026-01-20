import datetime
import re
import xml.etree.ElementTree as ET

import dateparser

from Contact import Contact
from EXCEL.my_excel import read_excel_file
from root_config import TEMPLATE_FILE_XLSX, PAGE_NAME


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


def get_contact_from_array(data_list) -> list[Contact]:
    users = []
    for data in data_list:
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

        if not data[0]:
            continue
        user.last_name_rus = data[0]
        user.first_name_rus = data[1]
        user.last_name_eng = data[2]
        user.first_name_eng = data[3]
        user.email = data[4]
        user.password = data[5]
        user.exam = data[6]
        user.date_from_file = dateparser.parse(data[7]).date()
        user.proctor = data[10]
        user.date_exam = dateparser.parse(f'{data[7].strip()} {str(data[8]).strip()}:{str(data[9]).strip()}')

        if user.normalize():
            users.append(user)
    return users


def get_contact_from_excel(filename=TEMPLATE_FILE_XLSX):
    sheet_data: dict = read_excel_file(filename=filename, sheet_names=(PAGE_NAME,))
    sheet_data = sheet_data.get(PAGE_NAME)

    contacts: list[Contact] = get_contact_from_array(sheet_data[1:])
    if not contacts:
        return None
    return contacts
