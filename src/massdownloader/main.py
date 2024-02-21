from .swift_dead_portal_search import search_page, get_multi_tlists, get_single_tlist, results_type, convert_tid_to_obsid
from .swift_dead_portal_downloader import download_files
from .swift_utils import prepare_download_dir, remove_incomplete_downloads
from .swift_comet_rename import rename_comet_name
from bs4 import BeautifulSoup
import os
import yaml

def main():
    working_path = os.getcwd()
    with open(f'{working_path}/config.yaml', 'r') as file:
        config = yaml.safe_load(file)  
        download_path = config['download_path']
        dtype_list = config['dtype_list']
    file.close()  
    if (os.path.isdir(f"{download_path}") == False):
            print("Unable to reconize download path in config.yaml")
            return
    while (True):
        print(f"\nSelect option\n\t0 Mass download\n\t1 Search portal for specific query\n\tq Quit")
        user_input = input()
        if (user_input == 'q'):
            return      
        elif (user_input == '0'):
            print("Select mass d")
            search_terms = {"Comet", "P/", "C/"} #{"C/", "Comet", "P/"}
            results = []
            for term in search_terms:
                page_html, search_soup = search_page(search_term = term)
                t_list = get_multi_tlists(search_term = term, search_soup = search_soup)
                results.append(t_list)
            full_results = results[0] + results[1] + results[2]
            condensed_list = set(full_results)
            converted_list = [(convert_tid_to_obsid(t_id), rename_comet_name(t_name)) for (t_id, t_name) in condensed_list] 
        elif (user_input == '1'):
            search_term = input("Search term (press q to return to main menu): ")
            if (search_term == 'q'):
                continue
            page_html, search_soup = search_page(search_term = search_term)
            num_of_results = results_type(search_soup = search_soup) 
            if (num_of_results == '0'):
                print(f"No results found for {search_term}")
                continue
            elif (num_of_results == '1'):
                t_list = get_single_tlist(search_term = search_term, search_soup = search_soup)
            else:
                t_list = get_multi_tlists(search_term = search_term, search_soup = search_soup)
            converted_list = [(convert_tid_to_obsid(t_id), rename_comet_name(t_name)) for (t_id, t_name) in t_list] 
        print(f'Found {len(converted_list)} target id(s) from the portal.') 
        while (True):
            print(f'Confirm download of new results to {download_path}?\n\ty Confirm\n\tn Cancel and return to main menu')
            confirm_download = input()
            if (confirm_download == 'y'):
                remove_incomplete_downloads(download_path=download_path, working_path=working_path)
                prepare_download_dir(converted_list, download_path)
                download_files(tlist=converted_list, dtype_list=dtype_list, dest_dir=download_path) 
                break
            elif (confirm_download == 'n'):
                print('Download canceled')
                break

if __name__ == "__main__":
    sys.exit(main())
