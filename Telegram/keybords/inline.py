from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Telegram.Call_Back_Data import CallBackData

inline_btn_logs = InlineKeyboardButton(text='Скачать Логи', callback_data=CallBackData.download_logs)

inline_kb_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⭐️ Скачать Логи', callback_data=CallBackData.get_log), ],
    [InlineKeyboardButton(text='📩 Скачать Шаблон', callback_data=CallBackData.get_template_file_xlsx), ],
    [InlineKeyboardButton(text='Показать регистрацию ISPRING', callback_data=CallBackData.show_registration), ],
    [InlineKeyboardButton(text='Удалить регистрацию ISPRING', callback_data=CallBackData.edit_registration), ],
    [InlineKeyboardButton(text='>> Admin >>', callback_data=CallBackData.admin_menu), ],
])

inline_kb_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='<< Back <<', callback_data=CallBackData.back_to_main), ],
    [InlineKeyboardButton(text='📩  Скачать Логи Программные', callback_data=CallBackData.get_log_program), ],
])


def del_enrollment(enrollment_id: str):
    inline_kb_del = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Delete', callback_data=f'{CallBackData.del_registration}{enrollment_id}'), ],
    ])
    return inline_kb_del
