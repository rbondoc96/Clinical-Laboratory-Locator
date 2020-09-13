# pylint: disable=import-error
# pylint: disable=anomalous-backslash-in-string

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from tqdm import tqdm

from navs.search import Search

class ConcentraSearch(Search):
    def set_params(self, zipcode=None):
        if zipcode is not None:
            self.zipcode = zipcode

        else:
            raise ValueError("Please enter a valid zipcode")

    def search(self, limit=100):
        print(f'[Concentra Scraper] "Searching for Concentra locations near {self.zipcode}..."')

        self.driver.get("https://www.concentra.com/urgent-care-centers/#g=&gtext=&glevel=&gstate=")
    
        for _ in range(3):      
            self.driver.implicitly_wait(1)
            input_box = self.driver.find_element_by_css_selector(
                "input.location-search-box-input.tt-input"
            )
            input_box.click()
            input_box.send_keys(self.zipcode)                  
            try:
                autocomplete = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 
                        "div.tt-dataset-1 span.tt-suggestions")
                    )
                )
                choice = autocomplete.find_element_by_class_name(
                    "tt-suggestion"
                )
                choice.click()                
                break
            except:
                print("error in pressing autocomplete")
                self.driver.refresh()

        time.sleep(2)
        results = self.driver.find_elements_by_css_selector(
            "ul.search-result-list li:not([class='component-hidden'])"
        )
        
        if len(results) > 0:
            processed_results = []
            print('[Concentra Scraper] "Concentras found, scraping info..."')
            
            limit = limit if limit < len(results) else len(results)
            for res, index in zip(
                results, 
                tqdm(
                    range(limit),
                    ncols=55, 
                    desc="Concentra"
                )
            ):
                if limit > 0:
                    if index >= limit:
                        break
                try: 
                    self.driver.execute_script(
                        "arguments[0].click()",
                        res
                    )
                    time.sleep(0.8)

                    card = self.driver.find_element_by_class_name(
                        "location-poi"
                    )

                    subname = card.find_element_by_css_selector(
                        "div.field-centername"
                    ).get_attribute("innerText")

                    open_status = card.find_element_by_css_selector(
                        "div.location-open-status"
                    ).get_attribute("innerText")

                    distance = res.find_element_by_class_name(
                        "number-rounder"
                    ).get_attribute("innerHTML").strip()

                    address_line_1 = card.find_element_by_class_name(
                        "field-addressline1"
                    ).get_attribute("innerText")

                    try:
                        address_line_2 = card.find_element_by_class_name(
                            "field-addressline2"
                        )
                    except:
                        address_line_2 = None

                    city = card.find_element_by_class_name(
                        "field-city"
                    ).get_attribute("innerText")

                    state = card.find_element_by_class_name(
                        "field-stateabbreviation"
                    ).get_attribute("innerText")

                    zipcode = card.find_element_by_class_name(
                        "field-zipcode"
                    ).get_attribute("innerText")

                    phone = card.find_element_by_class_name(
                        "field-mainphone"
                    ).get_attribute("innerText")

                    fax = card.find_element_by_class_name(
                        "field-faxnumber"
                    ).get_attribute("innerText")

                    hours = card.find_element_by_css_selector(
                        "div.location-poi div:nth-of-type(2) .location-right div:last-child"
                    ).get_attribute("innerText")

                    entry = {
                        "name": subname,
                        "distance": distance,
                        "open_status": open_status,
                        "address_line_1": address_line_1,
                        "city": city,
                        "state": state,
                        "zipcode": zipcode,
                        "phone": phone,
                        "fax": fax,
                        "hours": hours,
                    }
                    if address_line_2:
                        entry["address_line_2"] = address_line_2.get_attribute(
                            "innerText"
                        )
                    
                    processed_results.append(entry)
            
                except Exception as e:
                    print(str(e))   

            print('[Concentra Scraper] "Done scraping info"')            
            return processed_results
        else:
            print(f'[Concentra Scraper] "No Concentras found near {self.zipcode}"')
            return results       

if __name__ == "__main__":
    from search import Search
    search = ConcentraSearch(90720)
    results = search.search(limit=5)
    del search