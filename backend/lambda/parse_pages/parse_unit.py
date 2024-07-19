import logging
import subprocess 
import sys
from parsing_utils import *

logger = logging.getLogger()
logger.setLevel("INFO")

"""
this is a helper function for parsing unit soup into usable information.  
"""
def parse_unit(soup):
    unit = {}
    
    unit['price'] = parse_price(soup)
    unit['address'] = parse_address(soup)
    unit['num_beds'] = parse_beds(soup)
    unit['num_baths'] = parse_baths(soup)

    return unit