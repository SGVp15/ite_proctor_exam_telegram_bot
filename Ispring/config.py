from dotenv import dotenv_values, find_dotenv

config = dotenv_values(find_dotenv())

LOGIN_ISPRING = config.get('LOGIN_ISPRING')
PASSWORD_ISPRING = config.get('PASSWORD_ISPRING')
DOMAIN_ISPRING = 'https://itexpert.ispringlearn.ru'
