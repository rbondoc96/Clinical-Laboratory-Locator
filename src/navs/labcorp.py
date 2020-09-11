# pylint: disable=import-error
# pylint: disable=anomalous-backslash-in-string

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from navs.search import Search

class LabCorpSearch(Search):
    BLOODWORK = "ROUTINE_PHLEBOTOMY"
    DRUG_SCREEN_COLLECTION = "OCCUPATIONAL_DRUG_SCREENING"
    DRUG_SCREEN_POCT = "RADAR_DRUG_SCREEN"

    def __init__(self, zipcode, radius=25, service=DRUG_SCREEN_COLLECTION):
        Search.__init__(self, zipcode)
        self.radius = radius
        self.service = service

    def search(self):
        PATH = "C:\Program Files (x86)\chromedriver.exe"
        driver = webdriver.Chrome(PATH)

        # Zipcode search requires pressing an autocomplete option
        # and that doesn't have a 100% success rate with this script
        for i in range(5):
            driver.get("https://www.labcorp.com/labs-and-appointments/results")

            time.sleep(1)
            cookies_button = driver.find_element_by_id(
                "onetrust-accept-btn-handler"
            )
            cookies_button.click()

            address_box = driver.find_element_by_id("edit-address-single")
            service_opt = driver.find_element_by_css_selector(
                f"select option[value='{self.service}']"
            )
            search_button = driver.find_element_by_id("edit-submit--2")
            radius_box = driver.find_element_by_id(
                f"edit-radius-{self.radius}"
            )

            address_box.send_keys(self.zipcode)
            try:
                zipcode_opt = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "zip-codes-autocomplete-suggestion")
                    )
                )
                zipcode_opt.click()
                break
            except:
                print(f"Error in presssing zip code option. Retry #{i+1}")

        service_opt.click()
        radius_box.click()
        search_button.click()

        driver.implicitly_wait(2)
        cards = driver.find_elements_by_class_name("psc-lab")

        if len(cards) > 0:
            print("========== LabCorp Locations ==========")
            print(f"Category: {self.service}")
            for card in cards:
                for j in range(2):
                    try: 
                        address = card.find_element_by_css_selector(
                            "span.address a "
                        ).get_attribute("innerHTML").strip()

                        distance = card.find_element_by_class_name(
                            "location-distance"
                        ).text

                        hours = card.find_element_by_css_selector(
                            "div.psc-lab-schedule span"
                        ).get_attribute("innerHTML")

                        phone_fax = card.find_element_by_class_name(
                            "flex-container"
                        ).get_attribute("innerText")

                    except:
                        print("refreshing")
                        driver.refresh()

                    finally:
                        print("\n=====")
                        print(f"Distance from {self.zipcode}: {distance}")
                        print(f"[Address]\n{address}")
                        print(f"[Hours]\n{hours}")
                        print(f"[Phone & Fax]\nPhone {phone_fax}")

                        break
        else:
            print("========== LabCorp Locations ==========")
            print(f"Category: {self.service}")            
            print(f"\nNo locations found within 100 miles of {self.zipcode}")



