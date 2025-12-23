import importlib
import sys
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)


def find_config_modules(root_path):
    """
    Ищет все файлы config.py и возвращает их в виде имен модулей для импорта.
    """
    config_modules = []

    for root, dirs, files in os.walk(root_path):
        # Пропускаем виртуальные окружения и скрытые папки
        if any(part.startswith('.') or part in ('venv', 'env', '__pycache__') for part in root.split(os.sep)):
            continue

        for file in files:
            if file == 'config.py' or file == 'root_config.py':
                # Вычисляем относительный путь от корня проекта
                rel_path = os.path.relpath(os.path.join(root, file), root_path)
                # Превращаем путь в формат модуля: folder/config.py -> folder.config
                module_name = rel_path.replace(os.sep, '.').replace('.py', '')
                config_modules.append(module_name)

    return config_modules


def _test_star_import(module_name):
    """Имитирует 'from module_name import *'"""
    print(f"Проверка: from {module_name} import *")
    try:
        # Пытаемся импортировать
        mod = importlib.import_module(module_name)

        # Проверяем, что внутри нет критических ошибок при обращении к атрибутам
        names = [n for n in dir(mod) if not n.startswith('_')]
        print(f"   [OK] Модуль найден. Объектов для импорта: {len(names)}")
        return True
    except Exception as e:
        print(f"   [ОШИБКА] Не удалось импортировать {module_name}")
        print(f"   Детали: {type(e).__name__}: {e}")
        return False


def test_star_import():
    print(f"Сканирование проекта в: {BASE_DIR}\n")

    # Автоматический поиск модулей
    MODULES = find_config_modules(BASE_DIR)

    if not MODULES:
        print("Конфиг-файлы не найдены.")
        sys.exit(0)

    print(f"Найдено модулей для проверки: {len(MODULES)}")
    print("-" * 40)

    failed_modules = []
    for m in MODULES:
        if not _test_star_import(m):
            failed_modules.append(m)
        print("-" * 40)

    # Итоговый отчет
    if failed_modules:
        print(f"\nИТОГ: Ошибки в {len(failed_modules)} модулях:")
        for fm in failed_modules:
            print(f"  - {fm}")
        sys.exit(1)
    else:
        print("\nИТОГ: Все найденные конфиги успешно импортированы!")
