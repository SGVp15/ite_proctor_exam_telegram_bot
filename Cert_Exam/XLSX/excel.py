import re

import dateparser
from ..CertContact import CertContact
from ..UTILS.log import log
from ..XLSX.my_excel import read_excel_file
from ..config_cert_exam import FILE_XLSX, SHEETNAME


def get_contact_from_cert_excel(filename=FILE_XLSX) -> list[CertContact]:
    rows = read_excel_file(filename).get(SHEETNAME)
    cert_contacts = []
    for row in rows:
        cert_contact = CertContact()
        # "№ сертификата	Дата экзамена	Курс	ФИО слушателя на русском	ФИО слушателя на латинице	email	Полное название	Английское название"
        try:
            cert_contact.number = int(clean_export_excel(row[0]))
            settings = {'DATE_ORDER': 'DMY'}
            cert_contact.date_exam = dateparser.parse(clean_export_excel(row[1]), settings=settings)
            if not cert_contact.date_exam:
                continue
            cert_contact.abr_exam = clean_export_excel(row[2])
            cert_contact.name_rus = clean_export_excel(row[3])
            cert_contact.name_eng = clean_export_excel(row[4])
            cert_contact.email = clean_export_excel(row[5])
            cert_contact.exam_rus = clean_export_excel(row[6])
        except (ValueError, IndexError):
            continue

        try:
            cert_contact.can_create_cert = clean_export_excel(row[10])
            '''"Создать сертификат? 
                1 - создать,
                [пусто] - автоматически создается после 2 дней, 
                9 - не создавать"
            '''
        except (ValueError, IndexError):
            cert_contact.can_create_cert = 0

        try:
            cert_contact.create_path_file()
        except (FileNotFoundError,):
            log.error(f'No template file {cert_contact.template}')
            continue

        cert_contacts.append(cert_contact)
    return cert_contacts


def clean_export_excel(s):
    s = str(s)
    s = s.replace(',', ', ')
    s = re.sub(r'\s{2,}', ' ', s)
    s = s.strip()
    if s in ('None', '#N/A'):
        s = ''
    return s
