# pylint: disable=import-error
# pylint: disable=anomalous-backslash-in-string

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

import time
from tqdm import tqdm

from navs.search import Search

class GMapsSearch(Search):
    URGENT_CARE = "Urgent Care"
    OCCUPATIONAL_HEALTH = "Occupational Health"

    def __init__(
        self, 
        zipcode, 
        keywords=URGENT_CARE, 
        headless=True
    ):
        super(GMapsSearch, self).__init__(zipcode, headless)
        self.keywords = keywords

    def search(self, limit=100):
        print(f'[Google Maps Scraper] "Searching for locations near {self.zipcode}..."')            
        print(f'[Google Maps Scraper] "Keywords: {self.keywords}"')

        self.driver.get("https://www.google.com/maps/@32.7559447,-117.1131,14z") 

        time.sleep(2)
        for _ in range(3):
            try: 
                input_box = self.driver.find_element_by_id(
                    "searchboxinput"
                )
                input_box.click()
                input_box.send_keys(self.zipcode)
                input_box.send_keys(Keys.RETURN)

                break
            except Exception as e:
                print(str(e))
                print("Error in running page. Refreshing")
                self.driver.refresh() 

        self.driver.implicitly_wait(2)
        nearby_button = self.driver.find_element_by_css_selector(
            "button[data-value='Nearby']"
        )
        nearby_button.click()

        time.sleep(0.5)
        input_box.click()
        input_box.send_keys(self.keywords)
        input_box.send_keys(Keys.RETURN)
        
        time.sleep(2)
        pane = self.driver.find_element_by_id("pane")
        query = pane.find_elements_by_class_name("section-result")

        results = []
        if len(query) > 0:
            print('[Google Maps Scraper] "Locations found, scraping info..."')

            limit = limit if limit < len(query) else len(query)
            for index in tqdm(range(limit), ncols=55, desc="GMaps"):
                item = dict()
                action = ActionChains(self.driver)
                q = query[index]
                action.move_to_element(q).perform()

                # Sleep needed is a bit longer when distances from zip 
                # are larger
                time.sleep(1.1)
                
                # The text from the element is formatted as:
                # "10 min · 3.9 miles"
                route = self.driver.find_element_by_class_name(
                    "route-preview-controls-message-container"
                ).get_attribute("innerText").split("·")
                
                item["distance"] = route[1].strip()
                item["drive_time"] = route[0].strip()
                
                q.click()
                self.driver.implicitly_wait(1)
                try:
                    name = pane.find_element_by_class_name(
                        "section-hero-header-title-title"
                    ).get_attribute("innerText").strip()
                    item["name"] = name
                except:
                    name = None

                try: 
                    hours = pane.find_element_by_class_name(
                        "section-open-hours-container"
                    ).get_attribute("innerText")
                    hours = hours.replace(
                        "Holiday", ""
                    ).replace(
                        "hours", ""
                    ).replace(
                        "Hours", ""
                    ).replace(
                        "might", ""
                    ).replace(
                        "differ", ""
                    ).replace(
                        "\t", ""
                    ).replace(
                        "                ", "\n"
                    ).replace(
                        "    ", " "
                    ).strip()
                    item["hours"] = hours
                except:
                    hours = None
                
                try:
                    address = pane.find_element_by_css_selector(
                        "button[data-tooltip='Copy address']"
                    ).get_attribute("innerText").strip()
                    item["address"] = address
                except:
                    address = None

                try:
                    phone = pane.find_element_by_css_selector(
                        "button[data-tooltip='Copy phone number']"
                    ).get_attribute("innerText").strip()
                    item["phone"] = phone
                except:
                    phone = None

                back_button = pane.find_element_by_class_name(
                    "section-back-to-list-button"
                )
                back_button.click()
                time.sleep(1)
                query = pane.find_elements_by_class_name("section-result")

                results.append(item)

            print('[Google Maps Scraper] "Done scraping info"')            
        
        else:
            print(f'[Google Maps Scraper] "No locations found near {self.zipcode}"')
        
        return results

if __name__ == "__main__":
    from search import Search
    search = GMapsSearch(
        57633, 
        headless=False, 
        keywords=GMapsSearch.OCCUPATIONAL_HEALTH
    )
    results = search.search(limit=5)
    del search