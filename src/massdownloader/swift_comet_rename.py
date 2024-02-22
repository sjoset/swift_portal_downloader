import re
import yaml
from rich.console import Console

from typing import List, Optional

def match_long_period_name(comet_name: str) -> Optional[str]:
    """Searches comet_name for anything resembling a long-period comet naming convention"""
    # match naming convention of long period comets: C/[YEAR][one optional space character][one to two letters][one to two digits]
    long_period_match = re.search("C/[0-9]{4}\\s?[A-Z]{1,2}[0-9]{1,2}", comet_name)
    if long_period_match:
        # get the matched part of the string if there was a match
        long_period_name = long_period_match.group() if long_period_match else None
    else:
        # try the same match but instead of "C/...", look for "Comet..."
        long_period_match = re.search(
            "Comet[0-9]{4}\\s?[A-Z]{1,2}[0-9]{1,2}", comet_name
        )
        if long_period_match:
            long_period_name = re.sub("Comet", "C/", long_period_match.group())
        else:
            long_period_name = None

    return long_period_name


def match_short_period_name(comet_name: str) -> Optional[str]:
    """Searches comet_name for anything resembling a short-period comet naming convention"""
    # try to find  P/[YEAR][one to two characters][one to three numbers]
    short_period_match = re.search("P/[0-9]{4}[A-Z]{1,2}[0-9]{1,3}", comet_name)
    if short_period_match:
        short_period_name = short_period_match.group() if short_period_match else None
    else:
        # match naming convention of short period comets: [1 to 3 digits]P
        short_period_match = re.search("[0-9]{1,3}P", comet_name)
        if short_period_match:
            short_period_name = short_period_match.group()
        else:
            short_period_name = None

    return short_period_name

def manual_fix(comet_name: str, name_schemes_path: str) -> str:
    with open(f'{name_schemes_path}', 'r') as file:
        name_scheme = yaml.safe_load(file)
    file.close()
    if comet_name in name_scheme:
        proper_name = name_scheme[f'{comet_name}']
    else:
        return add_new_name(comet_name, name_scheme)
    return proper_name

def add_new_name(comet_name: str, name_scheme: dict) -> str:
    console = Console()
    console.print(f"Unable to classify [magenta]'{comet_name}'[/] observation name from the swift portal.", style='cyan')
    proper_name = input("Enter the correct conventional name for this observation: \n")
    name_scheme[f'{comet_name}'] = proper_name
    with open('comet_names.yaml', 'w') as file:
        yaml_output=yaml.dump(name_scheme, file)
    return proper_name

def rename_comet_name(comet_name: str, name_schemes_path: str) -> str: 
    long_name=match_long_period_name(comet_name)
    if (long_name != None):
        return long_name.replace('/', '_')    
    short_name=match_short_period_name(comet_name)
    if (short_name != None):
        return short_name.replace('/', '_')
    else:
        name = manual_fix(comet_name, name_schemes_path)
        return name.replace('/', '_')
