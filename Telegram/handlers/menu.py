from aiogram import types, F

from config import ADMIN_ID
from Telegram.keybords.inline import k_admin_menu, inline_kb_main
from Telegram.main import bot, dp
from Telegram.Call_Back_Data import CallBackData


@dp.callback_query(F.data.in_({CallBackData.ADMIN_MENU}) & F.from_user.id.in_({*ADMIN_ID}))
async def admin_menu(callback_query: types.callback_query):
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=k_admin_menu)


@dp.callback_query(F.data.in_({CallBackData.BACK_TO_MAIN}))
async def back_to_main(callback_query: types.callback_query):
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=inline_kb_main)
