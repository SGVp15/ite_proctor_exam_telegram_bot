import asyncio
import re
from asyncio import sleep

from Moodle.config import DIR_HTML_DOWNLOAD
from Moodle.moodleSelenium.moodle_selenium import MoodleSelenium
from Utils.log import log


async def download_reports_moodle():
    file_names = [int(re.sub(r'\.html$', '', f.name)) for f in DIR_HTML_DOWNLOAD.iterdir() if
                  f.is_file() and f.name.endswith('html')]
    webdriver_moodle = MoodleSelenium(base_url='https://exam.itexpert.ru')
    await webdriver_moodle.authorization()
    await sleep(2)

    k = 0
    i = 0
    if file_names:
        i = min(file_names)
    while True:
        i += 1
        if i in file_names:
            k = 0
            continue
        url = f'https://exam.itexpert.ru/mod/quiz/review.php?attempt={i}'
        webdriver_moodle.driver.get(url)
        s = webdriver_moodle.driver.page_source
        try:
            h1 = re.findall('<h1.*?>([\s\w]+)</h1>', s)[0]
            if re.findall('ТЕСТ', h1):
                with open(DIR_HTML_DOWNLOAD / f'{i}.html', encoding='utf-8', mode='w') as f:
                    f.write(s)
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


if __name__ == '__main__':
    if __name__ == '__main__':
        try:
            asyncio.run(download_reports_moodle())
        except KeyboardInterrupt:
            print("Программа остановлена пользователем")
