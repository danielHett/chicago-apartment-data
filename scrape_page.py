from bs4 import BeautifulSoup
from shared_utilities import get_page_html

"""
TODO: Maybe validate the structure of the HTML that we are scraping each field from? Furthermore make sure the value is something
      we expect. 
"""

"""
The price is structured as so:

<div class="lb__price">
    <div> $1,980 </div>
    <span>
        <div> /MO <div>
    </span>
</div>

returns the price, and the interval. 
"""
PRICE_CLASS = 'lb__price'
def scrape_price(soup):
    # specifically the root of where we want to start looking from, not of the whole document. 
    root_tag = soup.find(attrs={'class': PRICE_CLASS})

    return {
        'price': root_tag.div.string.strip(),
        'per': root_tag.span.div.string.strip().replace('/', '')
    }


"""
The neighborhood information:

<h2 class="lb__hoods">
    <div> ... </div>
    <a href="...">North Center</a>
    <span>,</span>
    <a href="...">Roscoe Village</a>
    ...
</h2>
"""
HOOD_CLASS = 'lb__hoods'
def scrape_hoods(soup):
    root_tag = soup.find(attrs={'class': HOOD_CLASS})
    
    hoods = []
    for a in root_tag.find_all('a'):
        hoods.append(a.string.strip())
    
    return hoods

"""
The address. This one is super easy. 

<h2 class="lb__address"> 2416 W Addison St, Chicago, IL, 60618 </h2>
"""
ADDRESS_CLASS = 'lb__address'
def scrape_address(soup):
    root_tag = soup.find(attrs={'class': ADDRESS_CLASS})

    return root_tag.string.strip()

TITLE_CLASS = 'lb__title'
def scrape_title(soup):
    root_tag = soup.find(attrs={'class': TITLE_CLASS})

    return ' '.join(root_tag.span.string.split())

"""
Call this to get back a dictionary will all listing information. 
"""
def scrape_page(listing_link):
    # Turn it into some soup. 
    soup = BeautifulSoup(get_page_html(listing_link), "html.parser")

    return {
        'price_information': scrape_price(soup),
        'hoods': scrape_hoods(soup),
        'address': scrape_address(soup),
        'title': scrape_title(soup)
    }