# pylint: disable=import-error
# pylint: disable=anomalous-backslash-in-string

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Search:
    def __init__(self, zipcode, headless=True):
        self.zipcode = zipcode

        self.chrome_options = Options()
        self.chrome_options.add_argument("--log-level=3")
        if headless:
            self.chrome_options.add_argument("--headless")
        
        self.CHROME_PATH = "C:\Program Files (x86)\chromedriver.exe"

        self.driver = webdriver.Chrome(
            chrome_options=self.chrome_options,
            executable_path=self.CHROME_PATH,
        )

    def __del__(self):
        self.driver.quit()
