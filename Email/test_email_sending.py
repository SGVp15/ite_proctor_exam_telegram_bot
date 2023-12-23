# from unittest import TestCase
#
# from Config.config import user_id_email
# from Contact import parser
# from Email.email_sending import EmailSending
# from My_jinja.my_jinja import MyJinja
#
#
# class TestEmailSending(TestCase):
#     @staticmethod
#     def test_send_email(callback_query_from_user_id):
#         s = '''Курс: «Проверка отправки почты
#         OPS-online
#         Даты проведения курса:	99.99.2000 - 80.90.2003 5 занятий с 10:00 до 14:00 мск (25 ак.ч. с тренером +7 ак.ч. на самост.вып.ДЗ)
#         Тренер:	Сапегин Степан Борисович
#         Место проведения:	Webinar_1
#         Идентификатор конференции:	+
#         Код доступа:
#         Ссылка для регистрации:	https://events.webinar.ru/event/999146969/1581189808/edit
#         №	ФИО		Организация		Должность		e-mail
#         1	Григорьева Сабина 					asdasdqdq@stadasdep.rasdasdu	'''
#         user = parser.get_list_users_from_string(s)[0]
#         user.manager_email = user_id_email.get(str(callback_query_from_user_id), '')
#
#         template_html = MyJinja()
#         html = template_html.render_document(user)
#
#         template_text = MyJinja(template_file='course_registration.txt')
#         text = template_text.render_document(user)
#
#         return EmailSending(subject=user.webinar_name, to=user.manager_email, text=text, html=html,
#                             manager=user.manager_email,
#                             files_path=['./Email/template_email/course_registration.html',
#                                         './Email/template_email/course_registration.txt']).send_email()
