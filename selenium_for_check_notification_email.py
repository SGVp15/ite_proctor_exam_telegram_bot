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
        self.web_error = (NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException,
                          ElementNotInteractableException)
        self.authorization()

        s = IspringApi().get_content()
        courses = get_ispring_only_quiz(s)
        self.urls = [
            f'https://itexpert.ispringlearn.ru/app/admin-portal/content/{c.get('contentItemId')}/edit/notifications' for
            c in courses]

        self.check_()

    def authorization(self):
        self.driver.get('https://itexpert.ispringlearn.ru/')

        for i in range(10):
            try:
                time.sleep(0.2)
                input_login = self.driver.find_element(By.ID, 'loginField')
                input_login.clear()
                input_login.send_keys('ANO_UC_DPO')

                time.sleep(0.2)
                input_password = self.driver.find_element(By.ID, 'passwordField')
                input_password.clear()
                input_password.send_keys(PASSWORD_ISPRING)
                time.sleep(0.2)
                button_enter = self.driver.find_element(
                    By.CLASS_NAME,
                    value='submit_button'
                )
                button_enter.click()
                time.sleep(1)
                break
            except self.web_error:
                pass

    def check_(self):
        for url in self.urls:
            self.driver.get(url)
            wait = WebDriverWait(self.driver, 10)
            try:
                check_box_send_email_to_user = wait.until(EC.presence_of_element_located(
                    (By.XPATH,
                     '/html/body/div/div[1]/div[2]/div[3]/div[3]/div/div/div/div/div/div[3]/div[2]/div/div[1]/div/div/input'
                     )))
                check_box_send_email_to_admin_exam_ok = wait.until(EC.presence_of_element_located(
                    (By.XPATH,
                     '/html/body/div/div[1]/div[2]/div[3]/div[3]/div/div/div/div/div/div[7]/div[2]/div[2]/div[1]/div/div/input'
                     )))
                check_box_send_email_to_admin_exam_not_ok = wait.until(EC.presence_of_element_located(
                    (By.XPATH,
                     '/html/body/div/div[1]/div[2]/div[3]/div[3]/div/div/div/div/div/div[7]/div[2]/div[2]/div[2]/div/div/input'
                     )))

                save_button = wait.until(EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div/div[1]/div[2]/div[3]/div[3]/div/div/div/div/div/div[1]/button')))
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
