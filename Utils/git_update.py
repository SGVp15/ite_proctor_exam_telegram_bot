import os
import subprocess
import sys
from asyncio import sleep


def check_for_updates():
    result = subprocess.run(["git", "diff", "--name-only"], capture_output=True, text=True)
    result = subprocess.run(["git", "pull"], capture_output=True, text=True)
    rows = str(result.stdout).split('\n')
    if len(rows) > 3:
        return True
    print(result)
    print(bool(result.stdout))
    return False


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
    await sleep(10)  # Проверка каждые 60 секунд
