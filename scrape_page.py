from bs4 import BeautifulSoup
from shared_utilities import get_page_html

"""
TODO: Maybe validate the structure of the HTML that we are scraping each field from? Furthermore make sure the value is something
      we expect. 
"""

"""
This one is more complicated. Domu has two types of listings:
    (1) A single unit listing. The price is displayed under the address like so:

        <div class="lb__price">
            <div> $1,980 </div>
            <span>
                <div> /MO <div>
            </span>
        </div>
       
        To get the bed/baths, we need to look at a different part of the page. 

        <div class="lb__attributes">
            <div class="attribute-item bed"><div> ... </div></div>
            <div class="attribute-item bath"><div> ... </div></div>
            <div class="attribute-item housing-type"></div>
        </div>

    (2) Many units are listed. Each unit is stored in a <table> element with class "desktop-units-table". Then, nested under 
        the table element, there is a <thead> element that gives information on what each column corresponds to. Then each <tbody>
        contains <tr> elements, which each correspond to a unit. Each <tr> has multiple <td> elements, which correspond to the rows. 
"""
PRICE_CLASS = 'lb__price'
def scrape_units(soup):
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

"""
Title. 

<h1 class="lb__title">
    <span> ... </span>
</h1>
"""
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