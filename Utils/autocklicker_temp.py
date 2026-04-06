import pyautogui
import keyboard
import time
import sys


def smart_clicker():
    print("=== Autoclicker с выходом на 'Q' ===")

    # 1. Захват цели
    print("\nНаведи мышь на ЦЕЛЬ и подожди 3 секунды...")
    # time.sleep(5)
    target_x, target_y = pyautogui.position()
    print(f"Цель зафиксирована: [{target_x}, {target_y}]")

    # 2. Настройки
    interval = 0.3  # Пауза между кликами в секундах

    print(f"\nЗапуск! Кликаю в цель и возвращаю мышь обратно.")
    print("Чтобы остановить работу, нажми клавишу 'Q' (английскую).")
    print("Или уведи мышь в любой угол экрана.")

    try:
        while True:
            # Проверка нажатия клавиши 'q'
            if keyboard.is_pressed('q'):
                print("\n[!] Остановка по нажатию 'Q'.")
                return

            # Запоминаем текущую позицию твоей руки
            curr_x, curr_y = pyautogui.position()

            # Клик в цель и мгновенный возврат
            pyautogui.click(target_x, target_y)
            pyautogui.moveTo(curr_x, curr_y)

            # Небольшая пауза, чтобы не перегружать процессор
            time.sleep(interval)

    except pyautogui.FailSafeException:
        print("\n[!] Остановка: мышь уведена в угол экрана.")
    except Exception as e:
        print(f"\nОшибка: {e}")

    print("Программа завершена.")


if __name__ == "__main__":
    # Включаем защиту углов экрана
    pyautogui.FAILSAFE = True
    while True:
        if keyboard.is_pressed('space'):
            smart_clicker()