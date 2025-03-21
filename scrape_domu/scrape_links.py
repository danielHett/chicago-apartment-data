"""
This code is used to scrape all of the listing links on the Domu website. 
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def scrape_links():
    # First we set up our driver and open the webpage with selenium. 
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)

    # We need both base_url and page to (1) see the listings and (2) keep track of where we are in the listing pagination. 
    base_url = "https://www.domu.com/chicago-il/apartments?zoom=7&center=41.424332%2C-87.671117&domu_keys=&domu_search=&places_api=&domu_polygon_hood=&domu_bedrooms_min=&domu_bedrooms_max=&domu_bathrooms_min=&domu_bathrooms_max=&domu_rentalprice_min=&domu_rentalprice_max=&sort=acttime&page="
    page = 0

    links = []
    while True:
        # Load the next page. 
        driver.get(base_url + str(page))
        
        # Get all links from the page and append them. 
        links += [link_element.get_attribute('href') for link_element in driver.find_elements(By.XPATH, '//div[@class="view-content"]//a[@class="listing-title"]')]

        # `find_elements` is getting back listings. This is asking the question, "are there any listings left". If there
        # are, we keep going. 
        if (len(driver.find_elements(By.XPATH, '//li[@class="pager__item pager__item--next"]//a')) > 0):
            page += 1
        else:
            break

    return links