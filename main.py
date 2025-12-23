import asyncio
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from Telegram.main import start_bot
from Itexpert.check_log_send_email import check_log_and_send_email
from Utils.chromedriver_autoupdate import ChromedriverAutoupdate
from Utils.git_update import git_update
from Utils.log import log


async def main():
    scheduler = AsyncIOScheduler()

    # 2. Добавляем задачу check_log_and_send_email каждые 30 минут
    # minutes=30 задает интервал.
    # Если нужно запустить задачу сразу при старте, можно добавить next_run_time=datetime.now()
    scheduler.add_job(
        check_log_and_send_email,
        IntervalTrigger(minutes=30),
        id='check_log_job',
        next_run_time=datetime.now(),
        replace_existing=True
    )

    # 3. Запускаем планировщик
    scheduler.start()
    log.info("Планировщик запущен: задача check_log будет выполняться каждые 30 минут.")

    # 4. Формируем список постоянно работающих задач
    # git_update обычно выполняется один раз при старте,
    # а start_bot работает бесконечно.
    tasks = [
        start_bot(),
        git_update(),
    ]

    # Запускаем асинхронные задачи
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    # Предварительная проверка драйвера
    ChromedriverAutoupdate(operatingSystem="win").check()

    try:
        log.info('Exam_Registration_bot START')
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.info('Bot stopped by user')
    finally:
        log.error('Exam_Registration_bot STOP')