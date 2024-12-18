import os
import time

from selenium import webdriver
from selenium.common import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException, \
    StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium_stealth import stealth

from Ispring.config import PASSWORD_ISPRING
from Ispring.ispring2 import IspringApi
from Utils.xml_to_dict import get_ispring_only_quiz


class WebDriverIspring:
    def __init__(self):
        # ChromedriverAutoupdate(operatingSystem="win").check()

        options = webdriver.ChromeOptions()
        # options.add_argument("start-maximized")

        options.add_argument("--headless")

        os.makedirs("./Tutorial/down", exist_ok=True)

        prefs = {'download.default_directory': "./Tutorial/down",
                 'download.prompt_for_download': False,
                 'download.default_behavior': 'allow'}
        options.add_experimental_option('prefs', prefs)

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--disable-notifications")

        options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": "./Tutorial/down"}
        options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(options=options)
        self.driver.minimize_window()
        stealth(self.driver,
                languages=["ru-RU", "ru"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        self.web_error = (NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException,
                          ElementNotInteractableException)

        self.authorization()

        s = IspringApi().get_content()
        courses = get_ispring_only_quiz(s)
        self.urls = [
            (f'https://itexpert.ispringlearn.ru/app/admin-portal/content/'
             f'{c.get('contentItemId')}'
             f'/edit/notifications') for c in courses]
        self.clicker_check_box()

    def find_element(self, by, value, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))

    def authorization(self):
        self.driver.get('https://itexpert.ispringlearn.ru/')
        for i in range(2):
            try:
                input_login = self.find_element(By.ID, value='loginField')
                input_password = self.find_element(By.ID, value='passwordField')
                button_enter = self.find_element(By.CLASS_NAME, value='submit_button')
                if input_password and input_login and button_enter:
                    input_login.clear()
                    input_login.send_keys('ANO_UC_DPO')

                    input_password.clear()
                    input_password.send_keys(PASSWORD_ISPRING)
                    button_enter.click()
                # cookies = self.driver.get_cookies()
                # print(cookies)
                break
            except self.web_error:
                pass

    def clicker_check_box(self):
        for i, url in enumerate(self.urls):
            self.driver.get(url)
            try:
                check_box_send_email_to_user = self.find_element(
                    By.XPATH,
                    '/html/body/div/div[1]/div[2]/div[3]/div[3]/div/div/div/div/div/div[3]/div[2]/div/div[1]/div/div/input'
                )
                check_box_send_email_to_admin_exam_ok = self.find_element(
                    By.XPATH,
                    '/html/body/div/div[1]/div[2]/div[3]/div[3]/div/div/div/div/div/div[7]/div[2]/div[2]/div[1]/div/div/input'
                )
                check_box_send_email_to_admin_exam_not_ok = self.find_element(
                    By.XPATH,
                    '/html/body/div/div[1]/div[2]/div[3]/div[3]/div/div/div/div/div/div[7]/div[2]/div[2]/div[2]/div/div/input'
                )

                save_button = self.find_element(
                    By.XPATH, '/html/body/div/div[1]/div[2]/div[3]/div[3]/div/div/div/div/div/div[1]/button')
            except TimeoutException:
                continue

            if check_box_send_email_to_user.get_attribute('data-at') == 'state=true':
                check_box_send_email_to_user.click()
                save_button.click()
                print('send_email_to_user', url)

            if check_box_send_email_to_admin_exam_ok.get_attribute('data-at') != 'state=true':
                check_box_send_email_to_admin_exam_ok.click()
                time.sleep(1)
                save_button.click()
                print('admin_exam_ok', url)

            if check_box_send_email_to_admin_exam_not_ok.get_attribute('data-at') != 'state=true':
                check_box_send_email_to_admin_exam_not_ok.click()
                time.sleep(1)
                save_button.click()
                print('admin_exam_not_ok', url)

    def quit(self):
        self.driver.quit()


if __name__ == '__main__':
    WebDriverIspring()
