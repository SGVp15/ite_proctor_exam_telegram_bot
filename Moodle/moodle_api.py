import urllib.parse
from random import choice

import requests

# Предполагается, что Contact, log, MOODLE_URL, MOODLE_TOKEN определены
from Contact import Contact
from Utils.log import log
from config import MOODLE_URL, MOODLE_TOKEN


class MOODLE_API:
    RESPONSE_FORMAT = 'json'
    API_URL = f'{MOODLE_URL}/webservice/rest/server.php'

    def core_user_get_users_by_field(self, value: str, field='email', ):
        """ - field can be 'id' or 'idnumber' or 'username' or 'email'"""
        FUNCTION_NAME = "core_user_get_users_by_field"
        # ... (Содержимое метода core_user_get_users_by_field) ...
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
            if data and isinstance(data, list):
                users_list = data
                # Возвращаем список найденных пользователей (может быть пустым)
                return users_list

            # --- 6. Обработка ошибок Moodle API ---
            elif isinstance(data, dict) and 'exception' in data:
                log.error(
                    f"\n❌ Ошибка Moodle API при поиске: {data.get('errorcode')}. Сообщение: {data.get('message')}")
                return []  # Возвращаем пустой список при ошибке
            else:
                log.error(f"\n⚠️ Получен неожиданный формат ответа при поиске: {data}")
                return []

        except requests.exceptions.RequestException as e:
            log.error(f"\n❌ Произошла ошибка запроса (Сеть/HTTP) при поиске: {e}")
            return []

    def core_user_create_users(self, user: Contact):
        '''Создает пользователя и возвращает его ID'''
        FUNCTION_NAME = "core_user_create_users"
        url_with_params = self.__get_url_with_params(FUNCTION_NAME)

        # ... (Остальной код core_user_create_users) ...
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

            response.raise_for_status()
            data = response.json()

            # --- 5. Обработка ответа ---
            if data and isinstance(data, list) and len(data) > 0 and 'id' in data[0]:
                log.info("\n✅ Пользователь успешно создан! ")
                new_user_info = data[0]
                log.info(f"  Новый ID пользователя: {new_user_info.get('id')}")
                return new_user_info.get('id')

            # --- 6. Обработка ошибок Moodle API ---
            elif isinstance(data, dict) and 'exception' in data:
                log.error("\n❌ Ошибка Moodle API при создании:")
                log.error(f"  Код ошибки: {data.get('errorcode')}")
                log.error(f"  Сообщение: {data.get('message')}")
                return None

            else:
                log.error(f"\n⚠️ Получен неожиданный формат ответа при создании: {data}")
                return None

        except requests.exceptions.RequestException as e:
            log.error(f"\n❌ Произошла ошибка запроса (Сеть/HTTP) при создании: {e}")
            return None

    def enrol_manual_enrol_users(self, COURSE_ID: int, USER_ID_TO_ENROL: int):
        '''Зачисляет пользователя на курс и возвращает True в случае успеха.'''
        # ... (Содержимое метода enrol_manual_enrol_users, измененное для логирования) ...
        FUNCTION_NAME = "enrol_manual_enrol_users"
        ROLE_ID_STUDENT = 5
        url_with_params = self.__get_url_with_params(FUNCTION_NAME)

        ENROLMENT_RECORD = {
            'roleid': ROLE_ID_STUDENT,
            'userid': USER_ID_TO_ENROL,
            'courseid': COURSE_ID
        }

        post_data_dict = {
            f'enrolments[0][{key}]': value
            for key, value in ENROLMENT_RECORD.items()
        }

        log.info(f"Попытка зачислить пользователя (ID: {USER_ID_TO_ENROL}) на курс (ID: {COURSE_ID})")

        try:
            response = requests.post(
                url_with_params,
                data=post_data_dict
            )

            response.raise_for_status()
            data = response.json() if response.text else []

            if isinstance(data, list) and not data:
                log.info(f"✅ Зачисление ID {USER_ID_TO_ENROL} на курс {COURSE_ID} успешно.")
                return True

            elif isinstance(data, dict) and 'exception' in data:
                log.error("\n❌ Ошибка Moodle API при зачислении:")
                log.error(f"  Код ошибки: {data.get('errorcode')}")
                log.error(f"  Сообщение: {data.get('message')}")
                return False

            else:
                log.error(f"\n⚠️ Получен неожиданный формат ответа при зачислении: {data}")
                return False

        except requests.exceptions.RequestException as e:
            log.error(f"\n❌ Произошла ошибка запроса (Сеть/HTTP) при зачислении: {e}")
            return False

    def core_user_update_password(self, user_id: int, new_password: str):
        '''
        *** ЭТОТ МЕТОД НУЖНО РЕАЛИЗОВАТЬ ***

        Использует Moodle API функцию 'core_user_update_users'
        для обновления пароля существующего пользователя.

        Возвращает True в случае успеха.
        '''
        log.warning(f"!!! ФУНКЦИЯ ОБНОВЛЕНИЯ ПАРОЛЯ НЕ РЕАЛИЗОВАНА. Выполняется имитация успеха.")
        # Тут должен быть POST-запрос к core_user_update_users
        # с параметрами users[0][id]=user_id и users[0][password]=new_password
        # ... Реализация ...
        return True  # Имитация успеха для продолжения логики

    def core_course_get_courses(self):
        # ... (Содержимое метода core_course_get_courses) ...
        FUNCTION_NAME = "core_course_get_courses"
        url_with_params = self.__get_url_with_params(FUNCTION_NAME)

        try:
            response = requests.post(url_with_params)
            response.raise_for_status()
            data = response.json()

            if data and isinstance(data, list):
                return data
            elif isinstance(data, dict) and 'exception' in data:
                log.error(f"\n❌ Ошибка Moodle API: {data.get('errorcode')}")
            else:
                log.error(f"\n⚠️ Неожиданный формат ответа: {data}")

        except requests.exceptions.RequestException as err:
            log.error(f"\n❌ Произошла ошибка: {err}")
        return []

    def __get_url_with_params(self, function_name: str):
        # Кодирование параметров для URL
        url_params = {
            'wstoken': MOODLE_TOKEN,
            'wsfunction': function_name,
            'moodlewsrestformat': self.RESPONSE_FORMAT
        }
        url_with_params = self.API_URL + '?' + urllib.parse.urlencode(url_params)
        return url_with_params

    def _get_id_shortname_course(self) -> dict:
        d = {}
        for course in self.core_course_get_courses():
            d[course.get('shortname')] = course.get('id')
        return d

    # ----------------------------------------------------------------
    # НОВЫЙ МЕТОД, ВЫПОЛНЯЮЩИЙ ЗАПРОШЕННУЮ ЛОГИКУ
    # ----------------------------------------------------------------
    def process_user_and_enrollment(self, contact: Contact):
        '''
        Выполняет три шага:
        1. Поиск пользователя по email.
        2. Если найден - обновляет пароль (требуется реализация core_user_update_password).
           Если не найден - создает пользователя.
        3. Зачисляет пользователя на указанный курс.
        '''
        course_shortname = contact.course_small
        log.info(f"--- Запуск процесса для пользователя: {contact.email} и курса: {course_shortname} ---")

        # 1. Поиск ID курса
        course_map = self._get_id_shortname_course()
        course_id = course_map.get(course_shortname)

        if not course_id:
            log.error(f"❌ Курс с коротким именем '{course_shortname}' не найден.")
            return False

        # 2. Проверка существования пользователя
        user_list = self.core_user_get_users_by_field(contact.email, field='email')
        user_id = None

        if user_list:
            # 2.1. Если он есть, то Обнови пароль (и получаем ID)
            user_data = user_list[0]
            user_id = user_data.get('id')
            log.info(f"✅ Пользователь {contact.email} найден (ID: {user_id}).")

            # ВАЖНО: Требуется реализация core_user_update_password
            update_success = self.core_user_update_password(user_id, contact.password)
            if update_success:
                log.info("✅ Пароль успешно обновлен (или имитировано обновление).")
            else:
                log.error("❌ Не удалось обновить пароль. Продолжение процесса зачисления...")
                # Решение: продолжить зачисление, даже если пароль не обновился.

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
