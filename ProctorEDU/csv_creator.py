import csv

from ProctorEDU.config import csv_header_session, csv_header_user, SESSIONS_CSV_FILE, USERS_CSV_FILE
from Contact import Contact


async def create_csv(contacts: list[Contact]):
    with open(SESSIONS_CSV_FILE, 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = csv_header_session.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for contact in contacts:
            csv_header_session.update({
                'student.username': contact.username,
                'members': f'proctor-{contact.proctor}',
                'subject': contact.subject,
                'identifier': contact.identifier,
                'scheduledAt': contact.scheduled_at,
                'deadline': contact.deadline,
                'removeAt': contact.remove_at,
            })

            writer.writerow(csv_header_session)

    with open(USERS_CSV_FILE, 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = csv_header_user.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for contact in contacts:
            csv_header_user.update({
                'nickname': contact.email,
                'username': contact.username,
                'password': contact.password,
            })
            writer.writerow(csv_header_user)
