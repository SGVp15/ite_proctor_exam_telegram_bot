import asyncio

from Telegram.main import start_bot


async def main():
    tasks = [
        start_bot(),
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    print('Exam_Registration_bot start')
    asyncio.run(main())
