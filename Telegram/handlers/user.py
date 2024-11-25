import os.path

from aiogram import types, F

from Ispring.ispring2 import get_session_in_enrollments_users_contents, IspringApi
from Telegram.Call_Back_Data import CallBackData
from config import USERS_ID, ADMIN_ID, PATH_DOWNLOAD_FILE
from Telegram.keybords.inline import inline_kb_main, del_enrollment
from Telegram.main import bot, dp, loop
from Utils.log import log
from main_registration import registration
from parser import get_contact_from_excel


@dp.message(F.document & F.from_user.id.in_({*ADMIN_ID, *USERS_ID}))
async def download_document_handle(message: types.Message):
    # Get the file ID from the document object
    file_id = message.document.file_id
    # Download the file
    file = await bot.get_file(file_id)
    file_path = file.file_path
    path = os.path.join(PATH_DOWNLOAD_FILE, file_path)

    # Read the contents of the file
    await bot.download_file(file_path, destination=path)
    await message.answer('Добавил файл', reply_markup=inline_kb_main)

    contacts = get_contact_from_excel(path)
    if not contacts:
        text_answer = 'No contact'
        await message.answer(text_answer, reply_markup=inline_kb_main)
    else:
        text_answer = await registration(contacts)
        await message.answer(text_answer, reply_markup=inline_kb_main)
        loop.create_task(registration(contacts))


@dp.callback_query(F.data.in_({CallBackData.EDIT_REGISTRATION}) & F.from_user.id.in_({*ADMIN_ID, *USERS_ID}))
async def show_registration(callback_query: types.callback_query):
    sessions = get_session_in_enrollments_users_contents()
    sessions = sorted(sessions)
    for session in sessions:
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=f'{session}',
            reply_markup=del_enrollment(session.enrollment_id),
        )

    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=f'End',
        reply_markup=inline_kb_main
    )


@dp.callback_query(F.data.in_({CallBackData.SHOW_REGISTRATION}) & F.from_user.id.in_({*ADMIN_ID, *USERS_ID}))
async def show_registration(callback_query: types.callback_query):
    sessions = get_session_in_enrollments_users_contents()
    sessions = sorted(sessions)
    text = ''
    for session in sessions:
        text += f'{session}\n'
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=text,
        reply_markup=inline_kb_main
    )


@dp.callback_query(
    F.data.regexp(f'{CallBackData.DEL_REGISTRATION}' + r'.*')
    & F.from_user.id.in_({*ADMIN_ID, *USERS_ID}))
async def del_registration(callback_query: types.callback_query):
    delete_id = callback_query.data.replace(CallBackData.DEL_REGISTRATION, '')
    log.info(f'{delete_id=}')
    if IspringApi().delete_enrollment(delete_id):
        text = 'Сессия удалена'
    else:
        text = 'Не получилось удалить сессию'
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=text,
        reply_markup=inline_kb_main
    )


@dp.message(F.text.regexp(r'{.*}') &
            F.from_user.id.in_({*ADMIN_ID, *USERS_ID}))
async def get_json(message: types.Message):
    await message.answer('Получил JSON', reply_markup=inline_kb_main)
    # answer = await registration()
    # await message.answer(answer, reply_markup=inline_kb_main)
    # loop.create_task(registration())
