from Contact import Contact
from config import MOODLE_URL, MOODLE_TOKEN
import urllib.parse
import requests


class MOODLE_API:
    def create_user(self, user: Contact):
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
        # Настройки запроса
        FUNCTION_NAME = "core_user_create_users"  # <-- ИЗМЕНЕНИЕ: функция для создания пользователя
        RESPONSE_FORMAT = "json"

        # --- 2. Формирование URL с мета-параметрами ---
        API_URL = f"{MOODLE_URL}/webservice/rest/server.php"

        # Мета-параметры (токен, функция, формат) передаются в URL-строке
        url_params = {
            'wstoken': MOODLE_TOKEN,
            'wsfunction': FUNCTION_NAME,
            'moodlewsrestformat': RESPONSE_FORMAT
        }

        # Кодирование параметров для URL
        url_with_params = API_URL + '?' + urllib.parse.urlencode(url_params)

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

        print(f"Отправка POST запроса к: {url_with_params}")
        print(f"Попытка создать пользователя: {NEW_USER_DATA['username']}")

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
                print("\n✅ Пользователь успешно создан!")
                new_user_info = data[0]
                return new_user_info.get('id')
                # print(f"  Новый ID пользователя: {new_user_info.get('id')}")
                # print(f"  Имя: {NEW_USER_DATA['firstname']} {NEW_USER_DATA['lastname']}")
                # print(f"  Username: {NEW_USER_DATA['username']}")

            # --- 6. Обработка ошибок Moodle API ---
            elif isinstance(data, dict) and 'exception' in data:
                print("\n❌ Ошибка Moodle API:")
                print(f"  Код ошибки: {data.get('errorcode')}")
                print(f"  Сообщение: {data.get('message')}")
                print("\nПолный ответ Moodle (для отладки):")
                print(data)

            else:
                # Обработка неожиданных ответов
                print(f"\n⚠️ Получен неожиданный формат ответа.")
                print(data)

        except requests.exceptions.RequestException as e:
            # Обработка сетевых ошибок
            print(f"\n❌ Произошла ошибка запроса (Сеть/HTTP): {e}")
