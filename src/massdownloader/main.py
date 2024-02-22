from .swift_dead_portal_search import search_page, get_multi_tlists, get_single_tlist, results_type, convert_tid_to_obsid
from .swift_dead_portal_downloader import download_files
from .swift_utils import prepare_download_dir, remove_incomplete_downloads
from .swift_comet_rename import rename_comet_name

from rich.console import Console
from rich.progress import track

import os
import yaml
import pandas as pd
import ast

def main():
    console = Console()
    working_path = os.getcwd()
    if (os.path.isfile(f'{working_path}/config.yaml') == False):
        console.print("[red]Unable to find [/][magenta][bold]config.yaml[/][/][red] file in current directory.[/]")
        return
    with open(f'{working_path}/config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        try:
            download_path = config['download_path']
            dtype_list = config['dtype_list']
            comet_names_path = config['comet_names_file_path']
            if (os.path.isfile(comet_names_path) == False):
                console.print("Unable to find [magenta][bold]comet_names.yaml[/][/] file.", style="red")
                return
        except (KeyError, TypeError):
            console.print("Unable to read [magenta][bold]config.yaml[/][/] file in current directory.", style="red")
            return
    file.close()  
    if (os.path.isdir(f"{download_path}") == False):
        console.print("Unable to reconize download path in [magenta][bold]config.yaml[/][/] file.", style="red")
        return
    while (True):
        console.print(f"\n[underline][green]Select option[/][/]\n\t[cyan]0[/]\tSearch and generate observation list\n\t[cyan]1[/]\tDownload results\n\t[cyan]q[/]\tQuit")
        user_input_1 = input()
        if (user_input_1 == 'q'):
            return  
        if (user_input_1 == '0'):
            console.print(f"\n[underline][green]Select option[/][/]\n\t[cyan]0[/]\tGrab all comet results\n\t[cyan]1[/]\tSearch portal for specific query\n\t[cyan]q[/]\tReturn to previous menu")
            while(True):
                user_input_2 = input()
                if (user_input_2 == 'q'):
                    continue
                elif (user_input_2 == '0'): 
                    search_terms = {"Comet", "P/", "C/"} 
                    results = []
                    print()
                    for term in track(search_terms, description="[cyan]Searching portal...[/]"):
                        page_html, search_soup = search_page(search_term = term)
                        tlist = get_multi_tlists(search_term = term, search_soup = search_soup)
                        results.append(tlist)
                    full_results = results[0] + results[1] + results[2]
                    condensed_list = set(full_results)
                    console.print('Converting target names[cyan]...[/]', style="cyan")
                    new_name_list = [(tid, rename_comet_name(tname, comet_names_path)) for (tid, tname) in condensed_list]
                    converted_list = [(convert_tid_to_obsid(tid), convectional_name) for (tid, convectional_name) in track(new_name_list, description="[cyan]Generating observation ids...[/]")] 
                elif (user_input_2 == '1'):
                    search_term = input(f"\nSearch term (press q to return to previous menu): ")
                    if (search_term == 'q'):
                        continue
                    page_html, search_soup = search_page(search_term = search_term)
                    num_of_results = results_type(search_soup = search_soup) 
                    if (num_of_results == '0'):
                        console.print(f"No results found for [magenta]{search_term}[/].", style="cyan")
                        break
                    elif (num_of_results == '1'):
                        tlist = get_single_tlist(search_term = search_term, search_soup = search_soup)
                        converted_list=[(convert_tid_to_obsid(tlist[1]), rename_comet_name(tlist[0], comet_names_path))] 
                    else:
                        tlist = get_multi_tlists(search_term = search_term, search_soup = search_soup) 
                        console.print('Converting target names[cyan]...[/]', style="cyan")
                        new_name_list = [(tid, rename_comet_name(tname, comet_names_path)) for (tid, tname) in tlist]
                        converted_list = [(convert_tid_to_obsid(tid), convectional_name) for (tid, convectional_name) in track(new_name_list, description="[cyan]Generating observation ids...[/]")] 
                console.print(f'Found [bold][cyan]{len(converted_list)}[/][/] [bright_white]target id(s)[/] from the portal.\nDumping search results to [bold][magenta]portal_search_results.csv[/][/] to current directory.') 
                df = pd.DataFrame(converted_list) 
                df.columns = ['Observation id(s)', 'Convectional name']
                df.to_csv(r"portal_search_results.csv")
                break

        if (user_input_1 == '1'):
            if (os.path.isfile(f'{working_path}/portal_search_results.csv') == False):
                console.print("\n[red]Unable to find [/][magenta][bold]portal_search_results.csv[/][/][red] file in current directory.\nGenerate it using [/][magenta][bold]Search and generate observation list[/][/][red] option.")
                continue
            df=pd.read_csv(f'{working_path}/portal_search_results.csv')
            df_list=df.values.tolist()
            tlist=[(ast.literal_eval(obsids), tname) for (i, obsids, tname) in df_list]
            console.print(f'\nSucessfully loaded [magenta][bold]portal_search_results.csv[/][/] and found [cyan][bold]{len(tlist)}[/][/] [bright_white]target id(s).[/]')
            while (True):
                console.print(f'\n[green]Confirm download to:[/] [magenta]{download_path}[/]\n\t[cyan]y[/]\tConfirm\n\t[cyan]n[/]\tCancel and return to main menu')
                confirm_download = input()
                if (confirm_download == 'y'):
                    console.print(f"\nRemoving incomplete downloads[cyan]...[/]", style="cyan")
                    remove_incomplete_downloads(download_path=download_path, working_path=working_path)
                    console.print("Preparing download directory[cyan]...[/]", style="cyan")
                    prepare_download_dir(tlist, download_path)
                    console.print("Beginning download[cyan]...[/]\n", style="cyan")
                    download_files(tlist=tlist, dtype_list=dtype_list, dest_dir=download_path)
                    console.print(f'\nDownload finished', style="cyan")
                    break
                elif (confirm_download == 'n'):
                    console.print(f'\nDownload canceled', style="cyan")
                    break

if __name__ == "__main__":
    sys.exit(main())
