import datetime
import re
import xml.etree.ElementTree as ET

from openpyxl.reader.excel import load_workbook

from Contact import Contact
from Telegram.config import (
    TEMPLATE_FILE_XLSX,
    PAGE_NAME,
    LastName_column, FirstName_column, Email_column, Exam_column,
    Date_column, Hour_column, Minute_column,
    FirstNameEng_column, LastNameEng_column,
    Proctor_column, Password_column
)


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
    """

    :rtype: object
    """
    root = ET.fromstring(xml)
    users: list[dict] = []
    for i, group1 in enumerate(root.findall('userProfile')):
        # print(group1.find('userId').text)
        users.append({'userId': group1.find('userId').text})
        for group2 in group1.findall('fields'):
            for group3 in group2.findall('field'):
                # print(group3.find('name').text)
                # print(group3.find('value').text)
                users[i].update({group3.find('name').text: group3.find('value').text})
    return users


def clean_export_excel(s):
    s = s.replace(',', ', ')
    s = re.sub(r'\s{2,}', ' ', s)
    s = s.strip()
    if s in ('None', '#N/A'):
        s = ''
    return s


def read_excel(excel, column, row):
    sheet_ranges = excel[PAGE_NAME]
    return str(sheet_ranges[f'{column}{row}'].value)


def get_contact_from_excel(filename=TEMPLATE_FILE_XLSX) -> list[Contact]:
    file_excel = load_workbook(filename=filename, data_only=True)
    users = []
    i = 1
    while i < 1000:
        i += 1
        user = Contact()

        user.last_name_rus = clean_export_excel(read_excel(file_excel, column=LastName_column, row=i)).capitalize().strip()
        if user.last_name_rus == '':
            continue
        user.first_name_rus = clean_export_excel(read_excel(file_excel, column=FirstName_column, row=i)).capitalize().strip()
        user.email = clean_export_excel(read_excel(file_excel, column=Email_column, row=i)).lower().strip()
        user.password = clean_export_excel(read_excel(file_excel, column=Password_column, row=i)).strip()

        user.exam = clean_export_excel(read_excel(file_excel, column=Exam_column, row=i)).strip()

        user.date_from_file = clean_export_excel(read_excel(file_excel, column=Date_column, row=i)).lower().strip()

        hour = int(round(float(clean_export_excel(read_excel(file_excel, column=Hour_column, row=i)).lower())))
        minute = int(round(float(clean_export_excel(read_excel(file_excel, column=Minute_column, row=i)).lower())))

        user.first_name_eng = clean_export_excel(
            read_excel(file_excel, column=FirstNameEng_column, row=i)).capitalize().strip()
        user.last_name_eng = clean_export_excel(
            read_excel(file_excel, column=LastNameEng_column, row=i)).capitalize().strip()
        user.proctor = clean_export_excel(read_excel(file_excel, column=Proctor_column, row=i)).lower().strip()
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
