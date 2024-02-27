from .swift_comet_rename import rename_comet_name

from bs4 import BeautifulSoup
from typing import List, Tuple
from rich.console import Console
from rich.progress import track

import requests
import pathlib

# swift_dead_portal_search.py

# Program to manage the searching the swift portal and get the tlist formatted properly

# Function to generate the page_html and search_soup for a given search_term
# This is the only time we directly requests the portal's url without using wget
def search_page(search_term: str) -> Tuple[str, str]:
    
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
def get_single_tlist(search_soup: str) -> List[Tuple[str, str]]:
    
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

# Method to mass search all terms in search_terms and convert the tlist
# All duplicates observations will be removed from the results
def mass_search(search_terms: list, name_scheme_path: pathlib.Path) -> List[Tuple[str, str]]:
    
    console = Console()
    print()

    # Collect all search results from search_terms
    results = []
    for term in track(search_terms, description="[cyan]Searching portal ...[/]"):
        page_html, search_soup = search_page(search_term = term)
        tlist = get_multi_tlists(search_soup = search_soup)
        results.append(tlist)

    # 'Flattens' results 
    # ie: results = list[list[results_pass1], list[results_pass2], ...] -> full_results = list[results_pass1, results_pass2, ...]
    full_results = [result for index in results for result in index]
        
    # Remove all duplicate search results
    condensed_list = set(full_results) 

    return convert_list_multi(tlist=condensed_list, name_scheme_path=name_scheme_path)

# Function to convert tlist to a converted_list
# tlist=List[Tuple(tid, swift_comet_rename)] -> converted_list=List[Tuple(List[obsids], conventional_name)]
# This conversion is only for len(tlist) >= 2
def convert_list_multi(tlist: str, name_scheme_path: pathlib.Path) -> List[Tuple[str, str]]:
    
    console = Console()

    # Converting all swift names -> conventional names
    console.print('Converting target names[cyan] ...[/]', style="cyan")
    new_name_list = [(tid, rename_comet_name(comet_name=tname, name_scheme_path=name_scheme_path)) for (tid, tname) in tlist]

    # Converting all tids -> list[obsids]
    converted_list = [(convert_tid_to_obsid(tid=tid), conventional_name) for (tid, conventional_name) in track(new_name_list, description="[cyan]Generating observation ids ...[/]")]
    
    return converted_list


# Function to generate a list of all obsids from a given tid
def convert_tid_to_obsid(tid: str) -> List[str]:
    
    # For any given target id, there may be multiple observations in their own directories,
    # with the naming scheme {target id}001/, {target id}002/, etc.
    # so we let the server give us the appropriate wget commands because it knows how
    # many observations each target id has
    
    # Generate the wget command and run it
    # Timeout set to none to ensure https request does not drop (issue for mass search)
    overwrite_option = '-nc'
    base_wget_url = f'https://www.swift.ac.uk/archive/download.sh?reproc=1&tid={tid}&source=obs&subdir=auxil'
    wget_response = requests.get(base_wget_url, timeout=None)

    # Get just a list of wget commands from the responses we got
    wget_commands = [line for line in wget_response.text.splitlines() if 'wget' in line]
    urls = [command.split()[-1] for command in wget_commands]
    
    # Iterates through each wget url created
    obsids =[url[38:-7] for url in urls]
    
    return obsids
