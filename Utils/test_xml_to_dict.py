from unittest import TestCase

from Ispring.ispring2 import IspringApi
from Utils.xml_to_dict import get_ispring_users


class Test(TestCase):
    def test_get_ispring_users(self):
        s = IspringApi().get_users()
        users = get_ispring_users(s)
        print(users)
