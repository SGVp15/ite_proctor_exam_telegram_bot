import asyncio

from Telegram.main import start_bot

if __name__ == '__main__':
    print('Exam_Registration_bot start')
    # loop.create_task(registration())
    asyncio.run(start_bot())
