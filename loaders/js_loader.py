from loaders.base_loader import BaseLoader
from selenium.webdriver.remote.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.common.by import By

class JSLoader(BaseLoader):
    def __init__(self, driver: WebDriver, link: str):
        super().__init__(link)
        self.driver = webdriver.Chrome()

    def load_site(self) -> str:
        self.driver.get(self.link)
        return self.driver.page_source
    
    def load_link(self, link: str) -> str:
        element = self.driver.find_element(By.LINK_TEXT, link)
        element.click()
        return self.driver.page_source
