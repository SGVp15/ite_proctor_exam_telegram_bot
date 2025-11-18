import urllib.parse
from random import choice
from pprint import pprint

import requests

# Предполагается, что Contact, log, MOODLE_URL, MOODLE_TOKEN определены
from Contact import Contact
from Utils.log import log
from config import MOODLE_URL, MOODLE_TOKEN


class MOODLE_API:
    RESPONSE_FORMAT = 'json'
    API_URL = f'{MOODLE_URL}/webservice/rest/server.php'

    # --- ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ---

    def __get_url_with_params(self, function_name: str):
        """Формирует полный URL с токеном и функцией Moodle."""
        url_params = {
            'wstoken': MOODLE_TOKEN,
            'wsfunction': function_name,
            'moodlewsrestformat': self.RESPONSE_FORMAT
        }
        url_with_params = self.API_URL + '?' + urllib.parse.urlencode(url_params)
        return url_with_params

    @staticmethod
    def __format_post_array(data: dict, array_name: str = 'users') -> dict:
        """
        Преобразует словарь в формат POST-данных Moodle-массива:
        {'username': 'test'} -> {'users[0][username]': 'test'}
        """
        return {
            f'{array_name}[0][{key}]': value
            for key, value in data.items()
        }

    def _get_id_shortname_course(self) -> dict:
        d = {}
        for course in self.core_course_get_courses():
            d[course.get('shortname')] = course.get('id')
        return d

    # --- ОСНОВНЫЕ МЕТОДЫ API ---

    def core_user_get_users_by_field(self, value: str, field='email') -> dict:
        """
        Ищет пользователя по полю (email, username и т.д.).
        Возвращает словарь с данными пользователя или пустой словарь {}.
        """
        FUNCTION_NAME = "core_user_get_users_by_field"
        url_with_params = self.__get_url_with_params(FUNCTION_NAME)

        post_data_dict = {'field': field, 'values[0]': value}

        try:
            response = requests.post(url_with_params, data=post_data_dict)
            response.raise_for_status()
            data = response.json()

            if data and isinstance(data, list) and data:
                # Возвращаем первый найденный элемент
                return data[0]

            elif isinstance(data, dict) and 'exception' in data:
                log.error(f"❌ Ошибка Moodle API при поиске: {data.get('errorcode')}. Сообщение: {data.get('message')}")
                return {}
            else:
                return {}

        except requests.exceptions.RequestException as e:
            log.error(f"❌ Произошла ошибка запроса (Сеть/HTTP) при поиске: {e}")
            return {}

    def core_user_create_users(self, user: Contact):
        '''Создает пользователя и возвращает его ID'''
        FUNCTION_NAME = "core_user_create_users"
        url_with_params = self.__get_url_with_params(FUNCTION_NAME)

        NEW_USER_DATA = {
            'username': f'{user.username}',
            'password': f'{user.password}',
            'firstname': f'{user.first_name_rus}',
            'lastname': f'{user.last_name_eng}',
            'email': f'{user.email}',
        }

        # Используем вспомогательный метод для форматирования
        post_data_dict = self.__format_post_array(NEW_USER_DATA, array_name='users')

        log.info(f"Попытка создать пользователя: {NEW_USER_DATA['username']}")

        try:
            response = requests.post(url_with_params, data=post_data_dict)
            response.raise_for_status()
            data = response.json()

            if data and isinstance(data, list) and len(data) > 0 and 'id' in data[0]:
                new_user_info = data[0]
                log.info(f"✅ Пользователь успешно создан! ID: {new_user_info.get('id')}")
                return new_user_info.get('id')

            elif isinstance(data, dict) and 'exception' in data:
                log.error(
                    f"❌ Ошибка Moodle API при создании: {data.get('errorcode')}. Сообщение: {data.get('message')}")
                return None

            else:
                log.error(f"⚠️ Получен неожиданный формат ответа при создании: {data}")
                return None

        except requests.exceptions.RequestException as e:
            log.error(f"❌ Произошла ошибка запроса (Сеть/HTTP) при создании: {e}")
            return None

    def core_user_update_password(self, user_id: int, new_password: str) -> bool:
        '''Обновляет пароль существующего пользователя по его ID (core_user_update_users).'''
        FUNCTION_NAME = "core_user_update_users"
        url_with_params = self.__get_url_with_params(FUNCTION_NAME)

        UPDATE_DATA = {
            'id': user_id,
            'password': new_password
        }

        # Используем вспомогательный метод для форматирования
        post_data_dict = self.__format_post_array(UPDATE_DATA, array_name='users')

        log.info(f"Попытка обновить пароль для пользователя ID: {user_id}")

        try:
            response = requests.post(url_with_params, data=post_data_dict)
            response.raise_for_status()
            data = response.json() if response.text else []

            # core_user_update_users при успехе возвращает пустой список []
            if isinstance(data, list) and not data:
                return True

            elif isinstance(data, dict) and 'exception' in data:
                log.error(
                    f"❌ Ошибка Moodle API при обновлении пароля: {data.get('errorcode')}. Сообщение: {data.get('message')}")
                return False

            else:
                log.error(f"⚠️ Получен неожиданный формат ответа при обновлении пароля: {data}")
                return False

        except requests.exceptions.RequestException as e:
            log.error(f"❌ Произошла ошибка запроса (Сеть/HTTP) при обновлении пароля: {e}")
            return False

    def enrol_manual_enrol_users(self, COURSE_ID: int, USER_ID_TO_ENROL: int):
        '''Зачисляет пользователя на курс (enrol_manual_enrol_users).'''
        FUNCTION_NAME = "enrol_manual_enrol_users"
        ROLE_ID_STUDENT = 5
        url_with_params = self.__get_url_with_params(FUNCTION_NAME)

        ENROLMENT_RECORD = {
            'roleid': ROLE_ID_STUDENT,
            'userid': USER_ID_TO_ENROL,
            'courseid': COURSE_ID
        }

        # Используем вспомогательный метод для форматирования, array_name='enrolments'
        post_data_dict = self.__format_post_array(ENROLMENT_RECORD, array_name='enrolments')

        log.info(f"Попытка зачислить пользователя (ID: {USER_ID_TO_ENROL}) на курс (ID: {COURSE_ID})")

        try:
            response = requests.post(url_with_params, data=post_data_dict)
            response.raise_for_status()
            data = response.json() if response.text else []

            if isinstance(data, list) and not data:
                log.info(f"✅ Зачисление ID {USER_ID_TO_ENROL} на курс {COURSE_ID} успешно.")
                return True

            elif isinstance(data, dict) and 'exception' in data:
                log.error(
                    f"❌ Ошибка Moodle API при зачислении: {data.get('errorcode')}. Сообщение: {data.get('message')}")
                return False

            else:
                log.error(f"⚠️ Получен неожиданный формат ответа при зачислении: {data}")
                return False

        except requests.exceptions.RequestException as e:
            log.error(f"❌ Произошла ошибка запроса (Сеть/HTTP) при зачислении: {e}")
            return False

    def core_course_get_courses(self):
        FUNCTION_NAME = "core_course_get_courses"
        url_with_params = self.__get_url_with_params(FUNCTION_NAME)

        try:
            response = requests.post(url_with_params)
            response.raise_for_status()
            data = response.json()

            if data and isinstance(data, list):
                return data
            elif isinstance(data, dict) and 'exception' in data:
                log.error(f"❌ Ошибка Moodle API: {data.get('errorcode')}")
            else:
                log.error(f"⚠️ Неожиданный формат ответа: {data}")

        except requests.exceptions.RequestException as err:
            log.error(f"❌ Произошла ошибка: {err}")
        return []

    # --- ОСНОВНАЯ ЛОГИКА ---
    def process_user_and_enrollment(self, contact: Contact):
        '''
        1. Поиск пользователя по email.
        2. Если найден - обновляет пароль.
           Если не найден - создает пользователя.
        3. Зачисляет пользователя на указанный курс.
        '''
        course_shortname = contact.course_small
        log.info(f"--- Запуск процесса для пользователя: {contact.email} и курса: {course_shortname} ---")

        # 1. Поиск ID курса
        course_map = self._get_id_shortname_course()
        course_id = course_map.get(course_shortname)

        if not course_id:
            log.error(f"❌ Курс с коротким именем '{course_shortname}' не найден. Процесс остановлен.")
            return False

        # 2. Проверка существования пользователя (возвращает dict или {})
        user_data = self.core_user_get_users_by_field(contact.email, field='email')
        user_id = None

        if user_data:
            # 2.1. Если он есть, то Обнови пароль
            user_id = user_data.get('id')
            log.info(f"✅ Пользователь {contact.email} найден (ID: {user_id}).")

            update_success = self.core_user_update_password(user_id, contact.password)
            if update_success:
                log.info("✅ Пароль успешно обновлен.")
            else:
                log.error("❌ Не удалось обновить пароль.")

        else:
            # 2.2. Если его нет, то он создаётся.
            log.info(f"⚠️ Пользователь {contact.email} не найден. Создание нового пользователя...")
            user_id = self.core_user_create_users(contact)

            if not user_id:
                log.error(f"❌ Не удалось создать пользователя {contact.email}. Процесс остановлен.")
                return False

        # 3. Назначь ему курс (Зачисление)
        if user_id:
            log.info(f"Начало зачисления пользователя (ID: {user_id}) на курс '{course_shortname}' (ID: {course_id}).")
            enrollment_successful = self.enrol_manual_enrol_users(
                COURSE_ID=course_id,
                USER_ID_TO_ENROL=user_id
            )
            return enrollment_successful

        return False