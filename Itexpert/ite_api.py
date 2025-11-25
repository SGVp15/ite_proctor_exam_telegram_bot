import json
from pprint import pprint
from typing import Optional

import requests
from requests.structures import CaseInsensitiveDict

from Contact import Contact
from Itexpert.config import ITEXPERT_URL, ITEXPERT_API_SECRET_KEY

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

    # --- Методы GET ---

    def get_exam_by_id(self, exam_id: Optional[str]) -> Optional[requests.Response]:
        """Получает информацию об экзамене по его ID."""
        if not exam_id:
            print("❌ ID экзамена не предоставлен.")
            return None

        # Предполагаем, что запрос для получения по ID выглядит так: /rus/tools/api/exam/?id=...
        path = f'{EXAM_ENDPOINT}?id={exam_id}'
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

    # --- Методы POST/DELETE ---

    def create_exam(self, user: Contact) -> Optional[requests.Response]:
        """Создает новый экзамен, используя данные из объекта Contact."""

        # Полный URL для создания экзамена
        url = self._get_full_url(EXAM_ENDPOINT)

        # Формирование тела запроса (Payload)
        exam_data = {
            "name": "Экзамен ITIL Foundation",
            "active": True,
            # Внимание: 'exam_in' обычно - ID элемента/курса, не 'ID' как строка
            "exam_in": "Элемент экзамена ID",
            "exam_date": "15.11.2025",
            # Предполагается, что эти поля доступны в объекте Contact
            "exam_time": user.date_exam_connect,
            "exam_type": "Online",
            "insurance_certificate": True,
            "link": user.url_proctor,
            # Используйте реальные base64 данные здесь
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

        print(f"Выполняется POST-запрос: {url=}")

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

    def delete_exam_by_id(self, exam_id: str) -> requests.Response:
        """Удаляет экзамен по его ID."""
        # Полный URL для удаления экзамена
        url = self._get_full_url(EXAM_ENDPOINT)
        print(f"Выполняется DELETE-запрос: {url=}")
        # Удаление часто использует тело JSON с ID
        return requests.delete(url=url, headers=self.headers, json={'id': exam_id})


# --- Пример использования (блок if __name__ == '__main__':) ---

if __name__ == '__main__':
    # --- Фиктивные данные для тестирования (для демонстрации) ---
    class MockContact:
        def __init__(self):
            self.date_exam_connect = "14:30"
            self.url_proctor = "https://proctoring.link/user/12345"


    # Присвойте фиктивные значения (для демонстрации работы без реальных импортов)
    if 'ITEXPERT_URL' not in locals():
        ITEXPERT_URL = "https://example.com/api"
        ITEXPERT_API_SECRET_KEY = "mock_secret_key"

    print(f"\n--- Тестирование API с базовым URL: {ITEXPERT_URL} ---")

    # Инициализация
    ite_api = ITEXPERT_API()

    # 1. Тестирование получения списка экзаменов
    print("\n[1. get_list_exams(active=True)]")
    r_list = ite_api.get_list_exams(active=True)
    if r_list and r_list.ok:
        pprint(json.loads(r_list.text))
    else:
        print("Не удалось получить список экзаменов.")

    # 2. Тестирование получения экзамена по ID
    print("\n[2. get_exam_by_id('27613')]")
    r_id = ite_api.get_exam_by_id('27613')
    if r_id and r_id.ok:
        pprint(json.loads(r_id.text))
    else:
        print("Не удалось получить экзамен по ID.")

    # 3. Тестирование создания экзамена (потребует MockContact)
    # print("\n[3. create_exam()]")
    # mock_user = MockContact()
    # r_create = ite_api.create_exam(mock_user)
    # if r_create:
    #     print("Результат создания:", r_create.status_code)

    # 4. Тестирование удаления экзамена
    # print("\n[4. delete_exam_by_id('12345')]")
    # r_delete = ite_api.delete_exam_by_id('12345')
    # print("Результат удаления:", r_delete.status_code)
