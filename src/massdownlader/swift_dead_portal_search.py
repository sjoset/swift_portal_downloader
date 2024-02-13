#hey

import pathlib
import requests
import subprocess
import os

from bs4 import BeautifulSoup
from typing import List, Tuple

    
def get_swift_wget_commands(tid: str, dtype: str, overwrite: bool) -> List[str]:

    # for any given target id, there may be multiple observations in their own directories,
    # with the naming scheme {target id}001/, {target id}002/, etc.
    # so we let the server give us the appropriate wget commands because it knows how
    # many observations each target id has
    
    if overwrite is False:
        overwrite_option = '-nc'
    else:
        overwrite_option = ''
        
    # this page returns a script with wget commands to download our data
    base_wget_url = f'https://www.swift.ac.uk/archive/download.sh?reproc=1&tid={tid}&source=obs&subdir={dtype}'
    wget_response = requests.get(base_wget_url)
    wget_commands = [line for line in wget_response.text.splitlines() if 'wget' in line]
    urls = [command.split()[-1] for command in wget_commands]
    
    # -nc ==> no clobber: don't replace already downloaded files
    # -q ==> quiet mode, no output
    # -w 2 ==> wait 2 seconds between files
    # -nH ==> don't create a directory based on the host, in this case no folder named www.swift.ac.uk/
    # --cut-dirs=2 ==> remove the /archive/reproc/ folders on the server from being created locally
    # -r ==> recursive: grab everything under this folder on the server
    # --reject ... ==> specify files that we don't want from the server
    adjusted_wget_commands = ['wget ' + overwrite_option + ' -q -w 2 -nH --cut-dirs=2 -r --no-parent --reject index.html*,robots.txt* ' + url for url in urls]
    
    return adjusted_wget_commands

def swift_download_uncompressed(tid: str, dtype: str, dest_dir: pathlib.Path = None, overwrite: bool = False) -> None:
    
    # given a Swift target id and type of data, this function downloads the uncompressed
    # data to the directory dest_dir
    
    # get our download commands from the server
    wget_commands = get_swift_wget_commands(tid=tid, dtype=dtype, overwrite=overwrite)
    if wget_commands is None:
        print("No wget commands to execute, skipping downloads...")
        return
    
    # change folders if we need to
    old_cwd = os.getcwd()
    if dest_dir is not None:
        os.chdir(dest_dir)
    print(f"Downloading {dtype} data of target id {tid} to {os.getcwd()} ...")
    
    # run each command to grab the individual observations for this target id
    for command in wget_commands:
        presult = subprocess.run(command.split())
        if presult.returncode != 0:
            print(f"Non-zero return code {presult.returncode} for {command}!")
    
    # change folders back
    os.chdir(old_cwd)

def swift_download_compressed(tid: str, tname: str, dtype: str, archive_type: str, dest_dir: pathlib.Path, overwrite: bool = False) -> None:

    """
        Downloads an archive of Swift data from swift.ac.uk to dest_dir

        Parameters
        ----------
        tid : string
            The target ID to be downloaded, e.g. '00020405'
        tname: string
            The name of the target, e.g. 'CometC/2031US10(Catalina)'
        dtype: string
            The type of data being downloaded, e.g. 'uvot'
        archive_type: string
            One of 'zip' or 'tar' to download the corresponding type
        dest_dir: pathlib.Path
            Directory to place files
        overwrite: bool
            Whether or not to overwrite the file if it already exists
    """
    
    # change folders if we need to
    old_cwd = os.getcwd()
    if dest_dir is not None:
        os.chdir(dest_dir)
    
    # name the archive with the target id and data type, because the server returns 'download.tar' no matter what
    out_file_stem = pathlib.Path(tid + f"_{dtype}")
    
    # download
    if archive_type == 'zip':
        print(f"Downloading .zip archives is broken server-side so is currently unsupported.")
    if archive_type == 'tar':
        swift_download_compressed_tar(tid=tid, tname=tname, dtype=dtype, out_file_stem=out_file_stem, overwrite=overwrite)

    os.chdir(old_cwd)
    return

def swift_download_compressed_tar(tid: str, tname: str, dtype: str, out_file_stem: pathlib.Path, overwrite: bool) -> None:

    out_file = out_file_stem.with_suffix('.tar')
    if out_file.exists() and overwrite is False:
        print(f"Found {str(out_file)} and overwriting was forbidden, skipping download.")
        return
    
    # build our urls and params to send the server
    swift_referer_base_url = 'https://www.swift.ac.uk/archive/prepdata.php'
    swift_download_portal_base_url = 'https://www.swift.ac.uk/archive/download.tar'

    referer_url = f"{swift_referer_base_url}?tid={tid}&source=obs&name={tname}&referer=portal"
    params = {
        'reproc': '1',
        'tid': tid,
        'source': 'obs',
        'subdir': dtype,
    }

    # lie to the server
    request_header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': referer_url,
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Sec-GPC': '1',
    }

    print(f"Attempting to download {tid} of {tname} to {out_file}, please wait ...")
    response = requests.get(swift_download_portal_base_url, params=params, headers=request_header)
    print(f"Requested data from {response.url}, response code {response.status_code} ...")

    # name the output file if it wasn't passed in an argument
    with open(out_file, 'wb') as f:
        f.write(response.content)
    
    print(f"Wrote {str(out_file)}.")

    return

def search_page(search_term: str) -> Tuple[]:
    # construct the search url
    base_search_url = 'https://www.swift.ac.uk/dead_portal/getobject.php'
    search_url = base_search_url + '?name=' + search_term + '&submit=Search+Names'
    
    # download the search page and parse it
    page_html = requests.get(search_url)
    search_soup = BeautifulSoup(page_html.text, features="lxml")
    return page_html, search_soup
    
def results_type(search_soup: str) -> str:
    # reads the html to see if the page showed that there is no results by displaying the string 
    # find() will return -1 if that exact string is not found     
    if(search_soup.get_text().find('No entry found in the database with object name matching') != -1):
        return '0'
    elif(search_soup.get_text().find('Download archive data') != -1):
        return '1'
    else:
        return '2+'
    
def get_single_tlist(search_term: str, search_soup) -> [str, str]:
    global SearchClass
    string = ''
    
    # searches the saved soup html of the page for the tid and tname
    page_head = str(search_soup.find_all('h1')[0])
    tname = page_head[30:-5]
    page_label = str(search_soup.find_all('label')[1])
    tid = page_label[29:37]
    
    # displays the results to the user
    print(f'\nFound a single data file for the search term \'{search_term}\':\n')
    print(f'Name of observation: {tname}'.ljust(67) + 'Total number of observations: 1\n')
    # returns the tname and tid as a list
    return [tname, tid]

def get_multi_tlists(search_term: str, search_soup: str) -> List[Tuple[str, str]]:    
    # get the main results table
    results_table = search_soup.find("table", {"class": "chTable"})
    
    # ignore the first row with the names of the columns, and the last row with links for all of the data
    table_rows = results_table.find_all("tr")[1:-1]
    
    # .contents is a list, our table has only one element in it, so take contents[0]
    tids = [row.find("td", {"headers": "row_targ"}).contents[0] for row in table_rows]
    tnames = [row.find("td", {"headers": "row_name"}).contents[0] for row in table_rows]
    tobservations = [row.find("td", {"headers": "row_num"}).contents[0] for row in table_rows]
    
    # create a dict to show the user the total ammount of data for each observation in tname
    # iterates through tnames and tobservations to count the total times for each tname, storing these values in print_table
    print_table = {}
    i = 0
    while i < len(table_rows):
        print_table[f'{tnames[i]}'] = print_table.get(f'{tnames[i]}', 0) + int(tobservations[i])
        i += 1
    print(f'\nFound the following data for the search term \'{search_term}\':\n')
    
    # prints the table of files found for the user to see what their search results are
    # cast elements in the print_table to be able to index the tname and toal tobservations separately
    j = 0
    while j < len(print_table):
        print(f'Name of observation: {tuple(print_table.items())[j][0]}'.ljust(67) + f'Total number of observations: {tuple(print_table.items())[j][1]}\n')
        j += 1

    # zips and returns the tids and tnames as a list of type Tuple
    all_targets_zip = zip(tids, tnames)
    return list(all_targets_zip)

def download_single_file(tlist: str, dtype_list: str, dest_dir: pathlib.Path, download_type: str, overwrite=False) -> None:
    # downloads the file for a single result when searching
    for dtype in dtype_list:
        if download_type == 'uncompressed':
            swift_download_uncompressed(tid=tlist[1], dtype=dtype, dest_dir=dest_dir, overwrite=overwrite)
        if download_type in ['tar', 'zip']:
            swift_download_compressed(tid=tlist[1], tname=tlist[0], dtype=dtype, archive_type=download_type, dest_dir=dest_dir, overwrite=overwrite)
    
def download_multi_files(tlist: str, dtype_list: str, dest_dir: pathlib.Path, download_type: str, overwrite=False) -> None:
    # downloads the files for 2+ results when searching
    # iterates over each requested data type and observation collected from get_multi_tlists()
    for dtype in dtype_list:
        for tid, tname in tlist:
            if download_type == 'uncompressed':
                swift_download_uncompressed(tid=tid, dtype=dtype, dest_dir=dest_dir, overwrite=overwrite)
            if download_type in ['tar', 'zip']:
                swift_download_compressed(tid=tid, tname=tname, dtype=dtype, archive_type=download_type, dest_dir=dest_dir, overwrite=overwrite)

search_term = input("Search Term: ")
page_html, search_soup = search_page(search_term=search_term)
num_of_results = results_type(search_soup=search_soup)
if(num_of_results == '0'):
    print("ERROR, 0 results")
    sys.exit()
elif(num_of_results == '1'):
    print("1 RESULT")
    get_single_tlist(search_term=search_term, search_soup=search_soup)
else:
    print("2 RESULTS")
    get_multi_tlists(search_term=search_term, search_soup=search_soup)
#print(search_term)
