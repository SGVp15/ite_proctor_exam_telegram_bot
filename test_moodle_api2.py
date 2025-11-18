import unittest
from unittest.mock import patch, MagicMock
from MOODLE_API import MOODLE_API  # Предполагаем, что класс MOODLE_API находится в MOODLE_API.py


# --- 1. МОК-КЛАСС Contact ---
# Создаем простой мок-класс Contact, чтобы имитировать данные пользователя
class MockContact:
    def __init__(self, email, username, password, course_small):
        self.email = email
        self.username = username
        self.password = password
        self.course_small = course_small
        self.first_name_rus = "Тест"
        self.last_name_eng = "User"


# ----------------------------------------------------------------------------------

class TestMoodleAPIEnrollment(unittest.TestCase):

    def setUp(self):
        # Инициализация тестируемого класса перед каждым тестом
        self.api = MOODLE_API()

        # Общие тестовые данные
        self.test_user_new = MockContact(
            email="new_test@example.com",
            username="newuser",
            password="Password123",
            course_small="BAFC"
        )
        self.test_user_existing = MockContact(
            email="existing_test@example.com",
            username="olduser",
            password="NewPassword456",
            course_small="BASRMC"  # Для BASRMC есть только BASRMC_0
        )

        # Словарь курсов, который будет мокать _get_id_shortname_course
        self.mock_course_map = {
            'BAFC_0': 11,
            'BAFC_1': 12,
            'BAFC_2': 13,
            'BASRMC_0': 18,
            'UNKNOWN_99': 99
        }

    # ----------------------------------------------------------------------
    #                          СЦЕНАРИЙ 1: СОЗДАНИЕ НОВОГО ПОЛЬЗОВАТЕЛЯ
    # ----------------------------------------------------------------------
    @patch.object(MOODLE_API, '_get_id_shortname_course')
    @patch.object(MOODLE_API, 'enrol_manual_enrol_users')
    @patch.object(MOODLE_API, 'core_user_create_users')
    @patch.object(MOODLE_API, 'core_user_get_users_by_field')
    @patch('random.choice')
    def test_process_user_new_creation_success(self, mock_choice, mock_get_user, mock_create_user, mock_enroll,
                                               mock_get_courses):
        """Проверяет сценарий: пользователь не найден -> создается -> зачисляется."""

        # 1. МОК-НАСТРОЙКИ

        # Мокаем выбор курса: всегда выбираем BAFC_1
        mock_get_courses.return_value = self.mock_course_map
        mock_choice.return_value = 'BAFC_1'

        # Мокаем поиск пользователя: пользователь НЕ найден
        mock_get_user.return_value = {}

        # Мокаем создание пользователя: возвращаем новый ID
        NEW_USER_ID = 200
        mock_create_user.return_value = NEW_USER_ID

        # Мокаем зачисление: успешно
        mock_enroll.return_value = True

        # 2. ВЫПОЛНЕНИЕ ТЕСТА
        result = self.api.process_user_and_enrollment(self.test_user_new)

        # 3. ПРОВЕРКИ

        # Проверяем, что поиск был вызван
        mock_get_user.assert_called_once_with(self.test_user_new.email, field='email')

        # Проверяем, что была вызвана функция создания (так как пользователь не найден)
        mock_create_user.assert_called_once_with(self.test_user_new)

        # Проверяем, что функция обновления пароля НЕ вызывалась
        self.assertFalse(self.api.core_user_update_password.called)

        # Проверяем, что зачисление было вызвано с правильным ID курса (12) и пользователя (200)
        mock_enroll.assert_called_once_with(
            COURSE_ID=12,  # BAFC_1 (ID 12)
            USER_ID_TO_ENROL=NEW_USER_ID
        )

        # Проверяем, что процесс завершился успехом
        self.assertTrue(result)

    # ----------------------------------------------------------------------
    #                          СЦЕНАРИЙ 2: ОБНОВЛЕНИЕ СУЩЕСТВУЮЩЕГО ПОЛЬЗОВАТЕЛЯ
    # ----------------------------------------------------------------------
    @patch.object(MOODLE_API, '_get_id_shortname_course')
    @patch.object(MOODLE_API, 'enrol_manual_enrol_users')
    @patch.object(MOODLE_API, 'core_user_update_password')
    @patch.object(MOODLE_API, 'core_user_get_users_by_field')
    @patch('random.choice')
    def test_process_user_existing_update_success(self, mock_choice, mock_get_user, mock_update_password, mock_enroll,
                                                  mock_get_courses):
        """Проверяет сценарий: пользователь найден -> обновляется пароль -> зачисляется."""

        # 1. МОК-НАСТРОЙКИ

        EXISTING_USER_ID = 101

        # Мокаем выбор курса: для BASRMC должен быть выбран BASRMC_0
        mock_get_courses.return_value = self.mock_course_map
        mock_choice.return_value = 'BASRMC_0'

        # Мокаем поиск пользователя: пользователь найден
        mock_get_user.return_value = {'id': EXISTING_USER_ID, 'username': 'olduser'}

        # Мокаем обновление пароля: успешно
        mock_update_password.return_value = True

        # Мокаем зачисление: успешно
        mock_enroll.return_value = True

        # 2. ВЫПОЛНЕНИЕ ТЕСТА
        result = self.api.process_user_and_enrollment(self.test_user_existing)

        # 3. ПРОВЕРКИ

        # Проверяем, что поиск был вызван
        mock_get_user.assert_called_once()

        # Проверяем, что функция обновления пароля была вызвана
        mock_update_password.assert_called_once_with(
            EXISTING_USER_ID,
            self.test_user_existing.password
        )

        # Проверяем, что функция создания пользователя НЕ вызывалась
        self.assertFalse(self.api.core_user_create_users.called)

        # Проверяем, что зачисление было вызвано с правильным ID курса (18) и пользователя (101)
        mock_enroll.assert_called_once_with(
            COURSE_ID=18,  # BASRMC_0 (ID 18)
            USER_ID_TO_ENROL=EXISTING_USER_ID
        )

        # Проверяем, что процесс завершился успехом
        self.assertTrue(result)

    # ----------------------------------------------------------------------
    #                          СЦЕНАРИЙ 3: ОШИБКА ПОИСКА КУРСА
    # ----------------------------------------------------------------------
    @patch.object(MOODLE_API, '_get_id_shortname_course')
    def test_process_course_not_found_failure(self, mock_get_courses):
        """Проверяет сценарий: курс не найден."""

        # 1. МОК-НАСТРОЙКИ

        # Мокаем курсы, чтобы они не содержали "DNE" (Do Not Exist)
        mock_get_courses.return_value = self.mock_course_map

        # Создаем контакт, который запросит несуществующий курс
        user_fail = MockContact(email="a@a.com", username="a", password="a", course_small="DNE")

        # 2. ВЫПОЛНЕНИЕ ТЕСТА
        result = self.api.process_user_and_enrollment(user_fail)

        # 3. ПРОВЕРКИ

        # Проверяем, что функции работы с пользователем НЕ вызывались
        self.assertFalse(self.api.core_user_get_users_by_field.called)
        self.assertFalse(self.api.core_user_create_users.called)
        self.assertFalse(self.api.enrol_manual_enrol_users.called)

        # Проверяем, что процесс завершился неудачей
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()