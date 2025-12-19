from aiogram import types

from Telegram.main import dp


@dp.message()
async def echo(message: types.Message):
    await message.reply('Не понимаю, что это значит.'
                        'Воспользуйтесь командой /help')
