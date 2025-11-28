from dotenv import dotenv_values, find_dotenv

config = dotenv_values(find_dotenv())

ITEXPERT_API_SECRET_KEY = config.get('ITEXPERT_API_SECRET_KEY')
ITEXPERT_URL = config.get('ITEXPERT_URL')

if not ITEXPERT_API_SECRET_KEY:
    raise f'ERROR .ENV {ITEXPERT_API_SECRET_KEY=}'
if not ITEXPERT_URL:
    raise f'ERROR .ENV {ITEXPERT_URL=}'
