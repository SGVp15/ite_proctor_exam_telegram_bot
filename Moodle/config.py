from dotenv import dotenv_values, find_dotenv

config = dotenv_values(find_dotenv())

MOODLE_TOKEN = config.get('MOODLE_TOKEN')
MOODLE_URL = config.get('MOODLE_URL')


if not MOODLE_TOKEN or not MOODLE_URL:
    raise (f'ERROR .ENV '
           f'{MOODLE_TOKEN=}'
           f'{MOODLE_URL=}')