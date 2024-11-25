import os

from aiogram import types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile

from config import USERS_ID, ADMIN_ID, LOG_FILE, TEMPLATE_FILE_XLSX, DOCUMENTS, SYSTEMLOG
from Telegram.keybords.inline import inline_kb_main
from Telegram.main import dp, bot
from Telegram.Call_Back_Data import CallBackData as call_back
from Utils.log import log


def is_empty_file(file) -> bool:
    if not os.path.exists(file):
        return True

    try:
        with open(file=file, mode="r", encoding='utf-8') as f:
            s = f.read()
            return len(s) <= 10
    except UnicodeDecodeError:
        log.error('UnicodeDecodeError')
    return False


@dp.message(Command('id'))
async def send_id(message: types.Message):
    await message.answer(str(message.chat.id))


@dp.callback_query(
    F.data.in_(
        {call_back.GET_LOG, call_back.GET_LOG_PROGRAM, call_back.GET_TEMPLATE_FILE_XLSX, call_back.GET_LAST_EXCEL_FILE})
    & F.from_user.id.in_({*ADMIN_ID, *USERS_ID})
)
async def get_file(callback_query: types.callback_query):
    query = callback_query.data

    if query == call_back.GET_LOG_PROGRAM:
        file = FSInputFile(SYSTEMLOG, 'systemlog.txt')
    elif query == call_back.GET_LOG:
        file = FSInputFile(LOG_FILE, 'log_file.txt')
    elif query == call_back.GET_TEMPLATE_FILE_XLSX:
        file = FSInputFile(TEMPLATE_FILE_XLSX, 'template_file.xlsx')
    elif query == call_back.GET_LAST_EXCEL_FILE:
        path = os.path.join(DOCUMENTS)
        files = os.listdir(path)
        paths = [os.path.join(path, basename) for basename in files]
        path = max(paths, key=os.path.getctime)
        file_name = os.path.basename(path)
        file = FSInputFile(path, file_name)

    try:
        if is_empty_file(file.path):
            await bot.answer_callback_query(chat_id=callback_query.from_user.id, text=f'✅ Файл пустой',
                                            reply_markup=inline_kb_main)
        else:
            await bot.send_document(chat_id=callback_query.from_user.id, document=file, reply_markup=inline_kb_main)
    except UnicodeDecodeError:
        log.error('UnicodeDecodeError')
