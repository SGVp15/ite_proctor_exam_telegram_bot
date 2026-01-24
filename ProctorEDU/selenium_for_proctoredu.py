import asyncio
import re

import keyboard
import pygetwindow as pg
import pyperclip
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException, \
    StaleElementReferenceException, TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium_stealth import stealth

from ProctorEDU.config import LOGIN_PROCTOREDU, PASSWORD_PROCTOREDU, SESSIONS_CSV_FILE, USERS_CSV_FILE
from Utils.chromedriver_autoupdate import ChromedriverAutoupdate
from Utils.log import log


async def activate_windows():
    win_names = ['Open', 'Открытие']
    is_win_activate = False
    while is_win_activate is False:
        await asyncio.sleep(1)
        for win_name in win_names:
            if win_name in pg.getAllTitles():
                try:
                    pg.getWindowsWithTitle(win_name)[0].activate()
                    is_win_activate = True
                    return
                except pg.PyGetWindowException:
                    continue
            log.info(f'Wait windows title = {win_name}')


class ProctorEduSelenium:
    def __init__(self):
        ChromedriverAutoupdate(operatingSystem="win").check()

        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")

        # options.add_argument("--headless")

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--disable-notifications")

        self.driver = webdriver.Chrome(
            options=options
        )
        stealth(self.driver,
                languages=["ru-RU", "ru"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        self.driver.get('https://itexpert.proctoring.online/')
        self.web_error = (NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException,
                          ElementNotInteractableException)

    def find_element(self, by, value, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        try:
            element = wait.until(EC.presence_of_element_located((by, value)))
            return element
        except TimeoutException:
            return None

    async def authorization(self):
        self.driver.get('https://itexpert.proctoring.online/')
        for i in range(2):
            try:
                input_password = self.find_element(
                    By.XPATH,
                    value='/html/body/div/div[2]/div[2]/div[2]/div/div[2]/div/input'
                )
                input_login = self.find_element(
                    By.XPATH,
                    value='/html/body/div/div[2]/div[2]/div[2]/div/div[1]/div/input'
                )

                button_enter = self.find_element(
                    By.XPATH,
                    value='//div[@class="webix_scroll_cont"]//button'
                )

                if input_password and input_login and button_enter:
                    input_login.clear()
                    input_login.send_keys(LOGIN_PROCTOREDU)
                    input_password.clear()
                    input_password.send_keys(PASSWORD_PROCTOREDU)
                    button_enter.click()

                await asyncio.sleep(0.2)
                break
            except self.web_error:
                pass

    def alert_message(self):
        self.driver.get(url='https://itexpert.proctoring.online/#!/users')
        try:
            self.find_element(
                By.XPATH, value='//div[@class="webix_message webix_debug"]', timeout=3).click()
        except Exception:
            log.info('No alert_message')

    def is_authorized(self) -> bool:
        if self.driver.current_url != 'https://itexpert.proctoring.online/#!/rooms':
            log.info('Error authorization')
            return False
        return True

    async def create_users_and_session(self):
        self.alert_message()
        if self.is_authorized:
            await self.send_csv(url='https://itexpert.proctoring.online/#!/users',
                                file_path=USERS_CSV_FILE)
            await self.send_csv(url='https://itexpert.proctoring.online/#!/rooms',
                                file_path=SESSIONS_CSV_FILE)

    async def send_csv(self, url='https://itexpert.proctoring.online/#!/users', file_path=USERS_CSV_FILE):
        xpath = xpath_get_button_parrent('webix_icon mdi mdi-upload')
        # //button[.//span[@class={webix_icon mdi mdi-upload}]]
        while True:
            try:
                self.driver.get(url)
                button_upload = self.find_element(By.XPATH, xpath)
                button_upload.click()
                break
            except self.web_error:
                await asyncio.sleep(0.2)
                log.error(f'{xpath=}')
                save_page(self.driver.page_source)
                continue

        await activate_windows()

        await asyncio.sleep(0.5)
        keyboard.write(file_path)
        await asyncio.sleep(0.5)
        keyboard.press('enter')
        await asyncio.sleep(3)

    async def find_session(self, text_to_find: str):
        for _ in range(5):
            try:
                self.driver.get('https://itexpert.proctoring.online/#!/rooms')
                element = self.find_element(By.XPATH,
                                            '//div[@class="webix_view webix_control webix_el_search"]/div/input')
                if element:
                    element.clear()
                    element.send_keys(text_to_find)
                    element.send_keys(Keys.ENTER)
                await asyncio.sleep(1)
                break
            except self.web_error:
                save_page(self.driver.page_source)
                continue
        await asyncio.sleep(1)

    def get_urls_sessions(self, list_session: str):
        out = {}
        for session in list_session:
            out[session] = self.get_url_session(session)
        return out

    async def get_url_session(self, text_to_find: str) -> str:
        for _ in range(3):
            await self.find_session(text_to_find)
            try:
                # Click first row
                xpath = '//div[@column="1"][1]/div/a[1]'
                self.find_element(By.XPATH, xpath).click()
                await asyncio.sleep(1)

                # Copy user link to clipboard
                xpath = xpath_get_button_parrent('webix_icon mdi mdi-link-variant')
                self.find_element(By.XPATH, xpath).click()
                await asyncio.sleep(1)

                buffer = ''
                buffer = pyperclip.paste()
                pyperclip.copy = ''
                await asyncio.sleep(1)
                self.driver.get('https://itexpert.proctoring.online/#!/users')
                if re.findall(r'https://itexpert\.proctoring\.online.*', buffer):
                    return buffer
                else:
                    continue
            except self.web_error:
                save_page(self.driver.page_source)
                log.error('NoSuchElement')
        return ''

    async def download_report_file(self, text_to_find):
        await self.find_session(text_to_find)
        try:
            # Click to report
            xpath = '//a[@class="report_link webix_icon mdi mdi-file-video"]'
            self.find_element(By.XPATH, xpath).click()
            await asyncio.sleep(1)

            # Download PDF file
            xpath = xpath_get_button_parrent('webix_icon_btn mdi mdi-file-pdf-box')
            self.find_element(By.XPATH, xpath).click()
            await asyncio.sleep(1)
            return 'ok'
        except self.web_error:
            return 'элемент не найден'

    async def del_session(self, text_to_find: str) -> str:
        await self.find_session(text_to_find)
        # Click first row
        xpath = '//div[@column="1"][1]/div/a[1]'
        self.find_element(By.XPATH, xpath).click()
        await asyncio.sleep(5)

        return ''

    def quit(self):
        self.driver.quit()


def xpath_get_button_parrent(class_name: str) -> str:
    xpath = f'//button[.//span[@class="{class_name}"]]'
    return xpath


def save_page(html):
    import os
    from datetime import datetime
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H-%M-%S")
    file = f"./logs/{current_date}/{current_time}.html"
    os.makedirs(os.path.dirname(file), exist_ok=True)

    with open(file, 'w') as f:
        f.write(html)
