import logging
import requests
from bs4 import BeautifulSoup
from parse_unit import *
import threading

logger = logging.getLogger()
logger.setLevel("INFO")

def get_soup(link, soups):
    try:
        soups.append(BeautifulSoup(requests.get(link).text, "html.parser"))
    except Exception as e:
        logger.error('Failed to either (1) fetch the page or (2) parse it with bs4')

"""
this lambda takes an array of links in the event object and updates a table. 
"""
def handler(event, context):
    logger.info('starting parse_pages handler')

    if 'links' not in event:
        logger.error('the field \'links\' was not included in the request')
        raise Exception('the field \'links\' must be included in the request event')
    
    links = event['links']
    soups = []
    threads = []
    for link in links:
        baby_thread = threading.Thread(target=get_soup, args=(link,soups))
        baby_thread.start()
        threads.append(baby_thread)

    for daddy_thread in threads:
        daddy_thread.join()

    units = []
    for soup in soups:
        logger.info('start processing the following link: ' + link)
        
        try:
            # There are two different types of pages. We don't process multi-unit pages (yet). 
            if len(soup.find_all(attrs={"class": "units"})) != 0:
                logger.info('this was a multi-unit page. skipping.')
                units.append({ 'link': link, 'unit': None, 'failure_reason': 'multi-unit page' })
                continue

            unit = parse_unit(soup)
        except:
            logger.error('something went wrong, moving on to the next link')
            units.append({ 'link': link, 'unit': None, 'failure_reason': 'error while parsing the page' })
            continue

        units.append({ 'link': link, 'unit': unit })

        logger.info('processing complete for the following link: ' + link)

    # For each link, need to run some code. 
    return units



    

