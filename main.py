import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from Config import config

bot = Bot(token=config.BOT_TOKEN)
# , parse_mode=types.ParseMode.HTML)

loop = asyncio.get_event_loop()
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def start_bot():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    print('Exam_Registration_bot start')
    # loop.create_task(registration())
    asyncio.run(start_bot())
