from rich.console import Console
from rich.table import Table

import os
import shutil
import yaml

# swift_utils.py

# Utility program for spd.py

# Function to add all tnames in tlist to download_path as a sub directories
# ie: download_path/tname/...
def prepare_download_dir(tlist: str, download_path: str) -> None:
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
# interrupted and incomplete.
def remove_incomplete_downloads(download_path: str, working_path: str):
    os.chdir(download_path)
    dirs = [dir for dir in os.listdir() if os.path.isdir(dir)] 
    for dir in dirs:
        if dir.isnumeric():
            shutil.rmtree(f"{download_path}/{dir}")
    os.chdir(working_path)
    return

# Function to print the current name_scheme dict using a rich table
def print_name_scheme(name_scheme: dict) -> None:
    console=Console()
    table=Table(title='')
    table.add_column("Swift Portal Name", style='cyan')
    table.add_column("Conventional Name", style='bright_green') 
    for (swift_name, conventional_name) in name_scheme.items():
        table.add_row(swift_name,conventional_name)
    print()
    console.print(table)
    return

# Function to add a new name to the name scheme and overwrite the current one
# The entry will be as follows, 'swift_name': 'conventional_name'
def manual_add_name(swift_name: str, conventional_name: str, name_scheme: dict, name_schemes_path: str) -> None:
    name_scheme[f'{swift_name}'] = conventional_name 
    with open(f'{name_schemes_path}', 'w') as file:
        yaml_output=yaml.dump(name_scheme, file)
    file.close()
    return

# Function to remove a name from the current name scheme and overwrite the current one
def manual_remove_name(swift_name: str, name_scheme: dict, name_schemes_path: str) -> None:
    del name_scheme[f'{swift_name}']
    with open(f'{name_schemes_path}', 'w') as file:
        yaml_output=yaml.dump(name_scheme, file)
    file.close()
    return
