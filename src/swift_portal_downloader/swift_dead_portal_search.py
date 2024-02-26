from bs4 import BeautifulSoup
from typing import List, Tuple

import requests

# Function to generate the page_html and search_soup for a given search_term
# This is the only time we directly requests the portal's url without using wget
def search_page(search_term: str) -> (str, str):
    
    # Construct the search url
    base_search_url = 'https://www.swift.ac.uk/dead_portal/getobject.php'
    search_url = base_search_url + '?name=' + search_term + '&submit=Search+Names'
    
    # Download the search page and parse it
    page_html = requests.get(search_url)
    search_soup = BeautifulSoup(page_html.text, features="lxml")

    return page_html, search_soup

# Function to see how many results a given search_term has returned
def results_type(search_soup: str) -> str:

    # Reads the search_soup to see if the page showed that there is no results by displaying the string 
    # find() will return -1 if that exact string is not found     
    if(search_soup.get_text().find('No entry found in the database with object name matching') != -1):
        return '0'
    elif(search_soup.get_text().find('Download archive data') != -1):
        return '1'
    else:
        return '2+'

# Function to find the tname and tid from a given search soup
# This is for search_terms that had only 1 result found
def get_single_tlist(search_soup: str) -> [str, str]:
    
    # Search the saved soup of the page for the tid and tname
    page_head = str(search_soup.find_all('h1')[0])
    tname = page_head[30:-5]
    page_label = str(search_soup.find_all('label')[1])
    tid = page_label[29:37]
      
    # Returns the tname and tid as a list
    return [tname, tid]

# Function to find the a list of all tnames and tids from a given search soup
# This is for search_terms that had only 2 or more result found
def get_multi_tlists(search_soup: str) -> List[Tuple[str, str]]:    
    
    # Get the main results table
    results_table = search_soup.find("table", {"class": "chTable"})
    
    # Ignore the first row with the names of the columns, and the last row with links for all of the data
    table_rows = results_table.find_all("tr")[1:-1]
    
    # .contents is a list, our table has only one element in it, so take contents[0]
    tids = [row.find("td", {"headers": "row_targ"}).contents[0] for row in table_rows]
    tnames = [row.find("td", {"headers": "row_name"}).contents[0] for row in table_rows]
    tobservations = [row.find("td", {"headers": "row_num"}).contents[0] for row in table_rows]
      
    # Zips and returns the tids and tnames as a list of type Tuple
    all_targets_zip = zip(tids, tnames)
    return list(all_targets_zip)

# Function to generate a list of all obsids from a given tid
def convert_tid_to_obsid(tid: str) -> list[str]:
    
    # For any given target id, there may be multiple observations in their own directories,
    # with the naming scheme {target id}001/, {target id}002/, etc.
    # so we let the server give us the appropriate wget commands because it knows how
    # many observations each target id has
    
    # Generate the wget command and run it
    overwrite_option = '-nc'
    base_wget_url = f'https://www.swift.ac.uk/archive/download.sh?reproc=1&tid={tid}&source=obs&subdir=auxil'
    wget_response = requests.get(base_wget_url, timeout=None)

    # Get just a list of wget commands from the responses we got
    wget_commands = [line for line in wget_response.text.splitlines() if 'wget' in line]
    urls = [command.split()[-1] for command in wget_commands]
    
    # Iterates through each wget url created for all obsids
    obsids =[url[38:-7] for url in urls]
    
    return obsids
