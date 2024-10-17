import asyncio

from Telegram.main import start_bot
from Utils.git_update import git_update
from Utils.log import log


#  git pull https://github.com/SGVp15/proctor_exam_telegram_bot

async def main():
    tasks = [
        git_update(),
        start_bot(),
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    try:
        log.info('Exam_Registration_bot START')
        asyncio.run(main())
    finally:
        log.error('Exam_Registration_bot STOP')
# git pull https://github.com/SGVp15/proctor_exam_telegram_bot | python main.py
