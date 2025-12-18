from pathlib import Path

from dotenv import dotenv_values, find_dotenv

config = dotenv_values(find_dotenv())

LOGIN_MOODLE = config.get('LOGIN_MOODLE')
PASSWORD_MOODLE = config.get('PASSWORD_MOODLE')
MOODLE_TOKEN = config.get('MOODLE_TOKEN')
MOODLE_URL = config.get('MOODLE_URL')

DIR_HTML_DOWNLOAD = Path('./data/html_downloads')
DIR_HTML_DOWNLOAD.mkdir(exist_ok=True, parents=True)

if not LOGIN_MOODLE:
    raise f'ERROR .ENV {MOODLE_TOKEN=}'
if not PASSWORD_MOODLE:
    raise f'ERROR .ENV {MOODLE_URL=}'
if not MOODLE_TOKEN:
    raise f'ERROR .ENV {MOODLE_TOKEN=}'
if not MOODLE_URL:
    raise f'ERROR .ENV {MOODLE_URL=}'
