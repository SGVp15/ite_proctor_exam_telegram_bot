import asyncio
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from Itexpert.check_log_send_email import check_log_and_send_email
from Itexpert.ite_api import send_all_reports_and_cert
from Moodle.main import download_reports_moodle
from Moodle.parser_html import create_all_report
from Telegram.main import start_bot
from Utils.chromedriver_autoupdate import ChromedriverAutoupdate
from Utils.git_update import git_update
from Utils.log import log


async def main():
    # Инициализируем планировщик ТОЛЬКО здесь (внутри запущенного цикла)
    scheduler = AsyncIOScheduler()

    # Запуск проверки логов ровно в 00 и 30 минут
    scheduler.add_job(
        check_log_and_send_email,
        CronTrigger(minute='0,30'),
        id='check_log_and_send_email'
    )

    # Запуск download_reports_moodle ровно в 00 минут
    scheduler.add_job(
        download_reports_moodle,
        CronTrigger(minute='0'),
        id='download_reports_moodle'
    )

    # Запуск проверки create_all_report в 00 минут
    scheduler.add_job(
        create_all_report,
        CronTrigger(minute='52'),
        id='create_all_report'
    )
    # Запуск проверки create_all_report в 00 минут
    scheduler.add_job(
        send_all_reports_and_cert,
        CronTrigger(hour='18', minute='0'),
        id='send_all_reports_and_cert'
    )

    # Запуск проверки обновлений Git каждые 60 секунд (вместо while True)
    scheduler.add_job(
        git_update,
        IntervalTrigger(seconds=60),
        id='git_check',
        next_run_time=datetime.now()  # Проверить сразу при старте
    )

    scheduler.start()
    log.info("Планировщик запущен успешно.")

    # Запускаем бота (это заблокирует выполнение, пока бот работает)
    await start_bot()


if __name__ == '__main__':
    # Внешние проверки (синхронные)
    ChromedriverAutoupdate(operatingSystem="win").check()

    try:
        log.info('Exam_Registration_bot START')
        # asyncio.run сам создаст loop и запустит main()
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.info("Бот остановлен")
    finally:
        log.error('Exam_Registration_bot STOP')
