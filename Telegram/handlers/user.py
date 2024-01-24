from aiogram import types, F

from Config.config import USERS_ID, ADMIN_ID
from Telegram.keybords.inline import inline_kb_main
from main import dp, bot
from main_registration import registration
from aiogram.filters.command import Command


@dp.message(Command('id'))
async def send_id(message: types.Message):
    await message.answer(message.chat.id)


@dp.message(F.document & F.from_user.id.in_(user_id=[*ADMIN_ID, *USERS_ID]))
async def handle_document(message: types.Message):
    # Get the file ID from the document object
    file_id = message.document.file_id

    # Download the file
    file = await bot.get_file(file_id)
    file_path = file.file_path

    # Read the contents of the file
    await bot.download_file(file_path, destination_dir='./data/input')
    path = f'./data/input/{file_path}'
    await message.answer(f'Добавил {file_path}')
    answer = await registration(path)
    await message.answer(answer, reply_markup=inline_kb_main)
    # loop.create_task(registration(path))
