import datetime
import json
import re
import time
from pathlib import Path
from pprint import pprint
from typing import Optional

import requests
from requests.structures import CaseInsensitiveDict

from Contact import Contact, load_contacts_from_log_file
from Itexpert.config import ITEXPERT_URL, ITEXPERT_API_SECRET_KEY
from Moodle.config import DIR_REPORTS, DIR_CERTS
from Utils.log import log
from Utils.utils import file_to_base64

EXAM_ENDPOINT = '/rus/tools/api/exam/'


class ITEXPERT_API:
    """
    Класс для взаимодействия с API управления экзаменами.
    """

    def __init__(self):
        self.url_base = ITEXPERT_URL

        # Заголовки для всех запросов
        self.headers = CaseInsensitiveDict({
            'X-API-KEY': ITEXPERT_API_SECRET_KEY,
            'Content-Type': 'application/json'
        })

    def _get_full_url(self, path: str) -> str:
        """Создает полный URL, объединяя базовый URL и путь."""
        # Удаляем лишние слэши, чтобы избежать 'http://domain.com//path'
        base = self.url_base.rstrip('/')
        path = path.lstrip('/')
        return f'{base}/{path}'

    def _send_request_get(self, url: str) -> requests.Response:
        """Внутренний метод для выполнения GET-запросов."""
        print(f'Выполняется GET запрос: {url=}')
        return requests.get(url=url, headers=self.headers)

    def get_exam_by_id(self, id_exam: Optional[str]) -> Optional[requests.Response]:
        """Получает информацию об экзамене по его ID."""
        if not id_exam:
            print("❌ ID экзамена не предоставлен.")
            return None

        path = f'{EXAM_ENDPOINT}?id={id_exam}'
        url = self._get_full_url(path)
        return self._send_request_get(url)

    def get_exam_by_email(self, email: Optional[str]) -> Optional[requests.Response]:
        """Получает информацию об экзамене по его ID."""
        if not email:
            print("❌ email не предоставлен.")
            return None

        # Предполагаем, что запрос для получения по ID выглядит так: /rus/tools/api/exam/?id=...
        path = f'{EXAM_ENDPOINT}?name={email}'
        url = self._get_full_url(path)
        return self._send_request_get(url)

    def get_list_exams(self, active: Optional[bool] = None) -> requests.Response:
        """
        Получает список экзаменов.
        :param active: True для активных, False для неактивных, None для всех.
        """
        # Предполагаем, что запрос для получения списка выглядит так: /rus/tools/api/exam/?action=getlist&active=...
        path = f'{EXAM_ENDPOINT}?action=getlist'

        if active is not None:
            path += f'&active={str(active).lower()}'

        url = self._get_full_url(path)
        return self._send_request_get(url)

    def get_exam_dict_code_id(self) -> dict:
        r = self.get_list_exams(active=True)
        j = r.json()
        list_exam = j.get('data')
        exam_dict_code_id = {}
        for el in list_exam:
            exam_dict_code_id[el.get('code')] = el.get('id')
        exam_dict_code_id['ITIL4FC'] = exam_dict_code_id.get('ITSMC')
        return exam_dict_code_id

    # --- Методы POST/DELETE ---

    def create_exam(self, contact: Contact) -> Optional[requests.Response]:
        """Создает новый экзамен, используя данные из объекта Contact."""
        id_exam = self.get_exam_dict_code_id().get(contact.exam)
        url = self._get_full_url(EXAM_ENDPOINT)

        exam_type = "Offline"
        if contact.proctor:
            exam_type = "Online"

        exam_data = {
            "name": contact.email,
            "login": contact.username,
            "pass": contact.password,
            "active": True,
            # Экзамен id из списка экзаменов
            "exam_in": str(id_exam),
            "exam_date": f'{contact.date_exam.strftime("%d.%m.%Y")}',
            "exam_time": f'{contact.date_exam.strftime("%H:%M")}',
            # Proctor
            "exam_type": exam_type,
            # "insurance_certificate": "false",
            "link": contact.url_proctor,
            # "certificate": {
            #     "base64": "base64_encoded_file_content_CERT",
            #     "name": "certificate.pdf",
            #     "type": "application/pdf"
            # },
            # "result": {
            #     "base64": "base64_encoded_file_content_RESULT",
            #     "name": "result.pdf",
            #     "type": "application/pdf"
            # }
        }

        print(f"Выполняется POST-запрос: {url=}")
        print(exam_data)
        try:
            # Отправка POST-запроса с автоматической сериализацией JSON
            response = requests.post(url, headers=self.headers, json=exam_data)

            # Проверяем статус ответа
            response.raise_for_status()

            print(f"✅ Успешный ответ. Статус код: {response.status_code}")

            # Попытка вывода JSON-ответа
            try:
                print("Тело ответа (JSON):")
                print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            except json.JSONDecodeError:
                print("Тело ответа не является JSON-объектом или пустое.")
                print(f"Текстовый ответ: {response.text}")

            return response

        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка при выполнении запроса: {e}")
            # Переменная response может быть не определена в случае ошибки DNS/соединения
            if 'response' in locals() and response is not None:
                print(f"Статус код ошибки: {response.status_code}")
                print(f"Ответ сервера: {response.text}")
            return None

    def add_review_to_exam_by_id(
            self,
            id,
            file_path: str,
            name: str = ''
    ) -> Optional[requests.Response]:
        url = self._get_full_url(EXAM_ENDPOINT)
        if not name:
            name = Path(file_path).name
        exam_data = {
            'id': id,
            "result": {
                "base64": file_to_base64(file_path),
                "name": name,
            }
        }

        print(f"Выполняется POST-запрос: {url=}")

        try:
            # Отправка POST-запроса с автоматической сериализацией JSON
            response = requests.put(url, headers=self.headers, json=exam_data)

            # Проверяем статус ответа
            response.raise_for_status()

            print(f"✅ Успешный ответ. Статус код: {response.status_code}")

            # Попытка вывода JSON-ответа
            try:
                print("Тело ответа (JSON):")
                print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            except json.JSONDecodeError:
                print("Тело ответа не является JSON-объектом или пустое.")
                print(f"Текстовый ответ: {response.text}")

            return response

        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка при выполнении запроса: {e}")
            # Переменная response может быть не определена в случае ошибки DNS/соединения
            if 'response' in locals() and response is not None:
                print(f"Статус код ошибки: {response.status_code}")
                print(f"Ответ сервера: {response.text}")
            return None

    def add_cert_to_exam_by_id(
            self,
            id,
            file_path,
            name: str = '',
    ) -> Optional[requests.Response]:
        url = self._get_full_url(EXAM_ENDPOINT)
        if not name:
            name = Path(file_path).name
        exam_data = {
            'id': id,
            "certificate": {
                "base64": file_to_base64(file_path),
                "name": name,
            },
        }

        print(f"Выполняется POST-запрос: {url=}")

        try:
            # Отправка POST-запроса с автоматической сериализацией JSON
            response = requests.put(url, headers=self.headers, json=exam_data)

            # Проверяем статус ответа
            response.raise_for_status()

            print(f"✅ Успешный ответ. Статус код: {response.status_code}")

            # Попытка вывода JSON-ответа
            try:
                print("Тело ответа (JSON):")
                print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            except json.JSONDecodeError:
                print("Тело ответа не является JSON-объектом или пустое.")
                print(f"Текстовый ответ: {response.text}")

            return response

        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка при выполнении запроса: {e}")
            # Переменная response может быть не определена в случае ошибки DNS/соединения
            if 'response' in locals() and response is not None:
                print(f"Статус код ошибки: {response.status_code}")
                print(f"Ответ сервера: {response.text}")
            return None

    def delete_exam_by_id(self, exam_id: str) -> requests.Response:
        """Удаляет экзамен по его ID."""
        # Полный URL для удаления экзамена
        url = self._get_full_url(EXAM_ENDPOINT)
        print(f"Выполняется DELETE-запрос: {url=}")
        # Удаление часто использует тело JSON с ID
        return requests.delete(url=url, headers=self.headers, json={'id': exam_id})


def get_actual_exams_id_code_dict():
    # 1. Тестирование получения списка экзаменов
    print("\n[1. get_list_exams(active=True)]")
    response_ = ITEXPERT_API().get_list_exams(active=True)
    result = {}
    if response_ and response_.ok:
        data = json.loads(response_.text)['data']
        result = {item['id']: item['code'] for item in data}
    else:
        log.error("Не удалось получить список экзаменов.")
    result = mapping_exam_name_values(result)
    return result


def mapping_exam_name_values(old_dict: dict):
    mapping = {'ITSMC': 'ITIL4FC'}
    new_dict = {k: mapping.get(v, v) for k, v in old_dict.items()}
    return new_dict


def sent_report_and_cert_lk(date: datetime.datetime | None = None):
    if not date:
        d_delta = datetime.timedelta(days=1)
        current_day = datetime.datetime.now().date() - d_delta
        current_day = datetime.datetime.combine(current_day, datetime.time.min)
    else:
        current_day = datetime.datetime.combine(date, datetime.time.min)

    date_contact = []
    contacts = load_contacts_from_log_file()
    for c in contacts:
        c: Contact
        if not c:
            continue
        if c.date_exam == current_day:
            date_contact.append(c)
            print(c)

    all_cert_files = [f for f in DIR_CERTS.rglob('*') if f.is_file() and f.suffix == '.png']
    all_report_files = [f for f in DIR_REPORTS.rglob('*') if f.is_file() and f.suffix == '.html']

    ite_api = ITEXPERT_API()

    list_exams = get_actual_exams_id_code_dict()
    time.sleep(1)

    for c in date_contact:
        email = c.email
        # print(f"\n[get_exam_by_email({email})]")
        r_id = ite_api.get_exam_by_email(email)
        if r_id and r_id.ok:
            user_exams = json.loads(r_id.text)['data']
            # pprint(user_exams)
        else:
            print("Не удалось получить экзамен по ID.")
        time.sleep(1)

        for user_exam in user_exams:
            user_exam['exam'] = list_exams.get(user_exam.get('exam_in'), '')
            if c.exam.lower() != user_exam.get('exam', '').lower():
                continue
            if c.date_exam != current_day:
                continue

            c.exam_id_itexpert = user_exam.get('id')
            break

        pprint(user_exams)
        # 3. Добавление сертификата в ЛК
        id = c.exam_id_itexpert
        cert_files = [f for f in all_cert_files if c.email in f.name and c.exam in f.name]
        for cert_path in cert_files:
            if c.date_exam.strftime('_%Y.%m.%d_') not in cert_path.name:
                continue

            cert_name = re.sub('[ а-яА-яЁё]+_*', '', Path(cert_path).name)
            cert_name = re.sub('^_', '', cert_name)

            print(f"\n[3. add_cert_to_exam_by_id()]")
            r_update = ite_api.add_cert_to_exam_by_id(
                id=id,
                file_path=cert_path,
                name=cert_name,
            )
            if r_update:
                print("Результат:", r_update.status_code)
                time.sleep(1)

        report_files = [f for f in all_report_files if
                        c.last_name_rus in f.name
                        and c.first_name_rus in f.name
                        and c.exam in f.name]

        for file_report in report_files:
            if c.date_exam.strftime('_%Y.%m.%d_') not in file_report.name:
                continue

            r_update = ite_api.add_review_to_exam_by_id(
                id=id,
                file_path=file_report,
                name=file_report.name,
            )
            if r_update:
                print("Результат:", r_update.status_code)
            time.sleep(1)


if __name__ == '__main__':
    sent_report_and_cert_lk(date=datetime.datetime(year=2026, month=1, day=20))
    # main()
