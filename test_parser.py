from unittest import TestCase

from Contact import Contact, load_contacts_from_log_file
from parser import get_contact_from_excel
from root_config import LOG_FILE


class Test(TestCase):
    def test_get_contact_from_excel(self):
        contacts_from_file: [Contact] = get_contact_from_excel()
        contacts_from_log = load_contacts_from_log_file(LOG_FILE)
        contacts = [c for c in contacts_from_file if c not in contacts_from_log]
        print('\n == ---------------------------- == \n')
        for contact in contacts:
            print(contact)
