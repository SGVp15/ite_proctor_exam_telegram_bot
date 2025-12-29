from pathlib import Path

from dotenv import dotenv_values, find_dotenv

config = dotenv_values(find_dotenv())

ITEXPERT_API_SECRET_KEY = config.get('ITEXPERT_API_SECRET_KEY')
ITEXPERT_URL = config.get('ITEXPERT_URL')

if not ITEXPERT_API_SECRET_KEY:
    raise f'ERROR .ENV {ITEXPERT_API_SECRET_KEY=}'
if not ITEXPERT_URL:
    raise f'ERROR .ENV {ITEXPERT_URL=}'

BASE_PATH = Path('//192.168.20.100/Administrative server/РАБОТА АДМИНИСТРАТОРА/ОРГАНИЗАЦИЯ IT ЭКЗАМЕНОВ/ЭКЗАМЕНЫ ЦИФРОВОЙ ПУТЬ')
OUT_DIR_CERT = BASE_PATH / 'сертификаты'