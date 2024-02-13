from .swift_dead_portal_search import search_page, get_multi_tlists, get_single_tlist, results_type
from .swift_utils import convert_names, search_download_dir, remove_incomplete_downloads
from bs4 import BeautifulSoup
import os
import yaml

def main():
    with open('/Users/jduffy0121/Desktop/AMO/Image_Analysis/mass_downloader/config.yaml', 'r') as file:
        config = yaml.safe_load(file)  
        download_path = config['download_path']
    file.close()
    if (os.path.isdir(f"{download_path}") == False):
            print("Unable to reconize download path in config.yaml")
            return
    while (True):
        print(f"\nSelect option\n\t0 Mass download\n\t1 Search portal for specific query\n\tq Quit")
        user_input = input()
        if (user_input = 'q'):
            return
        elif (user_input == '0'):
            print("Select mass d")
            search_terms = {"Comet", "P/", "C/"}#{"C/", "Comet", "P/"}
            results = []
            for term in search_terms:
                page_html, search_soup = search_page(search_term = term)
                t_list = get_multi_tlists(search_term = term, search_soup = search_soup)
                results.append(t_list)
            full_results = results[0] + results[1] + results[2]
            condensed_list = set(full_results)
        elif (user_input == '1'):
            print("Select search p")
            search_term = input("Search term (press q to return to main menu): ")
            if (search_term == 'q'):
                pass
            page_html, search_soup = search_page(search_term = search_term)
            num_of_results = results_type(search_soup = search_soup)
            if (num_of_results == '0'):
                print(f"No results found for {search_term}")
                pass
            elif (num_of_results == '1'):
                t_list = get_single_tlist(search_term = search_term, search_soup = search_soup)
            else:
                t_list = get_multi_tlists(search_term = search_term, search_soup = search_soup)
        convert_names(t_list = t_list)
        remove_incomplete_downloads(download_path = download_path)
        new_results, duplicates, spliced_t_list = search_download_dir(t_list = t_list, download_path = download_path)
        print(f'Found {len(t_list)} target id(s) from the portal [{duplicates} duplicates and {new_results} new results].')
        if (new_results == 0):
            print('Nothing new to download')
            pass
        while (True):
            print(f'Confirm download of {new_results} new results to {download_path}?\n\ty Confirm\n\tn Cancel and return to main menu')
            confirm_download = input()
            if (confirm_download == 'y'):
                break
            elif (confirm_download == 'n'):
                print('Download canceled')
            else:
                pass

if __name__ == "__main__":
    sys.exit(main())
