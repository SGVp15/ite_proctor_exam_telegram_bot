from Contact import Contact
from Itexpert.ite_api import ITEXPERT_API
from Moodle.API.moodleapi import MoodleApi
from root_config import LOG_FILE, ALLOWED_EXAMS
from Email.config import EMAIL_BCC
from ProctorEDU.csv_creator import create_csv_files
from ProctorEDU.selenium_for_proctoredu import ProctorEduSelenium
from My_jinja.my_jinja import MyJinja
from Email import EmailSending, template_email_registration_exam_offline, template_email_registration_exam_online
from Utils.log import log


async def registration(contacts: [Contact]) -> str:
    out_str = ''
    exams = [contact.exam for contact in contacts]
    for exam in exams:
        if exam not in ALLOWED_EXAMS:
            return 'Проверьте курс'

    # -------------- Moodle --------------
    moodle_api = MoodleApi()
    for contact in contacts:
        moodle_api.process_user_and_enrollment(contact=contact)

    # -------------- ProctorEDU --------------
    contacts_proctor = [c for c in contacts if c.proctor]
    if contacts_proctor:
        await create_csv_files(contacts_proctor)

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

    # -------------- SEND EMAIL --------------
    log.info(f'[ start ] SEND EMAIL ')
    for contact in contacts:
        # if contact.is_create_enrollment:
        if contact.proctor:
            log.info(f'MyJinja start template_email_registration_exam_online')
            text = MyJinja(template_file=template_email_registration_exam_online).render_document(user=contact)
        else:
            log.info(f'MyJinja start template_email_registration_exam_online')
            text = MyJinja(template_file=template_email_registration_exam_offline).render_document(user=contact)
        subject = f'Вы зарегистрированы на экзамен {contact.exam} {contact.date_exam}'
        if contact.proctor and not contact.url_proctor:
            out_str += f'[Error] URL {contact}\n'
            log.error(f'[Error] URL {contact}')
            continue
        EmailSending(subject=subject, to=contact.email, bcc=EMAIL_BCC, text=text).send_email()
        contact.status = 'Ok'
    log.info(f'[ end ] SEND EMAIL ')
    # Write Log
    with open(LOG_FILE, mode='a', encoding='utf-8') as f:
        for contact in contacts:
            f.write(str(contact))
            log.info(contact)

    # ITEXPERT
    ite_api = ITEXPERT_API()
    for contact in contacts:
        ite_api.create_exam(contact)

    # OUT STRING
    for contact in contacts:
        # if contact.is_create_enrollment:
        out_str += (f'{contact.last_name_rus} {contact.first_name_rus} '
                    f'{contact.email} {contact.exam} {contact.date_exam}\n')
    return out_str
