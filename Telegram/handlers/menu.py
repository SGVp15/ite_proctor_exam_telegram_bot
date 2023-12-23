from aiogram import types

from Config.config import ADMIN_ID
from Telegram.keybords.inline import inline_kb_admin, inline_kb_main
from loader import dp, bot


@dp.callback_query_handler(lambda c: c.data == 'admin_menu', user_id=[*ADMIN_ID])
async def admin_menu(callback_query: types.callback_query):
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=inline_kb_admin)


@dp.callback_query_handler(lambda c: c.data == 'back_to_main')
async def back_to_main(callback_query: types.callback_query):
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=inline_kb_main)
