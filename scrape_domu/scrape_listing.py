import re
import requests
from bs4 import BeautifulSoup

def scrape_listing(link):
    # First, we create a soup (🥫). 
    soup = BeautifulSoup(requests.get(link).text, "html.parser")

    # For now, not parsing multi-unit pages. They are weird. 
    if len(soup.find_all(attrs={"class": "units"})) != 0:
        return None
    
    return parse_unit(soup)

def parse_unit(soup):
    unit = {}
    
    unit['current_price'] = parse_price(soup)
    unit |= parse_address(soup)
    unit['num_beds'] = parse_beds(soup)
    unit['num_baths'] = parse_baths(soup)

    return unit

def parse_price(soup):
    try: 
        raw_price_text = soup.find(attrs={"class": "lb__price"}).div.text
    except Exception as e: 
        raise

    # Remove any commas or dollar signs and strip spaces from the sides. 
    # Then, convert to an integer. 
    return int(raw_price_text.replace(",", "").replace("$", "").strip())

# Returns a dictionary of address information. 
def parse_address(soup):
    address_information = {}
    
    try:
        raw_address_text = soup.find(attrs={"class": "lb__address"}).text
    except Exception as e:
        raise 

    address_text = raw_address_text.strip()

    address_information['full_address'] = address_text
    
    # We get the neighborhood raw text. 
    try:
        neighborhood_soups = soup.find(attrs={"class": "lb__hoods lb__row"}).find_all("a")
        neighborhood_raw_texts = [neighborhood_soup.text for neighborhood_soup in neighborhood_soups]
    except Exception as e:
        raise 
    
    address_information['neighborhoods'] = [neighborhood_raw_text.strip().lower() for neighborhood_raw_text in neighborhood_raw_texts]

    return address_information

# This is staying commented out until a better address parsing tool is found. 
"""
def create_primary_key(address_parts):
    primary_key = address_parts['address_line_1'] if 'address_line_1' in address_parts else ''
    primary_key += f' {address_parts['city']}' if 'city' in address_parts else ''
    primary_key += f' {address_parts['postal_code']}' if 'postal_code' in address_parts else ''

    return primary_key

def create_secondary_key(address_parts):
    # if there isn't a unit number, then there can't be multiple units in one building. For now let's ignore sec_unit_type. 
    return address_parts['address_line_2'] if 'address_line_2' in address_parts else 'NONE' 
"""

def parse_beds(soup):
    try:
        raw_bed_text = soup.find(attrs={"class": "attribute-item bed"}).div.text
    except Exception as e:
        raise

    bed_text = raw_bed_text.strip().lower()

    # Studio is zero bedrooms. 
    if bed_text == 'studio':
        return 0

    # If not studio, it is some variation of "n bed", where n is the number of bedrooms. 
    p = re.compile(r"^[0-9](\.5)? bed(s)?$")
    if not p.match(bed_text):
        raise Exception('Encountered an unexpected value for "bed_text": ' + bed_text)
    
    return int(round(float(bed_text.split()[0])))

def parse_baths(soup):
    try:
        raw_bath_text = soup.find(attrs={"class": "attribute-item bath"}).div.text
    except Exception as e:
        raise

    bath_text = raw_bath_text.strip().lower()

    p = re.compile(r"^[0-9](\.5)? bath(s)?$")
    if not p.match(bath_text):
        raise Exception('Encountered an unexpected value for "bed_text": ' + bath_text)
    
    return int(round(float(bath_text.split()[0])))