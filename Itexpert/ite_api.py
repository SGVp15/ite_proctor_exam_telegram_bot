import json
from pprint import pprint

import requests
from requests.structures import CaseInsensitiveDict

from Contact import Contact
from Itexpert.config import ITEXPERT_URL, ITEXPERT_API_SECRET_KEY


# from Utils.log import log


class ITEXPERT_API:
    def __init__(self):
        self.url_base = ITEXPERT_URL
        self.headers = CaseInsensitiveDict()
        self.headers = {'X-API-KEY': ITEXPERT_API_SECRET_KEY,
                        'Content-Type': 'application/json'}

    def get_users(self):
        url = '/'.join([self.url_base, 'user'])
        response = requests.get(url=url, headers=self.headers)
        return response.text

    def get_exam_by_id(self, id=None):
        if not id:
            return ''
        url = '/'.join([self.url_base, f'?id={id}'])
        return self._send_request_get(url)

    def get_list_exams(self, active=None):
        """active=[None,True, False]"""
        url = '/'.join([self.url_base, '?action=getlist'])
        if active is not None:
            url += f'&active={str(active).lower()}'
        return self._send_request_get(url)

    def _send_request_get(self, url):
        print(f'{url=}')
        return requests.get(url=url, headers=self.headers)

    def create_exam(self, user: Contact) -> requests:
        url = self.url_base
        exam_data = {
            "name": "Экзамен ITIL Foundation",
            "active": True,
            "exam_in": "Элемент экзамена ID",
            "exam_date": "15.11.2025",
            "exam_time": user.date_exam_connect,
            "exam_type": "Online",
            "insurance_certificate": True,
            "link": user.url_proctor,
            "certificate": {
                "base64": "base64_encoded_file_content_CERT",
                "name": "certificate.pdf",
                "type": "application/pdf"
            },
            "result": {
                "base64": "base64_encoded_file_content_RESULT",
                "name": "result.pdf",
                "type": "application/pdf"
            }
        }

        try:
            response = requests.post(url, headers=self.headers, json=exam_data)

            # Проверяем статус ответа
            response.raise_for_status()  # Вызывает исключение для кодов 4xx/5xx

            print(f"✅ Успешный ответ. Статус код: {response.status_code}")
            print("Тело ответа (JSON):")

            try:
                print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            except json.JSONDecodeError:
                print("Тело ответа не является JSON-объектом или пустое.")
                print(response.text)

            return response

        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка при выполнении запроса: {e}")
            if 'response' in locals() and response is not None:
                print(f"Статус код ошибки: {response.status_code}")
                print(f"Ответ сервера: {response.text}")
            return None

    def delete_exam_by_id(self, id) -> requests:
        url = self.url_base
        return requests.delete(url=url, headers=self.headers, json={'id': id})


if __name__ == '__main__':
    ite_api = ITEXPERT_API()
    r = ite_api.get_list_exams(active=True)
    pprint(r.text)
    r = ite_api.get_exam_by_id('27613')
    pprint(r)
