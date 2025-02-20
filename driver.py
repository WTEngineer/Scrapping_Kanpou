from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import InvalidSessionIdException, NoSuchElementException, ElementNotInteractableException
import threading
import time
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

target_url = os.getenv("TARGET_URL")
target_url_login = os.getenv("LOGIN_URL")
email = os.getenv("ACCOUNT_EMAIL")
password = os.getenv("ACCOUNT_PWD")

class Driver:
    def __init__(self):
        self.createBrowser()
    
    def createBrowser(self):
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--window-size=1280,800")
        # self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        print("Loading Page ...")
        # self.driver.get(target_url)
        print("--------Ready------")
        self.status = 'ready'
        self.response = None

    def is_available(self):
        return self.status == 'ready'
    
    def reload_page(self):
        try:
            self.driver.get(target_url)
        except Exception:
            return
        
    def login(self):
        try:
            self.driver.get(target_url_login)
            # WebDriverWait(self.driver, 50).until(lambda driver: self.driver.find_element(By.XPATH, "//input[@name=\"email\"]"))
            self.driver.find_element(By.XPATH, "//input[@id=\"userId_input\"]").clear()
            self.driver.find_element(By.XPATH, "//input[@id=\"userId_input\"]").send_keys(email)
            time.sleep(1)
            self.driver.find_element(By.XPATH, "//input[@id=\"password_input\"]").clear()
            self.driver.find_element(By.XPATH, "//input[@id=\"password_input\"]").send_keys(password)
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//input[@id=\"btnLogin\"]').click()
            WebDriverWait(self.driver, 50).until(lambda driver: self.driver.find_element(By.XPATH, '//article'))
            # Check if element exists
            if self.driver.find_elements(By.CSS_SELECTOR, "form[name='formConfirm'] button[name='login']"):
                self.driver.find_element(By.CSS_SELECTOR, "form[name='formConfirm'] button[name='login']").click()
            WebDriverWait(self.driver, 50).until(lambda driver: self.driver.find_element(By.XPATH, '//article/div[@class=\"serviceBox\"]/section[@class=\"article\"]'))
            time.sleep(3)
            self.response = self.driver.page_source
            self.status = 'ready'
        except Exception as err:
            print("Exception in login process")
            print(err)

    def do_login(self):
        self.status = 'busy'
        threading.Thread(target=self.login, args=()).start()

    # get Magazine Page
    def get_article_page_execute(self, start_date, end_date, search_word):
        try:
            WebDriverWait(self.driver, 50).until(lambda driver: self.driver.find_element(By.XPATH, '//div[@class=\"serviceBox\"]/section[@class=\"article\"]'))
            # click search box
            self.driver.find_element(By.XPATH, '//div[@class=\"serviceBox\"]/section[@class=\"article\"]//ul[@class=\"btnMenu\"]/li[1]/a/img').click()
            time.sleep(1)
            WebDriverWait(self.driver, 50).until(lambda driver: self.driver.find_element(By.XPATH, '//input[@name=\"searchFormEnt.startYear\"]'))
            year, month, day = start_date.split("-")
            self.driver.find_element(By.XPATH, '//input[@name=\"searchFormEnt.startYear\"]').clear()
            self.driver.find_element(By.XPATH, '//input[@name=\"searchFormEnt.startYear\"]').send_keys(year)
            self.driver.find_element(By.XPATH, '//input[@name=\"searchFormEnt.startMonth\"]').clear()
            self.driver.find_element(By.XPATH, '//input[@name=\"searchFormEnt.startMonth\"]').send_keys(month)
            self.driver.find_element(By.XPATH, '//input[@name=\"searchFormEnt.startDay\"]').clear()
            self.driver.find_element(By.XPATH, '//input[@name=\"searchFormEnt.startDay\"]').send_keys(day)
            year, month, day = end_date.split("-")
            self.driver.find_element(By.XPATH, '//input[@name=\"searchFormEnt.endYear\"]').clear()
            self.driver.find_element(By.XPATH, '//input[@name=\"searchFormEnt.endYear\"]').send_keys(year)
            self.driver.find_element(By.XPATH, '//input[@name=\"searchFormEnt.endMonth\"]').clear()
            self.driver.find_element(By.XPATH, '//input[@name=\"searchFormEnt.endMonth\"]').send_keys(month)
            self.driver.find_element(By.XPATH, '//input[@name=\"searchFormEnt.endDay\"]').clear()
            self.driver.find_element(By.XPATH, '//input[@name=\"searchFormEnt.endDay\"]').send_keys(day)
            
            self.driver.find_element(By.CSS_SELECTOR, '#keyword1_input').clear()
            self.driver.find_element(By.CSS_SELECTOR, '#keyword1_input').send_keys(search_word)

            # checkedVal = self.driver.find_element(By.CSS_SELECTOR, '//input[@type=\"checkbox\"][@id=\"searchFormEnt.saiban\"]').get_attribute("checked")
            checkbox = self.driver.find_element(By.XPATH, "//input[@type=\"checkbox\"][@id=\"searchFormEnt.saiban\"]")
            if checkbox.is_selected():
                self.driver.find_element(By.XPATH, '//input[@type=\"checkbox\"][@id=\"searchFormEnt.saiban\"]').click()

            self.driver.find_element(By.CSS_SELECTOR, '#btnSearch').click()
            WebDriverWait(self.driver, 50).until(lambda driver: self.driver.find_element(By.XPATH, '//form[@name="formSearch"]'))
            time.sleep(2)
            self.response = self.driver.page_source
            self.status = 'ready'
        except Exception as err:
            print("Exception in get article page")
            print(err)

    def get_article_page(self, start_date, end_date, search_word=""):
        self.status = 'busy'
        threading.Thread(target=self.get_article_page_execute, args=(start_date, end_date, search_word)).start()

    def execute(self, task, url=None):
        try:
            if task == 'get_page' and url:
                # check if the element exist
                elements = self.driver.find_elements(By.XPATH, '//input[@id="searchboxinput"]')
                if len(elements) == 0:
                    # close
                    self.reload_page()
                else:
                    self.driver.find_element(By.XPATH, '//input[@id="searchboxinput"]').clear()
                    self.driver.find_element(By.XPATH, '//input[@id="searchboxinput"]').send_keys(url)
                    self.driver.find_element(By.XPATH, '//button[@id="searchbox-searchbutton"]').click()
                    time.sleep(4)
                    self.response = self.driver.page_source
            self.status = 'ready'
        except NoSuchElementException:
            # handle the exception
            print("Element not found")
            self.reload_page()
        except ElementNotInteractableException:
            self.reload_page()
        except InvalidSessionIdException:
            self.createBrowser()

    def get_page(self, url):
        self.status = 'busy'
        threading.Thread(target=self.execute, args=('get_page', url)).start()

    def has_response(self):
        return self.response is not None
    
    def get_response(self):
        if self.status == 'ready':
            result = self.response
            self.response = None
            return result
    
    def release(self):
        self.response = None
        self.status = 'ready'

    def close(self):
        self.release()
        self.driver.close()