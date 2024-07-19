import logging
from addresser import parse_location

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

def parse_address(soup):
    try:
        raw_address_text = soup.find(attrs={"class": "lb__address"}).text
    except Exception as e:
        raise 

    address_text = raw_address_text.strip()

    # Parse the address. 
    return parse_location(address_text)

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
    