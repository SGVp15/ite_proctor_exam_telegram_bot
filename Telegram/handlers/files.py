import os

from aiogram import types, F
from aiogram.types import FSInputFile

from Telegram.Call_Back_Data import CallBackData
from Telegram.config import USERS_ID, ADMIN_ID, DOCUMENTS
from Telegram.keybords.inline import inline_kb_main, get_list_files_keyboard
from Telegram.main import dp, bot


def is_empty_file(file_path) -> bool:
    with open(file=file_path, mode="r", encoding='utf-8') as f:
        s = f.read()
    return len(s) <= 10


@dp.callback_query(
    F.data.startswith(CallBackData.file_download_) & F.from_user.id.in_({*ADMIN_ID, *USERS_ID})
)
async def download_file(callback_query: types.callback_query):
    query = callback_query.data
    file_name = str(query).replace(CallBackData.file_download_, '')
    path = os.path.join(DOCUMENTS, file_name)
    if os.path.exists(path):
        file = FSInputFile(path, file_name)
        await bot.send_document(chat_id=callback_query.from_user.id, document=file, reply_markup=inline_kb_main)
    else:
        await bot.send_message(chat_id=callback_query.from_user.id, text='Файла не существует',
                               reply_markup=get_list_files_keyboard())


@dp.callback_query(
    F.data.startswith(CallBackData.file_delete_) & F.from_user.id.in_({*ADMIN_ID, *USERS_ID})
)
async def delete_file(callback_query: types.callback_query):
    query = callback_query.data
    file_name = str(query).replace(CallBackData.file_delete_, '')
    path = os.path.join(DOCUMENTS, file_name)
    if os.path.exists(path):
        os.remove(path)
        await bot.send_message(chat_id=callback_query.from_user.id, text=f'Файл {file_name} удален',
                               reply_markup=get_list_files_keyboard())
    else:
        await bot.send_message(chat_id=callback_query.from_user.id, text=f'Файл {file_name} не существует',
                               reply_markup=get_list_files_keyboard())


@dp.callback_query(F.data.in_({CallBackData.show_list_file}) & F.from_user.id.in_({*ADMIN_ID, *USERS_ID}))
async def show_list_files(callback_query: types.callback_query):
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Список файлов',
        reply_markup=get_list_files_keyboard()
    )
