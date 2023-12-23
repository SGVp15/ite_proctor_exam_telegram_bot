# import menus
# import utils
import Telegram
from aiogram.utils import executor

from loader import dp

if __name__ == '__main__':
    print('Exam_Registration_bot start')
    # loop.create_task(registration())
    executor.start_polling(dp)
