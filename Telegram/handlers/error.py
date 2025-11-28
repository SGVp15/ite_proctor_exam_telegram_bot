from aiogram import types

from root_config import LOG_FILE
from Telegram.main import dp


@dp.message()
async def echo(message: types.Message):
    await message.reply('Не понимаю, что это значит.'
                        'Воспользуйтесь командой /help')
    # with open(LOG_FILE, encoding='utf-8', mode='a') as f:
    #     for k, v in message:
    #         f.write(f'{k} {v}', )
    #     f.write('\n')
