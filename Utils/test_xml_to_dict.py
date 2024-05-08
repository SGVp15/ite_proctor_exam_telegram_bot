from unittest import TestCase

from Ispring.ispring2 import IspringApi
from Utils.xml_to_dict import get_ispring_users, get_ispring_enrollments, get_ispring_contents


class Test(TestCase):
    def test_get_ispring_users(self):
        s = IspringApi().get_users()
        users = get_ispring_users(s)
        print(users)

    def test_get_ispring_enrollment(self):
        s = IspringApi().get_enrollments()
        enrollments = get_ispring_enrollments(s)
        print(enrollments)

    def test_get_ispring_contents(self):
        s = IspringApi().get_content()
        courses = get_ispring_contents(s)
        print(courses)

