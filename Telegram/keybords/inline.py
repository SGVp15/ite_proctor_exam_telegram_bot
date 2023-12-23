from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Call_Back_Data import CallBackData as callback

inline_btn_logs = InlineKeyboardButton('Скачать Логи', callback_data=callback.download_logs)

inline_kb_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⭐️ Скачать Логи', callback_data=callback.get_log), ],
    [InlineKeyboardButton(text='📩 Скачать Шаблон', callback_data=callback.get_template_file_xlsx), ],
    [InlineKeyboardButton(text='>> Admin >>', callback_data=callback.admin_menu), ],
])

inline_kb_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='<< Back <<', callback_data=callback.back_to_main), ],
    [InlineKeyboardButton(text='📩  Скачать Логи Программные', callback_data=callback.get_log_program), ],
])
