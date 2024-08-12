from rich.progress import track
from typing import List

import pathlib
import subprocess
import os
import shutil

# swift_dead_portal_downloader.py

# Program to manage the download of all results found in tlist


# # Function to generate the wget commands needed to download the script from the portal
# def get_swift_wget_commands(obsid: str, dtype: str, overwrite: bool) -> List[str]:
#
#     # wget commands:
#     #   -nc -> no clobber: don't replace already downloaded files
#     #   -q -> quiet mode, no output
#     #   -w 2 -> wait 2 seconds between files
#     #   -nH -> don't create a directory based on the host, in this case no folder named www.swift.ac.uk/
#     #   --cut-dirs=2 -> remove the /archive/reproc/ folders on the server from being created locally
#     #   -r -> recursive: grab everything under this folder on the server
#     #   --reject ... -> specify files that we don't want from the server
#
#     if overwrite is False:
#         overwrite_option = "-nc"
#     else:
#         overwrite_option = ""
#     wget_command = (
#         "wget "
#         + overwrite_option
#         + f" -q -w 2 -nH --cut-dirs=2 -r --no-parent --reject index.html*,robots.txt*  http://www.swift.ac.uk/archive/reproc/{obsid}/{dtype}/"
#     )
#     return wget_command


# # Function to download a single type of data for single obsid
# def swift_download_uncompressed(
#     obsid: str, tname: str, dtype: str, dest_dir: pathlib.Path | None = None
# ) -> None:
#
#     # Get our download commands from the server
#     wget_command = get_swift_wget_commands(obsid, dtype, overwrite=False)
#     working_path = os.getcwd()
#     if dest_dir is not None:
#         os.chdir(dest_dir)
#     if os.path.isdir(f"{os.getcwd()}/{tname}/{obsid}/{dtype}") == True:
#         return
#     presult = subprocess.run(wget_command.split())
#     if presult.returncode != 0:
#         return
#
#     # change folders back to working directory
#     os.chdir(working_path)
#
#     # Moves the downloaded result to its final location
#     if os.path.isdir(
#         f"{dest_dir}/{tname}/{obsid}"
#     ):  # if there is already data for the given obsid in dest_dir
#
#         # Move the dtype folder's parent to be the current obsid folder
#         # ie: dest_dir/obsid/dtype/... -> dest_dir/canonical_name/obsid/dtype/...
#         shutil.move(
#             f"{dest_dir}/{obsid}/{dtype}",
#             f"{dest_dir}/{tname}/{obsid}",
#             copy_function=shutil.copytree,
#         )
#
#         # Delete the new empty dir
#         shutil.rmtree(f"{dest_dir}/{obsid}/")
#
#     else:  # if there is not any data found for the given obsid in dest_dir
#
#         # Move the dtype folder's parent to be the canonical_name
#         # ie: dest_dir/obsid/dtype/... -> dest_dir/canonical_name/obsid/dtype/...
#         shutil.move(
#             f"{dest_dir}/{obsid}", f"{dest_dir}/{tname}", copy_function=shutil.copytree
#         )


# # Function to download data in dtype_list for all obsids found in tlist
# # Only uncompressed downloads work at this time
# def download_files(tlist: str, dtype_list: str, dest_dir: pathlib.Path) -> None:
#
#     # Iterates through tlist which has [(list['obsid'], canonical_name), ...]
#     # Will download all dtypes specified in dtype_list for a single obsid before moving on to the next
#     for obsids_list, tname in tlist:
#         for obsid in track(
#             obsids_list,
#             description=f"[cyan]Downloading target id[/] [magenta]{obsids_list[0][0:8]}[/][/][cyan] ...[/]",
#         ):
#             for dtype in dtype_list:
#                 swift_download_uncompressed(
#                     obsid=obsid, tname=tname, dtype=dtype, dest_dir=dest_dir
#                 )
