# pylint: disable=import-error
# pylint: disable=anomalous-backslash-in-string

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from navs.search import Search

class QuestSearch(Search):
    def search(self):
        PATH = "C:\Program Files (x86)\chromedriver.exe"
        driver = webdriver.Chrome(PATH)

        for i in range(1):
            driver.get(
                "https://appointment.questdiagnostics.com/patient/findlocation"
            )

            driver.implicitly_wait(5)
            zipcode_field = driver.find_element_by_id("input-1")
            list_toggle = driver.find_element_by_class_name(
                "reason-find-location__locationDropIcon"
            )
            drug_button = driver.find_element_by_css_selector(
                "button[aria-label='Drug and Alcohol Tests']"
            )
            electronic_drug = driver.find_element_by_class_name(
                "reason-find-location__reasonCheckbox"
            )

            list_toggle.click()
            drug_button.click()
            electronic_drug.click()
            list_toggle.click()

            time.sleep(2)

            zipcode_field.send_keys(self.zipcode)
            try:
                autocomplete = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR, 
                            "ul.md-autocomplete-suggestions li"
                        )
                    )
                )
                autocomplete.click()

            except:
                print(f"Error in presssing zip code option. Retry #{i+1}")
            
            finally: 

                cards = driver.find_elements_by_css_selector(
                    "ul#locationResultScroll li"
                )

                for card in cards:
                    card.click()
                    time.sleep(2)

                # ul#locationResultScroll is list of results
                # li is each card
                # md-menu-content.qd-location-timings__menu-desktop
                # md-menu-item button -- has the hours in aria-label

                time.sleep(1000)
                break