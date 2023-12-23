import smtplib
from email.message import EmailMessage

from jinja2 import Environment, FileSystemLoader

from Config.config import EMAIL_BСС, EMAIL_BСС_course

environment = Environment(auto_reload=True, loader=FileSystemLoader('./data/templates_email'))
email_registration_exam_online = environment.get_template('email_registration_exam_online.txt')
email_registration_exam_offline = environment.get_template('email_registration_exam_offline.txt')
email_exam_success = environment.get_template('email_exam_success.txt')
email_registration_course = environment.get_template('email_registration_course.txt')
