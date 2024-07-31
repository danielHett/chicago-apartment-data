"""
This script is used to pull all listing data from Domu.com and update S3. 
"""

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import threading
import boto3
import json
import zlib

def process_links(links, processed_units):
    payload = {
        "links": links
    }

    client = boto3.client('lambda')
    response = client.invoke(
        FunctionName='parse_pages',
        InvocationType='RequestResponse',
        Payload=json.dumps(payload),
    )

    units = json.loads(response['Payload'].read())
    
    if type(units) is not list:
        print('ERROR: Recieved something wrong back from parse_pages')
        return

    processed_units.extend(units)

def exists_next_link(driver):
    next_link = driver.find_elements(By.XPATH, '//li[@class="pager__item pager__item--next"]//a')
    return len(next_link) > 0

# Open the webpage with selenium. 
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

# Getting the URLs then kicking off the lambda function that processes them. 
base_url = "https://www.domu.com/chicago-il/apartments?zoom=7&center=41.424332%2C-87.671117&domu_keys=&domu_search=&places_api=&domu_polygon_hood=&domu_bedrooms_min=&domu_bedrooms_max=&domu_bathrooms_min=&domu_bathrooms_max=&domu_rentalprice_min=&domu_rentalprice_max=&sort=acttime&page="
page = 0

processed_units = []
threads = []
while True:
    # Load the next page. 
    driver.get(base_url + str(page))
    
    # Get all listings from the page. 
    links = [link_element.get_attribute('href') for link_element in driver.find_elements(By.XPATH, '//div[@class="view-content"]//a[@class="listing-title"]')]

    baby_thread = threading.Thread(target=process_links, args=(links,processed_units))
    baby_thread.start()
    threads.append(baby_thread)

    # Can we keep going?
    if (exists_next_link(driver)):
        page += 1
        print(page)
    else:
        break

for daddy_thread in threads:
    daddy_thread.join()

client = boto3.client('s3')
response = client.put_object(
    Body=zlib.compress(json.dumps(processed_units).encode('utf-8'), level=9),
    Bucket='chicago-apartment-data',
    Key='listing-data'
)