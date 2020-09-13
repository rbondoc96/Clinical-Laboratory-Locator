# pylint: disable=import-error
# pylint: disable=anomalous-backslash-in-string

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from tqdm import tqdm 

from navs.search import Search

class LabcorpSearch(Search):
    BLOODWORK = "ROUTINE_PHLEBOTOMY"
    DRUG_SCREEN_COLLECTION = "OCCUPATIONAL_DRUG_SCREENING"
    DRUG_SCREEN_POCT = "RADAR_DRUG_SCREEN"

    def __init__(self, zipcode, radius=25, service=DRUG_SCREEN_COLLECTION):
        Search.__init__(self, zipcode)

        # Labcorp search only takes these values for the radius
        radius = int(radius)
        if radius <= 10:
            self.radius = 10
        elif radius <= 25:
            self.radius = 25
        elif radius <= 50:
            self.radius = 50
        elif radius < 75:
            self.radius = 75
        elif radius < 100 and radius > 100:
            self.radius = 100
    
        self.service = service

    def set_params(self, zipcode=None, radius=None, service=None):
        if zipcode is not None and radius is not None and service is not None:
            self.zipcode = zipcode
            self.radius = radius
            self.service = service
        else:
            raise ValueError(
                "Inputs are None. Please enter 'non-None' fields."
            )

    def search(self, limit=100):
        print(f'[LabCorp Scraper] "Searching for LabCorp PSC Sites within {self.radius} miles of {self.zipcode}..."')
        print(f'[LabCorp Scraper] "Category: {self.service}"')

        # Zipcode search requires pressing an autocomplete option
        # and that doesn't have a 100% success rate with this script
        for attempt in range(5):
            self.driver.get("https://www.labcorp.com/labs-and-appointments/results")

            self.driver.implicitly_wait(1)
            
            # On first visit, there is a Cookie Disclaimer to click
            try:
                cookies_button = self.driver.find_element_by_id(
                    "onetrust-accept-btn-handler"
                )
                cookies_button.click()
            except:
                print('[LabCorp Scraper] "Cookies disclaimer not present."')

            address_box = self.driver.find_element_by_id("edit-address-single")
            service_opt = self.driver.find_element_by_css_selector(
                f"select option[value='{self.service}']"
            )
            search_button = self.driver.find_element_by_id("edit-submit--2")
            radius_box = self.driver.find_element_by_id(
                f"edit-radius-{self.radius}"
            )

            address_box.send_keys(self.zipcode)
            try:
                zipcode_opt = WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "zip-codes-autocomplete-suggestion")
                    )
                )
                zipcode_opt.click()
                break
            except:
                print(f"Error in presssing zip code option. Retry #{attempt+1}")

        service_opt.click()
        radius_box.click()
        search_button.click()

        self.driver.implicitly_wait(2)
        cards = self.driver.find_elements_by_class_name("psc-lab")

        results = []
        if len(cards) > 0:
            print('[LabCorp Scraper] "LabCorps found, scraping info..."')

            limit = limit if limit < len(cards) else len(cards)
            for card, index in zip(
                cards, 
                tqdm(
                    range(limit), 
                    ncols=55,
                    desc="LabCorp"
                )
            ):
                if limit > 0:
                    if index >= limit:
                        break                
                for _ in range(2):
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

                        services_list = card.find_elements_by_css_selector(
                            "ul.psc-lab-services-list li"
                        )

                    except:
                        print("refreshing")
                        self.driver.refresh()

                    finally:
                        for elem, index in zip(
                            services_list, 
                            range(0, len(services_list))
                        ):
                            services_list[index] = elem.get_attribute(
                                "innerText"
                            ).strip()
                        results.append({
                            "distance": distance,
                            "address": address,
                            "hours": hours,
                            "phone_fax": phone_fax,
                            "services": ", ".join(services_list),
                        })
                        break
            print(f'[LabCorp Scraper] "Done scraping info"')
        
        else:
            results = []
            print(f'[LabCorp Scraper] "No LabCorps found within {self.radius} miles of {self.zipcode}"')

        return results

if __name__ == "__main__":
    search = LabcorpSearch(92108, radius=50)
    print(search.search(limit=3))
    del search


