from dotenv import dotenv_values, find_dotenv

config = dotenv_values(find_dotenv())

MOODLE_TOKEN = config.get('MOODLE_TOKEN')
MOODLE_URL = config.get('MOODLE_URL')
