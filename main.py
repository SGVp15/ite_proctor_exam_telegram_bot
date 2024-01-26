import asyncio

from Telegram.main import start_bot
#  git pull https://github.com/SGVp15/proctor_exam_telegram_bot

async def main():
    tasks = [
        start_bot(),
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    print('Exam_Registration_bot start')
    asyncio.run(main())
