import logging
from scourgify import normalize_address_record

logger = logging.getLogger()
logger.setLevel("INFO")

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

    # Break up the address into parts 
    address_parts = normalize_address_record(address_text)

    address_information['primary_key'] = create_primary_key(address_parts)
    address_information['secondary_key'] = create_secondary_key(address_parts)
    
    # We get the neighborhood raw text. 
    try:
        neighborhood_soups = soup.find(attrs={"class": "lb__hoods lb__row"}).find_all("a")
        neighborhood_raw_texts = [neighborhood_soup.text for neighborhood_soup in neighborhood_soups]
    except Exception as e:
        raise 
    
    address_information['neighborhoods'] = [neighborhood_raw_text.strip().lower() for neighborhood_raw_text in neighborhood_raw_texts]

    return address_information

def create_primary_key(address_parts):
    primary_key = address_parts['address_line_1'] if 'address_line_1' in address_parts else ''
    primary_key += f' {address_parts['city']}' if 'city' in address_parts else ''
    primary_key += f' {address_parts['postal_code']}' if 'postal_code' in address_parts else ''

    return primary_key

def create_secondary_key(address_parts):
    # if there isn't a unit number, then there can't be multiple units in one building. For now let's ignore sec_unit_type. 
    return address_parts['address_line_2'] if 'address_line_2' in address_parts else 'NONE' 


def parse_beds(soup):
    try:
        raw_bed_text = soup.find(attrs={"class": "attribute-item bed"}).div.text
    except Exception as e:
        raise

    # For now, we are leaving it as a string. 
    # TODO: Find a way to make this an integer. 
    bed_text = raw_bed_text.strip()
    
    return bed_text

def parse_baths(soup):
    try:
        raw_bath_text = soup.find(attrs={"class": "attribute-item bath"}).div.text
    except Exception as e:
        raise

    # For now, we are leaving it as a string. 
    # TODO: Find a way to make this an integer. 
    bath_text = raw_bath_text.strip()
    
    return bath_text
    
# Bring this code back later. 
"""
    # Get the different info sections. 
    try:
        info_sections = soup.find(attrs={"class": "lb__basic"}).find_all("div", recursive=False)
        for info_section in info_sections:
            label = info_section.find(attrs={"class": "label"}).text.strip().replace(':', '').lower().replace(' ', '_').replace('-', '_')
            info = info_section.find(attrs={"class": "label"}).find_next_sibling().text.strip()
            unit[label] = info
            
        
    except:
        print('An error')
"""
    