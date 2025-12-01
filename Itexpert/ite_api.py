import datetime
import json
from pprint import pprint
from typing import Optional

import requests
from requests.structures import CaseInsensitiveDict

from Contact import Contact, parser_str_to_contact
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

    def update_exam_by_id(self, user: Contact, id, id_exam) -> Optional[requests.Response]:
        """Создает новый экзамен, используя данные из объекта Contact."""

        # Полный URL для создания экзамена
        url = self._get_full_url(EXAM_ENDPOINT)

        exam_data = {
            "name": user.email,
            "login": user.username,
            "pass": user.password,
            "active": True,
            # Экзамен id из списка экзаменов
            "exam_in": str(id_exam),
            "exam_date": f'{user.date_exam.strftime("%d.%m.%Y")}',
            "exam_time": f'{user.date_exam.strftime("%H:%M")}',
            # Proctor
            "exam_type": "Online",
            # "insurance_certificate": "false",
            "link": user.url_proctor,
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


# --- Пример использования (блок if __name__ == '__main__':) ---

if __name__ == '__main__':

    s = '''Ok	2025-10-29 17:12:02.371940	subject=2025-10-31T11:00:00Z_nadezhda_smirnova_ITIL4FC_proctor-0	lastName=Смирнова	firstName=Надежда	email=smirnova_nv@tkbbank.ru	username=nadezhda_smirnova	password=nadezhda_smirnova_P5076	url=None
Ok	2025-10-29 17:12:02.371940	subject=2025-10-31T11:00:00Z_pavel_belov_ITIL4FC_proctor-0	lastName=Белов	firstName=Павел	email=belov_pa@tkbbank.ru	username=pavel_belov	password=pavel_belov_P4657	url=None
Ok	2025-10-29 17:12:02.371940	subject=2025-10-31T11:00:00Z_aleksey_slinkov_ITIL4FC_proctor-0	lastName=Слинков	firstName=Алексей	email=slinkov_ai@tkbbank.ru	username=aleksey_slinkov	password=aleksey_slinkov_P6299	url=None
Ok	2025-10-30 09:28:04.203309	subject=2025-10-31T11:00:00Z_denis_isaev_OPSC_proctor-0	lastName=Исаев	firstName=Денис	email=observer3d@gmail.com	username=denis_isaev	password=denis_isaev_P2879	url=None
Ok	2025-10-30 13:30:48.452475	subject=2025-10-30T13:35:00Z_aleksey_belyaev_OPSC_proctor-1	lastName=Беляев	firstName=Алексей	email=a.belyaev@itexpert.ru	username=aleksey_belyaev	password=aleksey_belyaev_P9058	url=https://itexpert.proctoring.online?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY5MDMzZTQ4NzY2MzI4YWZiY2I2NWYwOSIsImV4cCI6MTc2MTg0MTg0NCwiaG9zdCI6Iml0ZXhwZXJ0LnByb2N0b3Jpbmcub25saW5lIiwidXNlcm5hbWUiOiJhbGVrc2V5X2JlbHlhZXYiLCJuaWNrbmFtZSI6ImEuYmVseWFldkBpdGV4cGVydC5ydSIsInJvbGUiOiJzdHVkZW50Iiwicm9vbSI6IjY5MDMzZTRkNzY2MzI4YWZiY2I2NWYyNiIsImlhdCI6MTc2MTgyMDI0NH0.r-a6mfz-GIz8mL262s9QmA1GOe35KHSQYzwdR2824HM
Ok	2025-11-19 15:26:10.781356	subject=2025-11-24T14:00:00Z_egor_markov_ITIL4FC_proctor-1	lastName=Марков	firstName=Егор	email=egor.markov@an-rf.ru	username=egor_markov	password=egor_markov_P6037	url=https://itexpert.proctoring.online?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY5MWRiNzQ2NjFjYjJiOWFiZTM5YjAyZiIsImV4cCI6MTc2MzU3Njc1NCwiaG9zdCI6Iml0ZXhwZXJ0LnByb2N0b3Jpbmcub25saW5lIiwidXNlcm5hbWUiOiJlZ29yX21hcmtvdiIsIm5pY2tuYW1lIjoiZWdvci5tYXJrb3ZAYW4tcmYucnUiLCJyb2xlIjoic3R1ZGVudCIsInJvb20iOiI2OTFkYjc0YjYxY2IyYjlhYmUzOWIwM2YiLCJpYXQiOjE3NjM1NTUxNTR9.CtayB_biOnFAi3Y785yo1dsc9zzYZ7qfW3V2347QYiI	moolde_id_exam=2	moolde_id_user=20
Ok	2025-11-19 15:26:10.781356	subject=2025-11-21T14:00:00Z_artyom_brylyov_ITIL4FC_proctor-1	lastName=Брылёв 	firstName=Артём	email=brylev_aa@tkbbank.ru	username=artyom_brylyov	password=artyom_brylyov_P7690	url=https://itexpert.proctoring.online?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1ZDMxY2RlOTM3MTgxYzI0OTdmNjZmNCIsImV4cCI6MTc2MzU3Njc1OSwiaG9zdCI6Iml0ZXhwZXJ0LnByb2N0b3Jpbmcub25saW5lIiwidXNlcm5hbWUiOiJPbGdhX0t1cHJpZW5rbyIsIm5pY2tuYW1lIjoiby5rdXByaWVua29AaXRleHBlcnQucnUiLCJyb2xlIjoic3R1ZGVudCIsInJvb20iOiI2NWQzMWNlNDkzNzE4MWMyNDk3ZjY3MDUiLCJpYXQiOjE3NjM1NTUxNTl9.t5PJ689B7pkSqFrmXYMSq8pmN_GC-l3ZYieCGgCQDBo	moolde_id_exam=2	moolde_id_user=21
Ok	2025-11-19 15:26:10.781356	subject=2025-12-02T11:00:00Z_olga_rybkina_ICSC_proctor-1	lastName=Рыбкина 	firstName=Ольга	email=olga.n.ribkina@bspb.ru	username=olga_rybkina	password=olga_rybkina_P2178	url=https://itexpert.proctoring.online?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1ZDMxY2RlOTM3MTgxYzI0OTdmNjZmNCIsImV4cCI6MTc2MzU3Njc2NSwiaG9zdCI6Iml0ZXhwZXJ0LnByb2N0b3Jpbmcub25saW5lIiwidXNlcm5hbWUiOiJPbGdhX0t1cHJpZW5rbyIsIm5pY2tuYW1lIjoiby5rdXByaWVua29AaXRleHBlcnQucnUiLCJyb2xlIjoic3R1ZGVudCIsInJvb20iOiI2NWQzMWNlNDkzNzE4MWMyNDk3ZjY3MDUiLCJpYXQiOjE3NjM1NTUxNjV9.3XPJ6hSykTOBL7eYwGbUoBe8ipb6igEursSV3lShk6Q	moolde_id_exam=25	moolde_id_user=22
Ok	2025-11-28 16:34:26.909828	subject=2030-01-01T11:00:00Z_test_testyy_ITIL4FC_proctor-1	last_name_rus=Тестый	first_name_rus=Тест	email=g.savushkin@itexpert.ru	date_from_file=01.01.2030	username=test_testyy	password=test_testyy_P5453	url=https://itexpert.proctoring.online?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY5MDExZWYzOWI4MjQ5Y2I1NDllMWRmNyIsImV4cCI6MTc2NDM1ODQ2MiwiaG9zdCI6Iml0ZXhwZXJ0LnByb2N0b3Jpbmcub25saW5lIiwidXNlcm5hbWUiOiJ0ZXN0X3Rlc3R5eSIsIm5pY2tuYW1lIjoidGVzdEB0ZXN0LnR0Iiwicm9sZSI6InN0dWRlbnQiLCJyb29tIjoiNjkyOWE0ZDg3NWQwZTFiNjRkYjhiOWI1IiwiaWF0IjoxNzY0MzM2ODYyfQ.B1c4jD31FR9sa1WES9BLMq_8rMc1Oi3gybWEFUSmWTM	exam=ITIL4FC	moolde_id_exam=9	moolde_id_user=2	
Ok	2025-11-28 16:39:22.088184	subject=2026-01-01T11:00:00Z_grigoriy_savushkin_ITIL4FC_proctor-1	last_name_rus=Савушкин	first_name_rus=Григорий	email=g.savushkin@itexpert.ru	date_from_file=01.01.2026	username=grigoriy_savushkin	password=grigoriy_savushkin_P6256	url=https://itexpert.proctoring.online?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY5MjlhNWZhY2FhOWYwNDcyOTRiNzgyZiIsImV4cCI6MTc2NDM1ODc1OCwiaG9zdCI6Iml0ZXhwZXJ0LnByb2N0b3Jpbmcub25saW5lIiwidXNlcm5hbWUiOiJncmlnb3JpeV9zYXZ1c2hraW4iLCJuaWNrbmFtZSI6Imcuc2F2dXNoa2luQGl0ZXhwZXJ0LnJ1Iiwicm9sZSI6InN0dWRlbnQiLCJyb29tIjoiNjkyOWE1ZmZjYWE5ZjA0NzI5NGI3ODYwIiwiaWF0IjoxNzY0MzM3MTU4fQ.CyodYebIdmPHIe1oERZAut6d-XyzqlHPGX4KAtgm71Q	exam=ITIL4FC	moolde_id_exam=10	moolde_id_user=2	
'''

    contact = parser_str_to_contact(s)

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
    for id_exam in [28312, 28313]:
        print(f"\n[2. get_exam_by_id({id_exam})]")
        r_id = ite_api.get_exam_by_id(id_exam)
        if r_id and r_id.ok:
            pprint(json.loads(r_id.text))
        else:
            print("Не удалось получить экзамен по ID.")

    # # 3. Тестирование создания экзамена
    # print(f"\n[3. create_exam({contact})]")
    # r_create = ite_api.create_exam(contact)
    # if r_create:
    #     print("Результат создания:", r_create.status_code)

    # # 4. Тестирование удаления экзамена
    # for id_exam_delete in [28296, ]:
    #     print(f"\n[4. delete_exam_by_id({id_exam_delete})]")
    #     r_delete = ite_api.delete_exam_by_id(id_exam_delete)
    #     print("Результат удаления:", r_delete.status_code)
    # #
    #
    # email = 'g.savushkin@itexpert.ru'
    # print(f"\n[get_exam_by_email({email})]")
    # r_id = ite_api.get_exam_by_email(email)
    # if r_id and r_id.ok:
    #     pprint(json.loads(r_id.text))
    # else:
    #     print("Не удалось получить экзамен по ID.")
