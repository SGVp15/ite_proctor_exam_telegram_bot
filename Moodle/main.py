import asyncio
import re
from asyncio import sleep

from .config import DIR_HTML_DOWNLOAD, BASE_URL
from .moodleSelenium.moodle_selenium import MoodleSelenium
from Utils.log import log


async def download_reports_moodle(is_only_new=True, start_num=None):
    file_names = [int(re.sub(r'\.html$', '', f.name)) for f in DIR_HTML_DOWNLOAD.iterdir() if
                  f.is_file() and f.name.endswith('html')]
    webdriver_moodle = MoodleSelenium(base_url=BASE_URL)
    await webdriver_moodle.authorization()
    await sleep(2)

    k = 0
    i = 0
    if file_names and not is_only_new:
        i = max(file_names)
    if start_num:
        i = start_num

    while True:
        i += 1
        if is_only_new and i in file_names:
            k = 0
            continue

        url = f'{BASE_URL}/mod/quiz/review.php?attempt={i}'
        webdriver_moodle.driver.get(url)
        s = webdriver_moodle.driver.page_source
        try:
            h1 = re.findall('<h1.*?>([\s\w]+)</h1>', s)[0]
            if re.findall('ТЕСТ', h1):
                # 1. Ищем ссылку на профиль пользователя
                user_profile_links = re.findall(r'https://exam\.itexpert\.ru/user/view\.php\?id=\d+.*', s)
                user_email = "Email не найден"
                if not user_profile_links:
                    continue
                if user_profile_links:
                    profile_url = user_profile_links[0]
                    # Сохраняем текущее окно, чтобы вернуться или просто переходим
                    webdriver_moodle.driver.get(profile_url)
                    profile_source = webdriver_moodle.driver.page_source

                    # 2. Извлекаем Email (поиск по шаблону email в коде страницы профиля)
                    email_match = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', profile_source)
                    if email_match:
                        user_email = email_match[0]
                    else:
                        continue
                    # Возвращаемся обратно
                    webdriver_moodle.driver.back()

                with open(DIR_HTML_DOWNLOAD / f'{i}.html', encoding='utf-8', mode='w') as f:
                    f.write(f'{user_email=}\n{s}')
                    k = 0
                    log.info(f'Download review moodle [{url}]')
            else:
                k += 1
        except IndexError:
            k += 1
        await sleep(0.1)
        if k > 40:
            break
    await webdriver_moodle.quit()
    return None
