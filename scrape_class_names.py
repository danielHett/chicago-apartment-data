# This script is just used for research purposes. Want to see all of the possible class names there are. 

import os
import sys
from bs4 import BeautifulSoup
from shared_utilities import get_page_html
import constants
from threading import Thread, Lock

# Get back a set of class names for a single listing. 
def get_classes(listing):
    # This takes some time. 
    html = get_page_html(listing)

    # Turn it into some soup. 
    soup = BeautifulSoup(html, "html.parser")

    classes = set()
    for tag in soup.find_all(lambda tag : tag.has_attr('class') and any(['lb__' in c for c in tag['class']])):
        for c in tag['class']:
            if ('lb__' in c):
                classes.add(c)
    
    return classes


# This is the function the thread will run. 
def collect_classes(lock, listings, classes):
    while True:
        # Accessing the shared listings array, so we aquire the lock. 
        lock.acquire()

        if len(listings) == 0:
            # Release before returning!
            lock.release()
            return
        
        # Otherwise, we pull a listing. 
        listing = listings.pop()

        # We can release now. 
        lock.release()

        found_classes = get_classes(listing)

        # Modifying a shared resource. Get the lock. 
        lock.acquire()
        classes |= found_classes
        lock.release()


# You can't use thi script unless you've already loaded the listing data file. 
if (not os.path.exists(os.path.join(constants.DATA_FOLDER_PATH, constants.LISTING_FILE_NAME))):
    sys.exit("No listing file found. Run 'populate_listings.py'.")

# Get all of the listings. 
listings = []
with open(os.path.join(constants.DATA_FOLDER_PATH, constants.LISTING_FILE_NAME), "r") as file:
    for listing in file:
        listings.append(listing)

# This is a shared lock. 
lock = Lock()

# This is where all of the classes will be stored. 
classes = set()

t_count = 8
ts = []
for i in range(t_count):
    t = Thread(target=collect_classes, args=[lock, listings, classes])
    t.start()
    ts.append(t)

for t in ts:
    t.join()


print(classes)




