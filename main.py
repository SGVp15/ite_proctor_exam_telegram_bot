import asyncio
import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from Itexpert.check_log_send_email import check_log_and_send_email
from Moodle.main import download_reports_moodle
from Moodle.parser_html import create_all_report
from Telegram.main import start_bot
from Utils.chromedriver_autoupdate import ChromedriverAutoupdate
from Utils.git_update import git_update
from Utils.log import log


async def main():
    # Инициализируем планировщик
    scheduler = AsyncIOScheduler()

    # Запуск проверки логов и отправки писем
    scheduler.add_job(
        check_log_and_send_email,
        CronTrigger(minute='0,30'),
        id='check_log_and_send_email'
    )

    # Запуск скачивание страницы отчета из moodle в 00 минут
    scheduler.add_job(
        download_reports_moodle,
        CronTrigger(hour='1'),
        id='download_reports_moodle',
        next_run_time=datetime.datetime.now()  # Проверить сразу при старте
    )

    # Запуск создание отчетов
    scheduler.add_job(
        create_all_report,
        CronTrigger(hour='1', minute='30'),
        id='create_all_report',
        next_run_time=datetime.datetime.now() + datetime.timedelta(minutes=3),  # Проверить сразу при старте
    )

    # Запуск проверки обновлений Git каждые 60 секунд
    scheduler.add_job(
        git_update,
        IntervalTrigger(seconds=60),
        id='git_check',
        next_run_time=datetime.datetime.now()  # Проверить сразу при старте
    )

    scheduler.start()
    log.info("Планировщик запущен успешно.")

    await start_bot()


if __name__ == '__main__':
    ChromedriverAutoupdate(operatingSystem="win").check()

    try:
        log.info('Exam_Registration_bot START')
        # asyncio.run сам создаст loop и запустит main()
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.info("Бот остановлен")
    finally:
        log.error('Exam_Registration_bot STOP')
