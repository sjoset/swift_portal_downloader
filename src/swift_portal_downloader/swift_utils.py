from rich.console import Console
from rich.table import Table

import os
import shutil
import yaml
import pathlib
import pandas as pd

# swift_utils.py

# Utility program for the repo
# ie: a bunch of miscellaneous functions

# Function to add all tnames in tlist to download_path as a sub directories
# ie: download_path/tname/...
def prepare_download_dir(tlist: str, download_path: pathlib.Path) -> None:
    tnames = [tname for (tid, tname) in tlist]
    for dir_name in tnames:
        if os.path.exists(f'{download_path}/{dir_name}'):
            pass
        else:
            os.mkdir(f'{download_path}/{dir_name}')
    return

# Function to remove any sub dir numeric (dir with just ##### in the name) from download_path
#
# When the portal downloads a file as uncompressed, it will be named with the obsid by wget,
# thus any directory that is not renamed by swift_dead_portal_downloader.py was prematurely 
# interrupted and therefore incomplete.
#
# This will remove the directory plus recursively remove all child directories
def remove_incomplete_downloads(download_path: pathlib.Path, working_path: pathlib.Path) -> None:
    os.chdir(download_path)
    dirs = [dir for dir in os.listdir() if os.path.isdir(dir)] 
    for dir in dirs:
        if dir.isnumeric():
            shutil.rmtree(f"{download_path}/{dir}")
    os.chdir(working_path)
    return

# Function to print the current name_scheme dict using a rich table
def print_name_scheme(name_scheme: dict) -> None:
    
    console = Console()

    # Creates table headings
    table = Table(title='')
    table.add_column("Swift Portal Name", style='cyan')
    table.add_column("Conventional Name", style='bright_green')

    # Adds all table elements
    for (swift_name, conventional_name) in name_scheme.items():
        table.add_row(swift_name,conventional_name)
    print()

    console.print(table)
    return

# Function to add a new name to the name scheme and overwrite the current one
# The entry will be as follows, 'swift_name': 'conventional_name'
def manual_add_name(swift_name: str, conventional_name: str, name_scheme: dict, name_scheme_path: pathlib.Path) -> None:
    name_scheme[f'{swift_name}'] = conventional_name 
    dump_yaml(dict_to_dump=name_scheme, output_path=name_scheme_path)
    return

# Function to remove a name from the current name scheme and overwrite the current one
def manual_remove_name(swift_name: str, name_scheme: dict, name_scheme_path: pathlib.Path) -> None:
    del name_scheme[f'{swift_name}']
    dump_yaml(dict_to_dump=name_scheme, output_path=name_scheme_path)
    return

# Function to dump a dictionary to a yaml file
# output_path will contain the file name
def dump_yaml(dict_to_dump: dict, output_path: pathlib.Path) -> None:
    with open(f'{output_path}', 'w') as file:
        yaml_output=yaml.dump(dict_to_dump, file)
    file.close()
    return

# Function to dump a tlist -> pd dataframe -> csv
def dump_dataframe(tlist: str, output_path: pathlib.Path, working_path: pathlib.Path) -> None:
    console = Console()
    if (output_path == working_path):
        console.print(f'Found [bold][cyan]{len(tlist)}[/][/] [bright_white]target id(s)[/] from the portal.\nDumping search results to [bold][magenta]portal_search_results.csv[/][/] to current directory.')
    else:
        console.print(f'Found [bold][cyan]{len(tlist)}[/][/] [bright_white]target id(s)[/] from the portal.\nDumping search results to [bold][magenta]portal_search_results.csv[/][/] to [bold][magenta]{output_path}[/][/].') 

    # Creates the dataframe and dumps to csv
    df = pd.DataFrame(tlist) 
    df.columns = ['Observation id(s)', 'Conventional name']
    df.to_csv(f"{output_path}/portal_search_results.csv")
    return
