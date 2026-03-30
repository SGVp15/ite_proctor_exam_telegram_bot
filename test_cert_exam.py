import unittest
import datetime
from unittest.mock import patch


# Класс-заглушка для теста
class User:
    def __init__(self, date_exam, can_create_cert):
        self.date_exam = date_exam
        self.can_create_cert = can_create_cert


def check_access(u):
    # Ваше условие
    if (datetime.datetime.now() >= u.date_exam + datetime.timedelta(days=2)
            or u.can_create_cert in (1, '1')):
        return True
    return False


class TestAccessCondition(unittest.TestCase):
    def setUp(self):
        # Фиксируем "текущее" время для тестов
        self.now = datetime.datetime(2024, 5, 10, 12, 0, 0)

    @patch('datetime.datetime')
    def test_logic(self, mock_datetime):
        mock_datetime.now.return_value = self.now
        # Позволяем mock-объекту создавать реальные datetime при вызове конструктора
        mock_datetime.side_effect = lambda *args, **kw: datetime.datetime(*args, **kw)

        # --- КЕЙС 1: Доступ по дате (can_create_cert = 0) ---

        # Прошло ровно 2 дня (True)
        u1 = User(self.now - datetime.timedelta(days=2), 0)
        self.assertTrue(check_access(u1), "Должно быть True: прошло ровно 2 дня")

        # Прошло меньше 2 дней (False)
        u2 = User(self.now - datetime.timedelta(days=1), 0)
        self.assertFalse(check_access(u2), "Должно быть False: прошло меньше 2 дней")

        # --- КЕЙС 2: Доступ по флагу (Дата еще не наступила) ---

        # Флаг как число 1 (True)
        u3 = User(self.now + datetime.timedelta(days=1), 1)
        self.assertTrue(check_access(u3), "Должно быть True: флаг can_create_cert=1")

        # Флаг как строка '1' (True)
        u4 = User(self.now + datetime.timedelta(days=1), '1')
        self.assertTrue(check_access(u4), "Должно быть True: флаг can_create_cert='1'")

        # --- КЕЙС 3: Оба условия ложны (False) ---

        u5 = User(self.now + datetime.timedelta(days=1), 0)
        self.assertFalse(check_access(u5), "Должно быть False: дата не пришла и флага нет")

        # --- КЕЙС 4: Оба условия истинны (True) ---

        u6 = User(self.now - datetime.timedelta(days=1), 1)
        self.assertTrue(check_access(u6), "Должно быть True: и дата не прошла и флаг есть")


if __name__ == '__main__':
    unittest.main()