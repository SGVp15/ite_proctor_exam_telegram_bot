from aiogram import types
from aiogram.dispatcher import FSMContext

from Config.config import ADMIN_ID, USERS_ID
from Telegram.keybords import inline
from loader import dp


@dp.message_handler(commands=['start', 'help'], user_id=[*ADMIN_ID, ])
async def send_welcome_admin(message: types.Message, state: FSMContext):
    text = f'Здравствуйте , {message.from_user.first_name}! \n'
    text += f'Этот бот работает с ProctorEDU.'
    text += f'\n ❓/id - узнать ваш id'
    await message.answer(text=text, reply_markup=inline.inline_kb_main)


@dp.message_handler(commands=['start', 'help'], user_id=[*USERS_ID, ], state=['*', None])
async def send_welcome_new_user(message: types.Message):
    text = f'Здравствуйте, {message.from_user.first_name}.'
    text += f'\n ❓/id - узнать ваш id'
    await message.answer(text=text, reply_markup=inline.inline_kb_main)


@dp.message_handler(commands=['start', 'help'], state=['*', None])
async def send_welcome(message: types.Message):
    text = f'Здравствуйте, {message.from_user.first_name}.'
    text += f'\n ❓/id - узнать ваш id'
    await message.answer(text=text, reply_markup=inline.inline_kb_main)


@dp.message_handler(commands='id')
async def send_id(message: types.Message):
    await message.answer(message.chat.id)
