import asyncio
from random import choice

from Config.config import TEMPLATE_FILE_XLSX, LOG_FILE, EMAIL_BСС
from ispring2 import IspringApi
from parser import get_all_courses, get_all_users, get_contact_from_excel
from proctor_edu import create_csv
from selenium_for_proctoredu import Proctor
from My_jinja.my_jinja import MyJinja
from Email import EmailSending, template_email_registration_exam_offline, template_email_registration_exam_online


async def registration(file=TEMPLATE_FILE_XLSX):
    contacts = get_contact_from_excel(file)
    if not contacts:
        return
    ispring_api = IspringApi()
    courses_content_item_id: dict = get_all_courses(ispring_api.get_content())
    all_users_ispring = get_all_users(ispring_api.get_user())
    emails_user_id = {}
    for user in all_users_ispring:
        emails_user_id.update({user['EMAIL']: user['userId']})
    for contact in contacts:
        contact.id_ispring = emails_user_id.get(contact.email, '')

    # создать пользователя привязка к email
    emails = [str(x['EMAIL']).lower() for x in all_users_ispring]
    for contact in contacts:
        if contact.email not in emails:
            contact.id_ispring = ispring_api.create_user(contact)
            print(contact.id_ispring)
        else:
            ispring_api.reset_password(contact)

    all_users_ispring = get_all_users(ispring_api.get_user())
    emails_user_id = {}
    for user in all_users_ispring:
        emails_user_id.update({user['EMAIL']: user['userId']})
    for contact in contacts:
        contact.id_ispring = emails_user_id[contact.email]

    # назначить пользователя

    all_users_ispring = get_all_users(ispring_api.get_user())

    # # Delete users in ISPRING
    # for contact in contacts:
    #     ispringApi.delete_user(contact.id_ispring)
    #     print(f'[delete] {contact}')
    # print('del - ok')
    # time.sleep(100_000)

    # ProctorEDU
    contacts_proctor = [c for c in contacts if c.proctor]
    if contacts_proctor:
        # Create CSV for ProctorEDU
        await create_csv(contacts_proctor)

        # Webdriver ProctorEDU
        drive = Proctor()
        await drive.create_users_and_session()

        # Get link ProctorEDU
        for contact in contacts:
            if contact.proctor:
                contact.url_proctor = await drive.get_url_session(contact.subject)
                if contact.url_proctor == '':
                    print(f"\n\n[error] NOT found URL {contact}\n\n")
                    contacts.remove(contact)
        drive.quit()

    # User registration for the exam in ISPRING
    for contact in contacts:
        course_id = choice(courses_content_item_id[contact.exam])
        contact.is_create_enrollment = ispring_api.create_enrollment(learner_id=contact.id_ispring,
                                                                     course_id=course_id,
                                                                     access_date=contact.scheduledAt)

    # Send email
    for contact in contacts:
        if contact.proctor and contact.is_create_enrollment:
            text = MyJinja(template_file=template_email_registration_exam_online).render_document(user=contact)
        else:
            text = MyJinja(template_file=template_email_registration_exam_offline).render_document(user=contact)

        subject = f'Вы зарегистрированы на экзамен {contact.exam} {contact.dateExam}'
        EmailSending(subject=subject, to=contact.email, bcc=EMAIL_BСС, text=text).send_email()

    # Write Log
    with open(LOG_FILE, mode='a', encoding='utf-8') as f:
        for contact in contacts:
            f.write(str(contact))
            print(contact)


if __name__ == '__main__':
    asyncio.run(registration())
