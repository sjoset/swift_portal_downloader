from .swift_dead_portal_search import search_page, get_multi_tlists, get_single_tlist, results_type, convert_tid_to_obsid, mass_search, convert_list_multi
from .swift_dead_portal_downloader import download_files
from .swift_utils import prepare_download_dir, remove_incomplete_downloads, print_name_scheme, manual_add_name, manual_remove_name, dump_dataframe
from .swift_comet_rename import rename_comet_name

from rich.console import Console
from rich.progress import track
from rich.markdown import Markdown

import os
import yaml
import pandas as pd
import ast
import pathlib
import sys

# spd.py

# Diver program for the swift_portal_downloader
# Manages all menus that the user can navigate

# ==============================================================
# ==============================================================
#                   Program init
#                       |
#                   read config
#                       |
#               --- user_input_1  -----        
#              /    |       |   \      \
#             /     |       |    \      \
#            /      |       |     \      \
#           /       |       |      \      \
#          /        |       |       \      \
#     search      info   download  quit    name_scheme
#         |                 |        |         |
#    user_input_3     read resuls   exit  user_input_2
#       /    \                              /      \
#   mass    specific                      add   remove
#      \      /                             \      /
#     dump results                      dump name_scheme
# ==============================================================
# ==============================================================

def main():
    console = Console()

    # Loads in all the paths for the script
    #   working_path = current cwd
    #   script_path = where spd.py is located
    #   name_scheme_path = where comet_names.yaml should be located
    #   info_path = where INFO.md should be located
    working_path = os.getcwd()
    script_path = pathlib.Path(__file__).parent.resolve()
    name_scheme_path = f'{script_path}/comet_names.yaml'
    info_path = f'{script_path}/INFO.md'

    # Loads and reads config
    # Throws errors if 
    #       -the file doesn't exist in working_path
    #       -the file doesn't have download_path and dtype_list
    # Will read in obs_list_path if exist (defaults to working_path if not)
    if (os.path.isfile(f'{working_path}/config.yaml') == False):
        console.print("[red]Unable to find [/][magenta][bold]config.yaml[/][/][red] file in current directory.[/]")
        return
    with open(f'{working_path}/config.yaml', 'r') as file:
        config = yaml.safe_load(file)

        try:
            download_path = config['download_path']
            dtype_list = config['dtype_list'] 
        except (KeyError, TypeError):
            console.print("Unable to read [magenta][bold]config.yaml[/][/] file in current directory.", style="red")
            return

        try:
            obs_list_path = config['obs_list_path']
        except (KeyError, TypeError):
            obs_list_path = working_path

    file.close()

    # Test to see if download_path is actually a path
    if (os.path.isdir(f"{download_path}") == False):
        console.print("Unable to reconize download path in [magenta][bold]config.yaml[/][/] file.", style="red")
        return

    # Adds new name scheme if for some reason it does not exist currently
    if (os.path.isfile(f"{name_scheme_path}") == False):
        new_scheme = open(f"{name_scheme_path}", 'w')
        new_scheme.close()

    console.clear()

    # Entering level 1 of the menu:
    #   -Search
    #   -Download
    #   -Name_scheme
    #   -Info
    #   -Quit

    while (True):

        console.print(f"\n[underline][green][bold]Swift Dead Portal Downloader[/][/][/]\n", justify='center')
        console.print(f"\t[cyan]0[/]\tSearch and generate observation list\n\t[cyan]1[/]\tDownload results\n\t[cyan]n[/]\tView/edit manual naming scheme\n\t[cyan]i[/]\tInformation\n\t[cyan]q[/]\tQuit program")
        user_input_1 = input()

        if (user_input_1 == 'q'): # LEVEL 1: User selected quit
            return

        elif (user_input_1 == 'i'): # LEVEL 1: User selected info
            
            # Test to see if INFO.md is missing or not
            if (os.path.isfile(f'{info_path}') == False):
                console.print(f"Unable to reconize INFO.md file in [magenta][bold]{script_path}[/][/]", style="red")
            
            # Will read INFO.md and display it to the console()
            else:
                with open(f"{info_path}") as md:
                    markdown = Markdown(md.read())
                    console.print(markdown)
                md.close()
        
        elif (user_input_1 == 'n'): # LEVEL 1: User selected name_scheme
            console.clear()

            # Entering level 2 of the menu:
            #   -Add
            #   -Remove
            #   -Return

            while(True):
                # Loads in and prints current name scheme
                with open(f'{name_scheme_path}', 'r') as file:
                    name_scheme = yaml.safe_load(file)
                file.close() 
                console.print(f"\n[underline][yellow][bold]Name Scheme[/][/][/]", justify='center')
                print_name_scheme(name_scheme)

                console.print(f"\n\t[magenta]0[/]\tAdd element to naming scheme\n\t[magenta]1[/]\tRemove element from naming scheme\n\t[magenta]q[/]\tReturn to previous menu")
                user_input_2 = input()

                if(user_input_2 == 'q'): # LEVEL 2: User selected return to level 1, break out of level 2
                    console.clear()
                    break

                elif(user_input_2 == '0'): # LEVEL 2: User selected add new names
                    print()

                    # Strip any whitespace before the name (makes copy and paste from name_scheme easier)
                    new_sw_name = input("Enter new swift portal name: ")
                    new_cv_name = input("Enter new convectional name: ")
                    stripped_sw = new_sw_name.strip()
                    stripped_cv = new_cv_name.strip()

                    while(True): # Entering confirm addition level
                        console.print(f"Confirm addition of [cyan]{stripped_sw}[/] to be renamed to [bright_green]{stripped_cv}[/]\n\t[cyan]y[/]\tConfirm\n\t[cyan]n[/]\tCancel and return to previous menu")
                        confirm_add = input()

                        if (confirm_add == 'n'):
                            break

                        elif (confirm_add == 'y'):
                            manual_add_name(swift_name=stripped_sw, conventional_name=stripped_cv, name_scheme=name_scheme, name_scheme_path=name_scheme_path)
                            break

                    continue

                elif(user_input_2 == '1'): # LEVEL 2: User selected remove name
                    print()

                    # Strip any whitespace before the name (makes copy and paste from name_scheme easier)
                    sw_name = input("Enter swift portal name to be removed: ")
                    stripped_sw = sw_name.strip()

                    # Test to see if the name actually already exist
                    if sw_name in name_scheme:
                        while(True): # Entering confirm removal level

                            console.print(f"Confirm removal of [cyan]{stripped_sw}[/]\n\t[cyan]y[/]\tConfirm\n\t[cyan]n[/]\tCancel and return to previous menu")
                            confirm_remove = input()

                            if (confirm_remove == 'n'):
                                break

                            elif (confirm_remove == 'y'):
                                manual_remove_name(swift_name=stripped_sw, name_scheme=name_scheme, name_scheme_path=name_scheme_path)
                                break

                    else:
                        console.print(f"Unable to reconize swift portal name [cyan][bold]{sw_name}[/][/]", style="red")

                    continue
                continue

        elif (user_input_1 == '0'): # LEVEL 1: User selected search
            console.clear()

            # Entering level 2 of the menu:
            #   -Mass search
            #   -Specific search

            while(True):
                console.print(f"\n[underline][red][bold]Search Options[/][/][/]\n", justify='center')
                console.print(f"\t[blue]0[/]\tMass search for comets\n\t[blue]1[/]\tSearch portal for specific query\n\t[blue]q[/]\tReturn to previous menu")
                user_input_3 = input()

                if (user_input_3 == 'q'): # LEVEL 2: User selected to return to level 1, break out of level 2
                    console.clear()
                    break

                elif (user_input_3 == '0'): # LEVEL 2: User selected mass search
                    search_terms = {"Comet", "P/", "C/"} 
                    
                    tlist = mass_search(search_terms=search_terms, name_scheme_path=name_scheme_path)
                    
                    # Dumping the finalized converted list to a pandas df -> csv to obs_list_path
                    dump_dataframe(tlist=tlist, output_path=obs_list_path, working_path=working_path)
                    break

                elif (user_input_3 == '1'): # LEVEL 2: User selected specific search term
                    search_term = input(f"\nSearch term (press q to return to main menu): ")

                    if (search_term == 'q'): # LEVEL 2: Search term specified to return to level 1, breaking out of level 2
                        console.clear()
                        break
                    
                    # Determing how many results 0, 1, or 2+ as the html of the page is different for these three cases
                    page_html, search_soup = search_page(search_term=search_term)
                    num_of_results = results_type(search_soup=search_soup) 

                    if (num_of_results == '0'): # No results found
                        console.print(f"No results found for [magenta]{search_term}[/].", style="cyan")
                        break

                    elif (num_of_results == '1'): # Only 1 results found
                        search_results = get_single_tlist(search_soup=search_soup)
                        console.print('Converting target names[cyan] ...[/]', style="cyan")

                        # Converting both swift name -> conventional name and tids -> list[obsids]
                        tlist = [(convert_tid_to_obsid(tid=search_results[1]), rename_comet_name(comet_name=search_results[0], name_scheme_path=name_scheme_path))] 

                    else: # 2+ results (following same code structure as mass search)
                        search_results = get_multi_tlists(search_soup=search_soup) 
                        tlist = convert_list_multi(tlist=search_results, name_scheme_path=name_scheme_path)

                    # Dumping the finalized converted list to a pandas df -> csv to obs_list_path
                    dump_dataframe(tlist=tlist, output_path=obs_list_path, working_path=working_path)
                    break

        elif (user_input_1 == '1'): # LEVEl 1: User selected download

            # Test to see if the results csv is in the obs_list_path, throws error if not
            if (os.path.isfile(f'{obs_list_path}/portal_search_results.csv') == False):
                if (obs_list_path == working_path):
                    console.print("\n[red]Unable to find [/][magenta][bold]portal_search_results.csv[/][/][red] file in current directory.\nGenerate it using [/][magenta][bold]Search and generate observation list[/][/][red] option.")
                else:
                     console.print(f"\n[red]Unable to find [/][magenta][bold]portal_search_results.csv[/][/][red] file in [/][magenta][bold]{obs_list_path}.\nGenerate it using [/][magenta][bold]Search and generate observation list[/][/][red] option.")
                continue

            # Converts results.csv -> pandas df -> list
            df = pd.read_csv(f'{obs_list_path}/portal_search_results.csv')
            df_list = df.values.tolist()

            # Pulls out all obsids as a list['obsids']
            tlist = [(ast.literal_eval(obsids), tname) for (i, obsids, tname) in df_list]
            console.print(f'\nSucessfully loaded [magenta][bold]portal_search_results.csv[/][/] and found [cyan][bold]{len(tlist)}[/][/] [bright_white]target id(s).[/]')

            while (True): # Entering confirmation level
                console.print(f'\n[green]Confirm download to:[/] [magenta]{download_path}[/]\n\t[cyan]y[/]\tConfirm\n\t[cyan]n[/]\tCancel and return to main menu')
                confirm_download = input()

                if (confirm_download == 'y'):
                    
                    # Remove any dirs with numeric names
                    console.print(f"\nRemoving incomplete downloads[cyan] ...[/]", style="cyan")
                    remove_incomplete_downloads(download_path=download_path, working_path=working_path)

                    # Add all conventionals names to download directory (ie: download_path/conventional_name)
                    console.print("Preparing download directory[cyan] ...[/]", style="cyan")
                    prepare_download_dir(tlist=tlist, download_path=download_path)

                    # Download files
                    console.print("Beginning download[cyan] ...[/]\n", style="cyan")
                    download_files(tlist=tlist, dtype_list=dtype_list, dest_dir=download_path)
                    
                    console.print(f'\nDownload finished', style="cyan")
                    break

                elif (confirm_download == 'n'):
                    console.clear()
                    break

if __name__ == "__main__":
    sys.exit(main())
