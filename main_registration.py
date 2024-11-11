import asyncio
from random import choice

from Contact import Contact
from config import LOG_FILE
from Email.config import EMAIL_BCC
from Ispring.ispring2 import IspringApi
from parser import get_all_courses, get_all_users
from ProctorEDU.csv_creator import create_csv
from ProctorEDU.selenium_for_proctoredu import ProctorEduSelenium
from My_jinja.my_jinja import MyJinja
from Email import EmailSending, template_email_registration_exam_offline, template_email_registration_exam_online
from Utils.log import log


async def registration(contacts: [Contact]) -> str:
    out_str = ''
    # -------------- ProctorEDU --------------
    contacts_proctor = [c for c in contacts if c.proctor]
    if contacts_proctor:
        # Create CSV for ProctorEDU
        await create_csv(contacts_proctor)

        # Webdriver ProctorEDU
        drive = ProctorEduSelenium()
        await drive.create_users_and_session()

        # Get link ProctorEDU
        for contact in contacts:
            if contact.proctor:
                contact.url_proctor = await drive.get_url_session(contact.subject)
                if contact.url_proctor == '':
                    log.warning(f"\n\n[error] NOT found URL {contact}\n\n")
                    contacts.remove(contact)
        drive.quit()

    # -------------- ISPRING --------------
    ispring_api = IspringApi()

    emails_user_id = {}

    for user in get_all_users(ispring_api.get_users()):
        emails_user_id.update({user['EMAIL']: user['userId']})

    # # delete contact ispring
    # for contact in contacts:
    #     contact.id_ispring = emails_user_id.get(contact.email, None)
    #     if contact.id_ispring:
    #         ispring_api.delete_user(contact.id_ispring)
    #         log.warning(contact.email, ' - deleted')
    #         contact.id_ispring = None

    # Create ispring users with email <==> id_ispring and reset password if user exist
    for contact in contacts:
        contact.id_ispring = emails_user_id.get(contact.email, None)
        if contact.id_ispring is None:
            for user in get_all_users(ispring_api.get_users()):
                emails_user_id.update({user['EMAIL']: user['userId']})
        contact.id_ispring = emails_user_id.get(contact.email, None)

        if contact.id_ispring is None:
            contact.id_ispring = ispring_api.create_user(contact)
        else:
            ispring_api.reset_password(contact)
            log.warning(f' {contact.email} [reset password]')
        log.warning(contact.id_ispring)

    # Get all courses ispring
    courses_content_item_id: dict = get_all_courses(ispring_api.get_content())

    # User registration for the exam in ISPRING
    for contact in contacts:
        course_id = choice(courses_content_item_id[contact.exam])
        contact.is_create_enrollment = ispring_api.create_enrollment(learner_id=contact.id_ispring,
                                                                     course_id=course_id,
                                                                     access_date=contact.scheduled_at)
        if contact.is_create_enrollment is False:
            out_str += f'[Error] ISPRINT ENROLLMENT {contact}\n'

    # -------------- SEND EMAIL --------------
    for contact in contacts:
        if contact.is_create_enrollment:
            if contact.proctor:
                text = MyJinja(template_file=template_email_registration_exam_online).render_document(user=contact)
            else:
                text = MyJinja(template_file=template_email_registration_exam_offline).render_document(user=contact)
            subject = f'Вы зарегистрированы на экзамен {contact.exam} {contact.date_exam}'
            if contact.proctor and not contact.url_proctor:
                out_str += f'[Error] URL {contact}\n'
                log.error(f'[Error] URL {contact}')
                continue
            EmailSending(subject=subject, to=contact.email, bcc=EMAIL_BCC, text=text).send_email()
            contact.status = 'Ok'
        else:
            out_str += f'[Error] ISPRING not enrollment {contact}\n'
            log.error(f'[Error] ISPRING not enrollment {contact}')

    # Write Log
    with open(LOG_FILE, mode='a', encoding='utf-8') as f:
        for contact in contacts:
            f.write(str(contact))
            log.info(contact)

    for contact in contacts:
        out_str += (f'{contact.last_name_rus} {contact.first_name_rus} '
                    f'{contact.email} {contact.exam} {contact.date_exam}\n')
    return out_str


if __name__ == '__main__':
    asyncio.run(registration())
