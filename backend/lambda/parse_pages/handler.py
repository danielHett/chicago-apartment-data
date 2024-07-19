import logging
import requests
from bs4 import BeautifulSoup
from parse_unit import *
from storage_utils import store_unit

logger = logging.getLogger()
logger.setLevel("INFO")

"""
this lambda takes an array of links in the event object and updates a table. 
"""
def handler(event, context):
    logger.info('starting parse_pages handler')

    if 'links' not in event:
        logger.error('the field \'links\' was not included in the request')
        raise Exception('the field \'links\' must be included in the request event')
    
    links = event['links']
    results = []

    for link in links:
        logger.info('start processing the following link: ' + link)
        
        try:
            soup = BeautifulSoup(requests.get(link).text, "html.parser")

            # There are two different types of pages. We don't process multi-unit pages (yet). 
            if len(soup.find_all(attrs={"class": "units"})) != 0:
                logger.info('this was a multi-unit page. skipping.')
                results.append({ 'link': link, 'action': 'skipped', 'reason': 'was multi-unit' })
                continue

            unit = parse_unit(soup)
        except:
            logger.error('something went wrong, moving on to the next link')
            results.append({ 'link': link, 'action': 'skipped', 'reason': 'error while parsin' })
            continue

        logger.info(unit)

        logger.info('begin storing in DynamoDB')

        try:
            action = store_unit(unit)
        except:
            logger.error('failed while storing. moving on.')
            results.append({ 'link': link, 'action': 'skipped', 'reason': 'error while storing' })
            continue

        results.append({ 'link': link, 'action': action })

        logger.info('processing complete for the following link: ' + link)

    # For each link, need to run some code. 
    return results



    

