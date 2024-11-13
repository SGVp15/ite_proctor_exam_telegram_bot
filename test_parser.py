from unittest import TestCase

from Contact import Contact
from parser import get_contact_from_data


class Test(TestCase):
    def test_get_contact_from_excel(self):
        users: [Contact] = get_contact_from_data()
        # self.fail()
