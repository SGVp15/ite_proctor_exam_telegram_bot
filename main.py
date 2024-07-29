import asyncio

from Telegram.main import start_bot
from Utils.log import log


#  git pull https://github.com/SGVp15/proctor_exam_telegram_bot

async def main():
    tasks = [
        start_bot(),
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    log.warning('Exam_Registration_bot start')
    asyncio.run(main())
    # git pull https://github.com/SGVp15/proctor_exam_telegram_bot | python main.py
