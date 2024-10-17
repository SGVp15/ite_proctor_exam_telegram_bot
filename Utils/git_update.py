import os
import subprocess
import sys
from asyncio import sleep


def check_for_updates():
    result = subprocess.run(["git", "diff"], capture_output=True, text=True)
    print(result.stdout)
    return bool(result.stdout)


def pull_updates():
    subprocess.run(["git", "pull"])


def restart_script():
    python = sys.executable
    os.execv(python, [python] + sys.argv)


async def git_update():
    if check_for_updates():
        print('check_for_updates [ ok ]')
        pull_updates()
        restart_script()
    await sleep(60)  # Проверка каждые 60 секунд
