from aiogram import types

from Config.config import USERS_ID, ADMIN_ID
from keybords.inline import inline_kb_main
from loader import dp, bot, loop
from main_registration import registration


@dp.message_handler(commands='id')
async def send_id(message: types.Message):
    await message.answer(message.chat.id)


@dp.message_handler(content_types=types.ContentType.DOCUMENT, user_id=[*ADMIN_ID, *USERS_ID])
async def handle_document(message: types.Message):
    # Get the file ID from the document object
    file_id = message.document.file_id

    # Download the file
    file = await bot.get_file(file_id)
    file_path = file.file_path

    # Read the contents of the file
    await bot.download_file(file_path, destination_dir='./data/input')
    path = f'./data/input/{file_path}'
    await message.answer(f'Добавил {file_path}', reply_markup=inline_kb_main)
    # asyncio.run(registration(path))
    loop.create_task(registration(path))
