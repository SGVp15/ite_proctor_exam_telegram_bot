from pprint import pprint
from unittest import TestCase

from Moodle.API.moodle_api import MOODLE_API


class TestMOODLE_API(TestCase):
    # def test_core_user_create_users(self):
    #     api = MOODLE_API()
    #     api.core_user_create_users()
    #     self.fail()

    # def test_core_course_get_courses(self):
    #     api = MOODLE_API()
    #     courses = api.core_course_get_courses()
    #     pprint(courses)

    def test__get_id_shortname_course(self):
        api = MOODLE_API()
        courses = api._get_id_shortname_course()
        requested_shortname='BAF'
        possible_courses = [
            shortname for shortname in courses.keys()
            if shortname.startswith(requested_shortname)
        ]
        pprint(possible_courses)
