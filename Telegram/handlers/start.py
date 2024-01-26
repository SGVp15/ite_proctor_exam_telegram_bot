from aiogram import types, F
from aiogram.fsm.context import FSMContext

from aiogram.filters import Command

from Telegram.config import ADMIN_ID, USERS_ID
from Telegram.keybords import inline
from Telegram.main import dp


@dp.message(F.command.in_({'start', 'help'}) & F.from_user.id.in_({*ADMIN_ID}))
async def send_welcome_admin(message: types.Message, state: FSMContext):
    text = f'Здравствуйте , {message.from_user.first_name}! \n'
    text += f'Этот бот работает с ProctorEDU.'
    text += f'\n ❓/id - узнать ваш id'
    await message.answer(text=text, reply_markup=inline.inline_kb_main)


@dp.message(F.command.in_({'start', 'help'}) & F.from_user.id.in_({*USERS_ID}))
async def send_welcome_new_user(message: types.Message):
    text = f'Здравствуйте, {message.from_user.first_name}.'
    text += f'\n ❓/id - узнать ваш id'
    await message.answer(text=text, reply_markup=inline.inline_kb_main)


@dp.message(Command('start', 'help'))
async def send_welcome(message: types.Message):
    text = f'Здравствуйте, {message.from_user.first_name}.'
    text += f'\n ❓/id - узнать ваш id'
    await message.answer(text=text, reply_markup=inline.inline_kb_main)


@dp.message(Command('id'))
async def send_id(message: types.Message):
    await message.answer(str(message.chat.id))
