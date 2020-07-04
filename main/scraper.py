import os
from checkers import is_in_path
import geckodriver_autoinstaller
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import (
    ElementNotSelectableException,
    ElementNotVisibleException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.expected_conditions import (
    StaleElementReferenceException,
    invisibility_of_element,
)
from selenium.webdriver.support.ui import WebDriverWait


class Driver:
    def __init__(self, path):
        self.options = Options()
        self.options.headless = False
        self.path = path
        self.driver = None
        self.wait = None

    def gecko_install(self):
        if not is_in_path(self.path, "v0.26.0"):
            print(f"Installing WebDriver to {self.path}")
            geckodriver_autoinstaller.install(cwd=True)
            print("WebDriver succesfully installed!")
        else:
            pass

    def start_webdriver(self):
        driver_path = self.path + "/v0.26.0/geckodriver"
        self.driver = webdriver.Firefox(
            executable_path=driver_path, options=self.options,
        )
        self.wait = WebDriverWait(
            self.driver,
            3,
            poll_frequency=0.5,
            ignored_exceptions=[
                ElementNotVisibleException,
                ElementNotSelectableException,
                NoSuchElementException,
            ],
        )

    def stop_driver(self):
        if self.driver is not None:
            self.driver.quit()
        else:
            print("Driver not runnning - passing")
            pass


class Finder(Driver):
    def get_item_by_xpath(self, xpath):
        self.driver.find_element_by_xpath(xpath)

    def get_items_by_xpath(self, xpath):
        self.driver.find_elements_by_xpath(xpath)

    def get_item_by_css(self, css):
        self.driver.find_element(By.CSS_SELECTOR, css)

    def get_items_by_css(self, css):
        self.driver.find_elements(By.CSS_SELECTOR, css)


class Scraper(Finder):
    def start(self):
        self.gecko_install()
        self.start_webdriver()

    def stop(self):
        self.stop_driver()


scrap = Scraper(os.getcwd())
