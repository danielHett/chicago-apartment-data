import logging
import requests
from bs4 import BeautifulSoup
from parse_unit import *

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

    for link in links:
        logger.info('start processing the following link: ' + link)
        
        try:
            soup = BeautifulSoup(requests.get(link).text, "html.parser")
            unit = parse_unit(soup)
        except:
            logger.error('something went wrong, moving on to the next link')
            continue

        logger.info(unit)

        logger.info('processing complete for the following link: ' + link)
    
    # For each link, need to run some code. 
    return 'Hello World!'



    

