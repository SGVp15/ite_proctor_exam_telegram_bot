from aiogram import types

from Config.config import USERS_ID, ADMIN_ID, QUEUE, LOG_FILE, TEMPLATE_FILE_XLSX
from keybords.inline import inline_kb_main
from loader import dp, bot
from Call_Back_Data import CallBackData as call_back


def is_empty_file(file) -> bool:
    with open(file=file, mode="r", encoding='utf-8') as f:
        s = f.read()
    return len(s) <= 10


@dp.message_handler(commands='id')
async def send_id(message: types.Message):
    await message.answer(message.chat.id)


@dp.callback_query_handler(
    lambda c: c.data in [call_back.get_log, call_back.get_log_program, call_back.get_template_file_xlsx],
    user_id=[*ADMIN_ID, *USERS_ID])
async def get_file(callback_query: types.callback_query):
    query = callback_query.data
    file = LOG_FILE
    if query == call_back.get_log_program:
        file = TEMPLATE_FILE_XLSX
    elif query == call_back.get_log:
        file = LOG_FILE
    elif query == call_back.get_template_file_xlsx:
        file = TEMPLATE_FILE_XLSX

    try:
        if is_empty_file(file):
            await bot.send_message(chat_id=callback_query.from_user.id, text=f'✅ Файл {file} пустой',
                                   reply_markup=inline_kb_main)
    except UnicodeDecodeError:
        ...
    with open(file, "rb") as f:
        await bot.send_document(chat_id=callback_query.from_user.id, document=f, reply_markup=inline_kb_main)
