from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask
import undetected_chromedriver.v2 as uc
import time
import sys
import requests
import os


class webdriver_functions(object):
    def __init__(self, arguments, browser="Chrome", sub_process=False):

        if browser == "Chrome" or browser == "undetected_chromedriver":
            options = uc.ChromeOptions()
        else:
            options = Options()

        for arg in arguments:
            options.add_argument(arg)

        if browser == "Chrome":
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
            self.driver.delete_all_cookies()

        elif browser == "Firefox":
            os.environ['GH_TOKEN'] = "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"
            self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
            self.driver.delete_all_cookies()

        elif browser == "undetected_chromedriver":
            self.driver = uc.Chrome(options=options)
            self.driver.delete_all_cookies()

    def check_if_xpath_exists(self, xpath, interval=0) -> object:

        time.sleep(interval)
        try:
            self.driver.find_element(By.XPATH, xpath)
            return True
        except:
            return False

    def click_on_xpath(self, xpath, interval=0, iterations=100, terminate=True):

        time.sleep(interval)
        for i in range(1, iterations):

            try:
                self.driver.find_element(By.XPATH, xpath).click()
                break

            except Exception as e:
                if i > 5:
                    print(e)
                if i == iterations:
                    if terminate:
                        sys.exit
                    else:
                        return None
                pass
            time.sleep(1)

    def count_xpath(self, xpath, interval=0, iterations=100, terminate=True):

        time.sleep(interval)
        for i in range(1, iterations):

            try:
                count = len(self.driver.find_elements(By.XPATH, xpath))
                return count

            except Exception as e:
                if i > 5:
                    print(e)
                if i == iterations:
                    if terminate:
                        sys.exit
                    else:
                        return None
                pass
            time.sleep(1)

    def get_text_from_xpath(self, xpath, interval=0, iterations=100, terminate=True):

        time.sleep(interval)
        for i in range(1, iterations):

            try:
                text = self.driver.find_element(By.XPATH, xpath).text
                return text

            except Exception as e:
                if i > 5:
                    print(e)
                if i == iterations:
                    if terminate:
                        sys.exit
                    else:
                        return None
                pass
            time.sleep(1)

    def open_website(self, link, interval=0):

        time.sleep(interval)
        self.driver.get(link)
        time.sleep(1)

    def send_keys_to_text_box(self, xpath, text, interval=0, iterations=100, terminate=True):

        time.sleep(interval)
        for i in range(1, iterations):

            try:
                text_box = self.driver.find_element(By.XPATH, xpath)
                text_box.send_keys(text)
                break

            except Exception as e:
                if i > 5:
                    print(e)
                if i == iterations:
                    if terminate:
                        sys.exit
                    else:
                        return None
                pass
            time.sleep(1)

    def send_enter_key(self, xpath, interval=0, iterations=100, terminate=True):

        time.sleep(interval)
        for i in range(1, iterations):

            try:
                text_box = self.driver.find_element(By.XPATH, xpath)
                text_box.send_keys(Keys.RETURN)
                break

            except Exception as e:
                if i > 5:
                    print(e)
                if i == iterations:
                    if terminate:
                        sys.exit
                    else:
                        return None
                pass
            time.sleep(1)

    def get_xpath_attribute(self, xpath, attribute, interval=0, iterations=100, terminate=True):

        time.sleep(interval)
        for i in range(1, 100):

            try:
                element = self.driver.find_element(By.XPATH, xpath)
                attr = element.get_attribute(attribute)
                return attr

            except Exception as e:
                if i > 5:
                    print(e)
                if i == iterations:
                    if terminate:
                        sys.exit
                    else:
                        return None
                pass
            time.sleep(1)

    def switch_tabs(self, tab_index=-1, interval=0, iterations=100, terminate=True):

        time.sleep(interval)
        for i in range(1, iterations):

            try:
                self.driver.switch_to.window(self.driver.window_handles[tab_index])
                break

            except Exception as e:
                if i > 5:
                    print(e)
                if i == iterations:
                    if terminate:
                        sys.exit
                    else:
                        return None
                pass
            time.sleep(1)

    def get_in_iframe(self, iframe_xpath, interval=0, iterations=10, terminate=True):

        time.sleep(interval)
        for i in range(1, iterations):

            try:
                iframe = self.driver.find_element_by_xpath(iframe_xpath)
                self.driver.switch_to.frame(iframe)
                break

            except Exception as e:
                if i > 5:
                    print(e)
                if i == iterations:
                    if terminate:
                        sys.exit
                    else:
                        return None
                pass
            time.sleep(1)

    def exit_iframe(self):
        try:
            self.driver.switch_to.default_content()
        except Exception as e:
            print(Exception)

    def quit_driver(self):

        self.driver.quit()
        return "Driver closed"

    def get_html_of_link(self, link):
        html = requests.get(link)
        return html.text

    def anit_captcha(self, site_key, anti_c_api_key, url):

        client = AnticaptchaClient(anti_c_api_key)
        task = NoCaptchaTaskProxylessTask(url, site_key)
        job = client.createTask(task)
        job.join()
        g_token = job.get_solution_response()

        self.driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML = "{}";'.format(g_token))
        return g_token


def latest_download_file_rename(new_name):
    path = r'C:\Users\konra\Downloads'
    os.chdir(path)
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    newest = files[-1]
    try:
        os.rename(f"C:/Users/konra/Downloads/{newest}",
                  f"C:/Users/konra/Downloads/{new_name}.{newest.split(sep='.')[1]}")
    except:
        print(new_name)
        pass
