import csv

from ProctorEDU.config import CSV_HEADER_SESSION, CSV_HEADER_USER, SESSIONS_CSV_FILE, USERS_CSV_FILE
from Contact import Contact


async def create_csv_files(contacts: list[Contact]):
    with open(SESSIONS_CSV_FILE, 'w', encoding='utf-8', newline='') as csvfile:
        rows = []
        for contact in contacts:
            rows.append({
                'student.username': contact.username,
                'members': f'proctor-{contact.proctor}',
                'subject': contact.subject,
                'identifier': contact.identifier,
                'scheduledAt': contact.scheduled_at,
                'openAt': contact.open_at,
                'closeAt': contact.close_at,
                'deadline': contact.deadline,
                'removeAt': contact.remove_at,
            })
        rows_field = [row.keys() for row in rows]
        field_names = list(set(list(CSV_HEADER_SESSION.keys()) + list(rows_field)))
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()

        for row in rows:
            writer.writerow(row)

    with open(USERS_CSV_FILE, 'w', encoding='utf-8', newline='') as csvfile:
        field_names = CSV_HEADER_USER.keys()
        writer = csv.DictWriter(csvfile, fieldnames=field_names)

        writer.writeheader()

        for contact in contacts:
            CSV_HEADER_USER.update({
                'nickname': contact.email,
                'username': contact.username,
                'password': contact.password,
            })
            writer.writerow(CSV_HEADER_USER)
