import os
import pickle

from UTILS.log import log
from config import PICKLE_FILE_MODIFY, FILE_XLSX


def get_time_modify_file():
    info = ''
    try:
        info = pickle.load(open(PICKLE_FILE_MODIFY, 'rb'))
    except (FileNotFoundError, IOError):
        pass
    return info


def check_update_file_excel_decorator(func):
    def wrapper():
        time_file_modify = get_time_modify_file()
        time_file_modify_now = 0
        try:
            time_file_modify_now = os.path.getmtime(FILE_XLSX)
        except (FileNotFoundError, IOError) as e:
            log(e)

        if time_file_modify != time_file_modify_now:
            func()
            pickle.dump(time_file_modify_now, open(PICKLE_FILE_MODIFY, 'wb'))

    return wrapper


def delete_empty_folder(folder_path):
    try:
        # Проверяем, существует ли папка
        if os.path.exists(folder_path):
            # Проверяем, пуста ли папка
            if os.listdir(folder_path) == []:
                # Удаляем пустую папку
                os.removedirs(folder_path)
        else:
            log(f"Папка {folder_path} не найдена.")
    except OSError as e:
        log(f"Ошибка при удалении папки: {e}")
