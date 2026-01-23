import datetime
from unittest import TestCase

from Contact import load_contacts_from_log_file
# from Config.config import user_id_email
# from Contact import parser

from Email import EmailSending, template_email_registration_exam_offline, template_email_registration_exam_online
from Email.template import template_email_exam_result_passed, template_email_exam_result_failed

from My_jinja import MyJinja


class TestEmailSending(TestCase):
    @staticmethod
    def test_send_email():
        contacts = load_contacts_from_log_file(filtered_date=datetime.datetime.now())
        print(contacts)
        for contact in contacts:
            templates = [
                # template_email_registration_exam_offline,
                #          template_email_registration_exam_online,
                         template_email_exam_result_passed,
                         template_email_exam_result_failed,
                         ]
            for template in templates:
                text = MyJinja(template_file=template).render_document(user=contact)
                EmailSending(to='g.savushkin@itexpert.ru',
                             # text='text',
                             html=text).send_email()
