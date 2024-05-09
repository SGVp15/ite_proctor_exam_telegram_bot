from aiogram import types, F

from Ispring.ispring2 import get_str_enrollments_users_contents
from Telegram.Call_Back_Data import CallBackData
from Telegram.config import USERS_ID, ADMIN_ID
from Telegram.keybords.inline import inline_kb_main
from Telegram.main import bot, dp, loop
from main_registration import registration


@dp.message(F.document & F.from_user.id.in_({*ADMIN_ID, *USERS_ID}))
async def download_document_handle(message: types.Message):
    # Get the file ID from the document object
    file_id = message.document.file_id
    # Download the file
    file = await bot.get_file(file_id)
    file_path = file.file_path
    path = f'./data/input/{file_path}'

    # Read the contents of the file
    await bot.download_file(file_path, destination=f'./data/input/{file_path}')
    await message.answer('Добавил файл', reply_markup=inline_kb_main)

    answer = await registration(path)
    await message.answer(answer, reply_markup=inline_kb_main)
    loop.create_task(registration(path))


@dp.callback_query(F.data.in_({CallBackData.show_registration}) & F.from_user.id.in_({*ADMIN_ID, *USERS_ID}))
async def show_registration(callback_query: types.callback_query):
    sessions = get_str_enrollments_users_contents()
    for session in sessions:
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=f'{session}',
            reply_markup=inline_kb_main
        )

    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=f'End',
        reply_markup=inline_kb_main
    )


@dp.callback_query(F.data.in_({CallBackData.del_registration}) & F.from_user.id.in_({*ADMIN_ID, *USERS_ID}))
async def del_registration(callback_query: types.callback_query):
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=f'del_registration',
        reply_markup=inline_kb_main
    )
