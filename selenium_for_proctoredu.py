import asyncio
import re

import pyautogui
import pygetwindow as pg
import pyperclip
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException, \
    StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from Config.config import LOGIN_PROCTOREDU, PASSWORD_PROCTOREDU, EXECUTABLE_PATH_WEBDRIVER, SESSIONS_CSV_FILE, \
    USERS_CSV_FILE


async def activate_windows():
    win_names = ['Open', 'Открытие']
    is_win_activate = False
    while is_win_activate == False:
        await asyncio.sleep(1)
        for win_name in win_names:
            if win_name in pg.getAllTitles():
                try:
                    pg.getWindowsWithTitle(win_name)[0].activate()
                    is_win_activate = True
                    break
                except pg.PyGetWindowException:
                    continue
        print(f'Wait windows title = {win_name}')


class Proctor:
    def __init__(self):

        chrome_options = Options()
        # chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--ignore-certificate-errors')

        self.driver = webdriver.Chrome(
            # executable_path=EXECUTABLE_PATH_WEBDRIVER,
            options=chrome_options
        )
        self.driver.get('https://itexpert.proctoring.online/')
        self.web_error = (NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException)

    async def authorization(self):
        exceptions = (NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException)

        text = PASSWORD_PROCTOREDU
        xpath = '/html/body/div/div[2]/div[2]/div[2]/div/div[2]/div/input'
        for i in range(10):
            try:
                await asyncio.sleep(0.2)
                self.driver.find_element(By.XPATH, xpath).clear()
                self.driver.find_element(By.XPATH, xpath).send_keys(text)
                break
            except exceptions:
                continue

        text = LOGIN_PROCTOREDU
        xpath = '/html/body/div/div[2]/div[2]/div[2]/div/div[1]/div/input'
        for i in range(10):
            try:
                await asyncio.sleep(0.2)
                if self.driver.find_element(By.XPATH, xpath):
                    self.driver.find_element(By.XPATH, xpath).clear()
                    self.driver.find_element(By.XPATH, xpath).send_keys(text)
                    break
            except exceptions:
                continue

        xpath = '//button[1]'
        xpath = '/html/body/div/div[2]/div[2]/div[2]/div/div[3]/div/button'
        try:
            await asyncio.sleep(0.2)
            if self.driver.find_element(By.XPATH, xpath):
                self.driver.find_element(By.XPATH, xpath).click()
        except exceptions:
            pass

    async def create_users_and_session(self):
        await self.authorization()
        await self.send_users_csv()
        await self.send_session_csv()

    async def send_users_csv(self):
        xpath = '/html/body/div[3]/div[2]/div[2]/div[1]/div/div[7]/div/button'
        while True:
            try:
                self.driver.get('https://itexpert.proctoring.online/#!/users')
                await asyncio.sleep(0.2)
                self.driver.find_element(By.XPATH, xpath).click()
                self.driver.find_element(By.XPATH, xpath)
                break
            except self.web_error:
                try:
                    xpath_debug = '/html/body/div[17]/div'
                    self.driver.find_element(By.XPATH, xpath_debug).click()
                except self.web_error:
                    pass
                continue

        pyperclip.copy(USERS_CSV_FILE)
        await activate_windows()

        await asyncio.sleep(0.5)
        p = pyperclip.paste()
        pyautogui.hotkey('ctrl', 'v')
        await asyncio.sleep(0.5)
        pyautogui.press('enter')
        await asyncio.sleep(3)

    async def send_session_csv(self):  # Session send CSV
        xpath = '/html/body/div[3]/div[2]/div[2]/div[1]/div/div[9]/div/button'
        while True:
            try:
                self.driver.get('https://itexpert.proctoring.online/#!/rooms')
                await asyncio.sleep(0.2)
                self.driver.find_element(By.XPATH, xpath).click()
                break
            except NoSuchElementException:
                continue

        pyperclip.copy(SESSIONS_CSV_FILE)
        await activate_windows()

        await asyncio.sleep(0.5)
        pyautogui.hotkey('ctrl', 'v')
        await asyncio.sleep(0.5)
        pyautogui.press('enter')
        await asyncio.sleep(3)

    async def find_session(self, text_to_find: str):
        while True:
            try:
                self.driver.get('https://itexpert.proctoring.online/#!/rooms')
                await asyncio.sleep(1)
                xpath = '//input[1]'
                xpath = '/html/body/div[3]/div[2]/div[2]/div[2]/div/div[1]/div/input'
                self.driver.find_element(By.XPATH, xpath).clear()
                self.driver.find_element(By.XPATH, xpath).send_keys(text_to_find)
                self.driver.find_element(By.XPATH, xpath).send_keys(Keys.ENTER)
                await asyncio.sleep(1)
                break
            except self.web_error:
                continue

        await asyncio.sleep(1)

    def get_urls_sessions(self, list_session: str):
        out = {}
        for session in list_session:
            out[session] = self.get_url_session(session)
        return out

    async def get_url_session(self, text_to_find: str) -> str:
        await self.find_session(text_to_find)
        for _ in range(3):
            try:
                # xpath = '//input[@type="text"][2]//a'

                xpath = '/html/body/div[3]/div[2]/div[2]/div[3]/div[2]/div[2]/div/div[2]/div[1]/a'
                self.driver.find_element(By.XPATH, xpath).click()
                await asyncio.sleep(1)
                # class_name = 'webix_icon mdi mdi-link-variant'
                # self.driver.find_element(By.CLASS_NAME, class_name).click()
                xpath = '/html/body/div[13]/div/div[1]/div/div/div[2]/div/button'
                await asyncio.sleep(30)
                self.driver.find_element(By.XPATH, xpath).click()
                await asyncio.sleep(1)

                url = ''
                buffer = ''
                buffer = pyperclip.paste()
                pyperclip.copy = ''
                await asyncio.sleep(1)
                if re.findall(r'https://itexpert\.proctoring\.online.*', buffer):
                    url = buffer
                else:
                    continue

                # Закрыть крточку
                try:
                    xpath = '/html/body/div[12]/div/div[1]/div/div/div[3]/div/button'
                    self.driver.find_element(By.XPATH, xpath).click()
                except self.web_error:
                    print(xpath, 'NoSuchElement')
                return url
            except self.web_error:
                print('NoSuchElement')
        return ''

    async def download_report_file(self, text_to_find):
        await self.find_session(text_to_find)

        await asyncio.sleep(1)
        try:
            xpath = '/html/body/div[3]/div[2]/div[2]/div[3]/div[2]/div[2]/div/div[13]/div[1]/a'
            self.driver.find_element(By.XPATH, xpath).click()
            await asyncio.sleep(1)

            xpath = '/html/body/div[3]/div[2]/div[2]/div[1]/div[1]/div/div[3]/div/button'
            self.driver.find_element(By.XPATH, xpath).click()
            await asyncio.sleep(1)
            xpath = '/html/body/div[20]/div/div[1]/div/div/div[4]/div/button'
            self.driver.find_element(By.XPATH, xpath).click()
            await asyncio.sleep(1)
            return 'ok'
        except self.web_error:
            return 'элемент не найден'

    def quit(self):
        self.driver.quit()
