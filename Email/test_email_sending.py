import datetime
from unittest import TestCase

from Contact import load_contacts_from_log_file
from Email import EmailSending
from Email.template import template_email_exam_result_passed, template_email_exam_result_failed, \
    template_email_registration_exam_online, template_email_registration_exam_offline
from My_jinja import MyJinja


class TestEmailSending(TestCase):
    @staticmethod
    def test_send_email():
        # 2026-01-30
        contacts = load_contacts_from_log_file(filtered_date=datetime.datetime(2026, 1, 30))
        print(contacts)
        for contact in contacts:
            templates = [
                # template_email_registration_exam_offline,
                # template_email_registration_exam_online,
                # template_email_exam_result_passed,
                template_email_exam_result_failed,
            ]
            for template in templates:
                html_text = MyJinja(template_file=template).render_document(user=contact)
                EmailSending(
                    # to=[contact.email, ],
                    bcc=['g.savushkin@itexpert.ru', ],
                    subject='test_email',
                    # text='text',
                    html=html_text
                ).send_email()
