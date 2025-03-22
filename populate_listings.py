# Use this script to create a file in the data folder with newline seperated list of Domu listings. this
# script will overwrite the current list!

import os
from shared_utilities import scrape_links, init_data_folder
import constants

# if the folder doesn't exist, we just make it. 
init_data_folder()

# get a list of all links. 
listings = scrape_links()

with open(os.path.join(constants.DATA_FOLDER_PATH, constants.LISTING_FILE_NAME), "w") as file:
    for listing in listings:
        file.write(listing + '\n')

# Done!
    
