import urllib.parse
from random import choice

import requests

from Contact import Contact
from Utils.log import log
from config import MOODLE_URL, MOODLE_TOKEN


class MOODLE_API:
    RESPONSE_FORMAT = 'json'
    API_URL = f'{MOODLE_URL}/webservice/rest/server.php'

    def core_user_get_users_by_field(self, value: str, field='email', ):
        """ - field can be 'id' or 'idnumber' or 'username' or 'email'"""
        FUNCTION_NAME = "core_user_get_users_by_field"

        # Кодирование параметров для URL
        url_with_params = self.__get_url_with_params(FUNCTION_NAME)

        # --- 3. Параметры, передаваемые в теле POST (Данные функции) ---

        post_data_dict = {
            'field': field,  # Поле, по которому ищем
            'values[0]': value
        }

        # --- 4. Выполнение POST-запроса ---
        try:
            response = requests.post(
                url_with_params,
                data=post_data_dict
            )

            response.raise_for_status()
            data = response.json()

            # --- 5. Обработка ответа ---
            # core_user_get_users_by_field возвращает список (array) пользователей
            if data and isinstance(data, list):
                users_list = data
                return users_list
                if users_list:
                    print("\n✅ Запрос успешен. Получен пользователь:")
                    # Выводим информацию о первом найденном пользователе
                    user: dict = users_list[0]
                    print(f"  ID: {user.get('id')}")
                    print(f"  Логин: {user.get('username')}")
                    print(f"  Полное имя: {user.get('fullname')}")
                    print(f"  Email: {user.get('email')}")
                    print(f"  Подтвержден: {user.get('confirmed')}")
                    print(user.keys())
                    return users_list
                else:
                    print(f"\n⚠️ Запрос успешен, но пользователь '{value}' не найден.")
                    print("Проверьте, правильно ли указан логин.")


            # --- 6. Обработка ошибок Moodle API ---
            elif isinstance(data, dict) and 'exception' in data:
                print("\n❌ Ошибка Moodle API:")
                print(f"  Код ошибки: {data.get('errorcode')}")
                print(f"  Сообщение: {data.get('message')}")

            else:
                # Обработка неожиданных ответов
                print(f"\n⚠️ Получен неожиданный формат ответа.")
                print(data)

        except requests.exceptions.RequestException as e:
            # Обработка сетевых ошибок (подключение, DNS, таймаут)
            print(f"\n❌ Произошла ошибка запроса (Сеть/HTTP): {e}")

    def core_user_create_users(self, user: Contact):
        '''list of (
        object {
        createpassword int  Необязательно //True if password should be created and mailed to user.
        username string   //Username policy is defined in Moodle security config.
        auth string  По умолчанию - «manual» //Auth plugins include manual, ldap, etc
        password string  Необязательно //Plain text password consisting of any characters
        firstname string   //The first name(s) of the user
        lastname string   //The family name of the user
        email string   //A valid and unique email address
        maildisplay int  Необязательно //Email visibility
        city string  Необязательно //Home city of the user
        country string  Необязательно //Home country code of the user, such as AU or CZ
        timezone string  Необязательно //Timezone code such as Australia/Perth, or 99 for default
        description string  Необязательно //User profile description, no HTML
        firstnamephonetic string  Необязательно //The first name(s) phonetically of the user
        lastnamephonetic string  Необязательно //The family name phonetically of the user
        middlename string  Необязательно //The middle name of the user
        alternatename string  Необязательно //The alternate name of the user
        interests string  Необязательно //User interests (separated by commas)
        idnumber string  По умолчанию - «» //An arbitrary ID code number perhaps from the institution
        institution string  Необязательно //institution
        department string  Необязательно //department
        phone1 string  Необязательно //Phone 1
        phone2 string  Необязательно //Phone 2
        address string  Необязательно //Postal address
        lang string  По умолчанию - «ru» //Language code such as "en", must exist on server
        calendartype string  По умолчанию - «gregorian» //Calendar type such as "gregorian", must exist on server
        theme string  Необязательно //Theme name such as "standard", must exist on server
        mailformat int  Необязательно //Mail format code is 0 for plain text, 1 for HTML etc
        customfields  Необязательно //User custom fields (also known as user profil fields)
        list of (
        object {
        type string   //The name of the custom field
        value string   //The value of the custom field
        }
        )preferences  Необязательно //User preferences
        list of (
        object {
        type string   //The name of the preference
        value string   //The value of the preference
        }
        )}
        )'''

        # --- 1. Входные данные (Настройки) ---
        FUNCTION_NAME = "core_user_create_users"

        url_with_params = self.__get_url_with_params(FUNCTION_NAME)

        # --- 3. Параметры, передаваемые в теле POST (Данные нового пользователя) ---
        # Функция core_user_create_users ожидает массив 'users'.
        NEW_USER_DATA = {
            'username': f'{user.username}',
            'password': f'{user.password}',
            'firstname': f'{user.first_name_rus}',
            'lastname': f'{user.last_name_eng}',
            'email': f'{user.email}',
        }

        # Формируем словарь для POST-запроса, используя синтаксис массива Moodle: users[0][поле]
        post_data_dict = {
            f'users[0][{key}]': value
            for key, value in NEW_USER_DATA.items()
        }

        log.info(f"Отправка POST запроса к: {url_with_params}")
        log.info(f"Попытка создать пользователя: {NEW_USER_DATA['username']}")

        # --- 4. Выполнение POST-запроса ---
        try:
            response = requests.post(
                url_with_params,
                data=post_data_dict
            )

            # Проверка статуса HTTP (200 - OK)
            response.raise_for_status()
            data = response.json()

            # --- 5. Обработка ответа ---
            # При успешном создании возвращается список созданных пользователей с их ID
            if data and isinstance(data, list) and len(data) > 0 and 'id' in data[0]:
                log.info("\n✅ Пользователь успешно создан! ")
                new_user_info = data[0]
                log.info(f"  Новый ID пользователя: {new_user_info.get('id')}")
                log.info(f"  Имя: {NEW_USER_DATA['firstname']} {NEW_USER_DATA['lastname']}")
                log.info(f"  Username: {NEW_USER_DATA['username']}")
                return new_user_info.get('id')


            # --- 6. Обработка ошибок Moodle API ---
            elif isinstance(data, dict) and 'exception' in data:
                log.error("\n❌ Ошибка Moodle API:")
                log.error(f"  Код ошибки: {data.get('errorcode')}")
                log.error(f"  Сообщение: {data.get('message')}")
                log.error("\nПолный ответ Moodle (для отладки):")
                log.error(data)

            else:
                # Обработка неожиданных ответов
                log.error(f"\n⚠️ Получен неожиданный формат ответа.")
                log.error(data)

        except requests.exceptions.RequestException as e:
            # Обработка сетевых ошибок
            log.error(f"\n❌ Произошла ошибка запроса (Сеть/HTTP): {e}")

    def core_course_get_courses(self):
        # --- 1. Входные данные ---
        FUNCTION_NAME = "core_course_get_courses"
        url_with_params = self.__get_url_with_params(FUNCTION_NAME)

        log.debug(f"Отправка POST запроса к: {url_with_params}")

        # --- 4. Выполнение POST-запроса ---
        try:
            # Отправляем POST без данных в теле, чтобы получить ВСЕ курсы.
            response = requests.post(url_with_params)
            # Проверка статуса HTTP
            response.raise_for_status()
            data = response.json()

            # --- 5. Обработка ответа ---
            if data and isinstance(data, list):
                log.debug("\n✅ Запрос успешен. Получен список курсов:")
                courses_list = data
                return courses_list
            elif isinstance(data, dict) and 'exception' in data:
                # Обработка ошибок, возвращаемых Moodle
                log.error(f"\n❌ Ошибка Moodle API: {data.get('errorcode')}")
                log.error(f"Сообщение: {data.get('message')}")
            else:
                log.error(f"\n⚠️ Неожиданный формат ответа:")
                log.error(data)

        except requests.exceptions.RequestException as err:
            log.error(f"\n❌ Произошла ошибка: {err}")

    def __get_url_with_params(self, function_name: str):
        # Кодирование параметров для URL
        url_params = {
            'wstoken': MOODLE_TOKEN,
            'wsfunction': function_name,
            'moodlewsrestformat': self.RESPONSE_FORMAT
        }
        url_with_params = self.API_URL + '?' + urllib.parse.urlencode(url_params)
        return url_with_params

    def create_users_and_registration(self, contacts: [Contact]):
        for contact in contacts:
            id = self.core_user_get_users_by_field(contact.email)
            if id:
                contact.id_moodle = id
        return

        if not emails_user_id:
            contact.id_moodle = self.create_user(contact)
        else:
            moodle_api.reset_password(contact)
            log.info(f' {contact.email} [reset password]')
        log.info(f'{contact.id_ispring=}')

        # Get all courses moodle
        courses_content_item_id: dict = self._get_id_shortname_course()

        out_str = ''

        # User registration for the exam in MOODLE
        for contact in contacts:
            course_id = choice(courses_content_item_id[contact.exam])
            contact.is_create_enrollment = self.create_enrollment(learner_id=contact.id_ispring,
                                                                  course_id=course_id,
                                                                  access_date=contact.scheduled_at)
            if not contact.is_create_enrollment:
                out_str += f'[Error] Moodle not enrollment {contact}\n'
                log.error(f'[Error] Moodle not enrollment {contact}')

        return out_str

    def _get_id_shortname_course(self) -> dict:
        d = {}
        for course in self.core_course_get_courses():
            d[course.get('shortname')] = course.get('id')
        return d
