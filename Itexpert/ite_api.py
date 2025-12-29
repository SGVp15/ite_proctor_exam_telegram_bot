import json
import re
import time
from datetime import datetime
from pathlib import Path
from pprint import pprint
from typing import Optional

import dateparser
import requests
from requests.structures import CaseInsensitiveDict

from Contact import Contact
from Itexpert.check_log_send_email import get_contacts_from_logs
from Itexpert.config import ITEXPERT_URL, ITEXPERT_API_SECRET_KEY, OUT_DIR_CERT
from Utils.log import log
from Utils.utils import file_to_base64
from parset_se import parse_all_repots

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
        if not r.ok:
            print(f'get_exam_dict_code_id -> {r.status_code=}')
            return {}
        j = r.json()
        list_exam = j.get('data')
        exam_dict_code_id = {}
        for el in list_exam:
            if el.get('code') == 'ITSMC':
                el['code'] = 'ITIL4FC'
            exam_dict_code_id[el.get('code')] = el.get('id')
        return exam_dict_code_id

    def get_exam_dict_id_code(self) -> dict:
        exam_dict_id_code = {v: k for k, v in self.get_exam_dict_code_id().items()}
        return exam_dict_id_code

    # --- Методы POST/DELETE ---

    def create_exam(self, contact: Contact) -> Optional[requests.Response]:
        """Создает новый экзамен, используя данные из объекта Contact."""
        id_exam = self.get_exam_dict_code_id().get(contact.exam.upper())
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

    def update_exam(self, id, contact: Contact) -> Optional[requests.Response]:
        """Создает новый экзамен, используя данные из объекта Contact."""
        id_exam = self.get_exam_dict_code_id().get(contact.exam.upper())
        url = self._get_full_url(EXAM_ENDPOINT)

        exam_type = "Offline"
        if contact.proctor:
            exam_type = "Online"

        exam_data = {
            "id": id,
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
            "link": '',
            # "link": contact.url_proctor,
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

    def get_exams_by_email(self, email: str) -> []:
        """
        Получает список ID экзаменов для заданного email.

        :param email: Email пользователя
        :return: Список ID экзаменов
        """
        exam_ids = []
        response = self.get_exam_by_email(email)

        if response and response.ok:
            try:
                data = response.json().get('data', [])
                for exam in data:
                    if exam:
                        exam_ids.append(exam)
            except (json.JSONDecodeError, AttributeError, KeyError) as e:
                print(f"❌ Ошибка при парсинге ответа для email {email}: {e}")
        else:
            print(
                f"❌ Не удалось получить экзамены для email {email}. Статус: {response.status_code if response else 'None'}")

        return exam_ids


def get_today_exams(current_date=None) -> [Contact]:
    """
    Получает все контакты из LOG_FILE, фильтрует по дате и получает ID экзаменов для каждого в exam_id

    :return: contacts: [Contact]
    """
    if not current_date:
        current_date = datetime.now().date()
    contacts = get_contacts_from_logs()

    today_contacts = []
    api = ITEXPERT_API()

    id_exam_and_code_dict = ITEXPERT_API().get_exam_dict_id_code()
    if not id_exam_and_code_dict:
        return []
    for contact in contacts:
        # Проверяем, что у контакта есть дата экзамена и она совпадает с текущей датой
        if contact.date_exam and contact.date_exam.date() == current_date.date():
            email = contact.email
            if email:
                exams = api.get_exams_by_email(email)
                for exam in exams:
                    if contact.date_exam.date() == dateparser.parse(exam.get('exam_date')).date():
                        if contact.exam.upper() == id_exam_and_code_dict.get(exam.get('exam_in')):
                            contact.exam_id = exam.get('id')
                today_contacts.append(contact)
    return today_contacts


def send_all_reports_and_cert(current_date):
    if not current_date:
        current_date = datetime.now().date()
    contacts = get_today_exams(current_date=current_date)
    for c in contacts:
        pprint(c)
    # print(f"\n--- Тестирование API с базовым URL: {ITEXPERT_URL} ---")

    # Инициализация
    ite_api = ITEXPERT_API()

    list_reports = parse_all_repots()
    for c in contacts:
        c: Contact
        for r in list_reports:
            if f'{c.first_name_rus} {c.last_name_rus}'.strip() != r.get('username'):
                continue
            if c.date_exam.date() != r.get('date'):
                continue
            if c.exam.upper() != r.get('exam_name').upper():
                continue
            try:
                id = c.exam_id
            except AttributeError:
                continue
            file_path_report = r.get('file')
            r_update = ite_api.add_review_to_exam_by_id(
                id=id,
                file_path=file_path_report,
                # name='r_48.html',
            )
            time.sleep(2)
            if r_update:
                log.info("Результат:", r_update.status_code)
            if r_update.ok:
                log.info(f"[OK] Send to www.itexpert.ru {file_path_report}")

            for file_path in Path(OUT_DIR_CERT).rglob("*.png"):
                if not file_path.is_file():
                    continue
                file_name = str(file_path.name)

                if (c.exam not in file_name or
                        c.date_exam.strftime("%Y.%m.%d") not in file_name
                        or c.exam not in file_name):
                    continue

                cert_path = file_name
                cert_name = re.sub('[ а-яА-я]+_*', '', Path(cert_path).name)
                cert_name = re.sub('^_', '', cert_name)
                log.info(f"Send to www.itexpert.ru {file_path}")
                r_update = ite_api.add_cert_to_exam_by_id(
                    id=id,
                    file_path=file_path,
                    name=cert_name,
                )
                if r_update:
                    print("Результат:", r_update.status_code)

    # -------------------------------------------------------------------
    # id = 00000
    # r_update = ite_api.add_review_to_exam_by_id(
    #     id=id,
    #     file_path='./data/reports/r_48.html',
    #     name='r_48.html',
    # )
    # if r_update:
    #     print("Результат:", r_update.status_code)


if __name__ == '__main__':
    send_all_reports_and_cert(
        # dateparser.parse('2025.12.26')
    )
    time.sleep(1)
    # # 3. Добавление сертификата в ЛК
    # id = 28495
    # cert_path = 'data/cert/Сертификат_ITIL4FC_2025.12.26_Юртаев Александр_264_yurtaev_av@tkbbank.ru.png'
    #
    # cert_name = re.sub('[ а-яА-я]+_*', '', Path(cert_path).name)
    # cert_name = re.sub('^_', '', cert_name)
    #
    # print(f"\n[5. add_cert_to_exam_by_id()]")
    # r_update = ITEXPERT_API().add_cert_to_exam_by_id(
    #     id=id,
    #     file_path=cert_path,
    #     name=cert_name,
    # )
    # if r_update:
    #     print("Результат:", r_update.status_code)

    # # 1. Тестирование получения списка экзаменов
    # print("\n[1. get_list_exams(active=True)]")
    # r_list = ite_api.get_list_exams(active=True)
    # if r_list and r_list.ok:
    #     list_exams = json.loads(r_list.text)['data']
    #     pprint(list_exams)
    # else:
    #     print("Не удалось получить список экзаменов.")
    #
    # for contact in contacts:
    #     print(f'{contact.exam=},')

    # # 2. Тестирование получения экзамена по ID
    # for id_exam in [28312, 28313]:
    #     print(f"\n[2. get_exam_by_id({id_exam})]")
    #     r_id = ite_api.get_exam_by_id(id_exam)
    #     if r_id and r_id.ok:
    #         pprint(json.loads(r_id.text))
    #     else:
    #         print("Не удалось получить экзамен по ID.")

    # # 3. Тестирование создания экзамена
    # print(f"\n[3. create_exam({contact})]")
    # r_create = ite_api.create_exam(contact)
    # if r_create:
    #     print("Результат создания:", r_create.status_code)

    # # 4. Тестирование удаления экзамена
    # for id_exam_delete in (28501,28500):
    #     print(f"\n[4. delete_exam_by_id({id_exam_delete})]")
    #     r_delete = ite_api.delete_exam_by_id(id_exam_delete)
    #     print("Результат удаления:", r_delete.status_code)

    # print(f"\n[get_exam_by_email({email})]")
    # r_id = ite_api.get_exam_by_email(email)
    # if r_id and r_id.ok:
    #     user_exams = json.loads(r_id.text)['data']
    #     pprint(user_exams)
    # else:
    #     print("Не удалось получить экзамен по ID.")
    #
    # for user_exam in user_exams:
    #     print(user_exam)
