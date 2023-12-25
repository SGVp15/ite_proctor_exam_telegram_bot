from unittest import TestCase

# from Config.config import user_id_email
# from Contact import parser

from Email import EmailSending


# from My_jinja import MyJinja


class TestEmailSending(TestCase):
    @staticmethod
    def test_send_email():
        s = '''Курс: «Проверка отправки почты
        OPS-online
        Даты проведения курса:	99.99.2000 - 80.90.2003 5 занятий с 10:00 до 14:00 мск (25 ак.ч. с тренером +7 ак.ч. на самост.вып.ДЗ)
        Тренер:	Сапегин Степан Борисович
        Место проведения:	Webinar_1
        Идентификатор конференции:	+
        Код доступа:
        Ссылка для регистрации:	https://events.webinar.ru/event/999146969/1581189808/edit
        №	ФИО		Организация		Должность		e-mail
        1	Григорьева Сабина 					asdasdqdq@stadasdep.rasdasdu	'''

        EmailSending(to='g.savushkin@itexpert.ru', text='text', html='html').send_email()
