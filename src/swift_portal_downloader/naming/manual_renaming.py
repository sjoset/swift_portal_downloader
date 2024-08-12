import pathlib
import yaml

from rich.console import Console

from swift_portal_downloader.naming.canonical_comet_name import CanonicalCometName
from swift_portal_downloader.naming.manual_renaming_scheme import (
    get_internal_renaming_scheme,
)
from swift_portal_downloader.swift.swift_target_name import SwiftTargetName


# TODO: we need a userspace renaming file because we can't update the internal package .yaml file


# When extracting the canonical comet name fails, we may have to fall back to looking up the canonical names of a few known cases
# of odd swift_target_names
# These mappings from swift_target_name -> CanonicalCometName were produced manually when initially examining the SWIFT data set
# and are stored internally in swift
def manual_canonical_name_lookup(
    swift_target_name: SwiftTargetName,
) -> CanonicalCometName:

    # # TODO: this should only check the internal and external renaming schemes, and return None if not found - ask for user input elsewhere?
    internal_renaming_scheme = get_internal_renaming_scheme()

    if swift_target_name in internal_renaming_scheme:
        canonical_name = internal_renaming_scheme[f"{swift_target_name}"]
        # TODO: elif target in user_defined_renaming_scheme:
    else:
        # Name not found in any manual renaming scheme, ask user for canonical name
        # canonical_name = add_new_canonical_name_lookup_entry(
        #     swift_target_name=swift_target_name,
        #     name_scheme=internal_renaming_scheme,
        #     name_scheme_path=name_scheme_path,
        # )
        # TODO:
        print("Not asking for manual fix, but we should do that here!")
        canonical_name = CanonicalCometName("fixme")

    return canonical_name


# Function to add to and overwrite the current name_scheme
# TODO: this should add entry to a .yaml file in the current working directory
def add_new_canonical_name_lookup_entry(
    swift_target_name: SwiftTargetName,
    name_scheme: dict,
    name_scheme_path: pathlib.Path,
) -> CanonicalCometName:
    console = Console()

    # Requst canonical name from user and add name
    console.print(
        f"Unable to classify [magenta]'{swift_target_name}'[/] observation name from the swift portal.",
        style="cyan",
    )
    canonical_name = input("Enter the correct canonical name for this observation: \n")
    # TODO: fix dict addressing by removing f-string
    name_scheme[f"{swift_target_name}"] = canonical_name

    # Overwrite current name_scheme
    with open(f"{name_scheme_path}", "w") as file:
        yaml.dump(name_scheme, file)
    file.close()

    return canonical_name
