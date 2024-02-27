from rich.console import Console
from typing import List, Optional

import re
import yaml
import pathlib

# swift_comet_rename.py

# Program to manage the conversion of the swift name to the conventional name

# Function to match comet_names that contain C/ or Comet#### formatting
def match_long_period_name(comet_name: str) -> Optional[str]:
    """Searches comet_name for anything resembling a long-period comet naming convention"""
    
    # Match naming convention of long period comets: C/[YEAR][one optional space character][one to two letters][one to two digits]
    long_period_match = re.search("C/[0-9]{4}\\s?[A-Z]{1,2}[0-9]{1,2}", comet_name)
    if long_period_match:

        # Get the matched part of the string if there was a match
        long_period_name = long_period_match.group() if long_period_match else None
    else:

        # Try the same match but instead of "C/...", look for "Comet..."
        long_period_match = re.search("Comet[0-9]{4}\\s?[A-Z]{1,2}[0-9]{1,2}", comet_name)
        if long_period_match:
            long_period_name = re.sub("Comet", "C/", long_period_match.group())

        else:
            long_period_name = None

    return long_period_name

# Function to match comet_names that contain P/ or ##P formatting
def match_short_period_name(comet_name: str) -> Optional[str]:
    """Searches comet_name for anything resembling a short-period comet naming convention"""
    
    # Try to find P/[YEAR][one to two characters][one to three numbers]
    short_period_match = re.search("P/[0-9]{4}[A-Z]{1,2}[0-9]{1,3}", comet_name)
    if short_period_match:
        short_period_name = short_period_match.group() if short_period_match else None

    else:

        # Match naming convention of short period comets: [1 to 3 digits]P
        short_period_match = re.search("[0-9]{1,3}P", comet_name)
        if short_period_match:
            short_period_name = short_period_match.group()

        else:
            short_period_name = None

    return short_period_name

# Function to match comet_names that can be found in the name_scheme
def manual_fix(comet_name: str, name_scheme_path: pathlib.Path) -> str:
    with open(f'{name_scheme_path}', 'r') as file:
        name_scheme = yaml.safe_load(file)
    file.close()
    if comet_name in name_scheme: # Name found in current name_scheme (no overwrite needed)
        proper_name = name_scheme[f'{comet_name}']

    else: # Name not found in current name_scheme, addition and overwrite required
        return add_new_name(comet_name=comet_name, name_scheme=name_scheme, name_scheme_path=name_scheme_path)

    return proper_name

# Function to add to and overwrite the current name_scheme
def add_new_name(comet_name: str, name_scheme: dict, name_scheme_path: pathlib.Path) -> str:
    console = Console()

    # Requst conventional_name from user and add name
    console.print(f"Unable to classify [magenta]'{comet_name}'[/] observation name from the swift portal.", style='cyan')
    proper_name = input("Enter the correct conventional name for this observation: \n")
    name_scheme[f'{comet_name}'] = proper_name

    # Overwrite current name_scheme
    with open(f'{name_scheme_path}', 'w') as file:
        yaml_output=yaml.dump(name_scheme, file)
    file.close()

    return proper_name

# Function to match a given comet_name to a conventional_name
# This method will always return the conventional_name as a string
def rename_comet_name(comet_name: str, name_scheme_path: pathlib.Path) -> str: 
    
    # Replace all conventional_names / with _ for when we format our download_dir 
    long_name=match_long_period_name(comet_name=comet_name)
    if (long_name != None):
        return long_name.replace('/', '_') 

    short_name=match_short_period_name(comet_name=comet_name)
    if (short_name != None):
        return short_name.replace('/', '_')

    else:
        name = manual_fix(comet_name=comet_name, name_scheme_path=name_scheme_path)
        return name.replace('/', '_')
