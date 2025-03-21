from scrape_links import scrape_links
from scrape_listing import scrape_listing

# A link to every listing page. 
links = scrape_links()

# We keep track of:
# (1) The data for a successful scrape.
units = []
# (2) the error message for an unsuccessful scrape. 
failures = []

# Process all of the links. 
for link in links:
    try:
        units.append(scrape_listing(link))
    except Exception as e:
        failures.append({ 'link': link, 'errMsg': e })

with open('results.txt','w') as f:
    for unit in units:
        f.write(str(unit) + '\n')
    
with open('failures.txt','w') as f:
    for failure in failures:
        f.write(failure['link'] + '\t\t' + failure['errMsg'] + '\n')
