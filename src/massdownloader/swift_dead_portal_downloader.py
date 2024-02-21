from .swift_utils import merge_download_files
import pathlib
import requests
import subprocess
import os
import shutil
from typing import List, Tuple
import tqdm

def get_swift_wget_commands(tid: str, dtype: str, overwrite: bool) -> List[str]:

    if overwrite is False:
        overwrite_option = '-nc'
    else:
        overwrite_option = ''
    wget_command = 'wget ' + overwrite_option + f' -q -w 2 -nH --cut-dirs=2 -r --no-parent --reject index.html*,robots.txt*  http://www.swift.ac.uk/archive/reproc/{tid}/{dtype}/'
    return wget_command

def swift_download_uncompressed(tid: str, tname:str, dtype: str, dest_dir: pathlib.Path = None) -> None:
    
    # given a Swift target id and type of data, this function downloads the uncompressed
    # data to the directory dest_dir
    
    # get our download commands from the server
    wget_command = get_swift_wget_commands(tid, dtype, overwrite=False)
    old_cwd = os.getcwd()
    if dest_dir is not None:
        os.chdir(dest_dir)
    if (os.path.isdir(f'{os.getcwd()}/{tname}/{tid}/{dtype}') == True):
        return 
    presult = subprocess.run(wget_command.split())
    if presult.returncode != 0:
        return

    # change folders back
    os.chdir(old_cwd)

    if(os.path.isdir(f'{dest_dir}/{tname}/{tid}')):
        shutil.move(f'{dest_dir}/{tid}/{dtype}', f'{dest_dir}/{tname}/{tid}', copy_function = shutil.copytree)
        shutil.rmtree(f'{dest_dir}/{tid}/')
    else:
        shutil.move(f'{dest_dir}/{tid}', f'{dest_dir}/{tname}', copy_function = shutil.copytree)
    
def download_files(tlist: str, dtype_list: str, dest_dir: str) -> None:
    # downloads the files for 2+ results when searching
    # iterates over each requested data type and observation collected from get_multi_tlists()
    for obsid, t_name in tqdm.tqdm(tlist, desc="Target id(s)"):
        for t_id in obsid:
            for dtype in dtype_list: 
                swift_download_uncompressed(tid=t_id, tname=t_name, dtype=dtype, dest_dir=dest_dir)
                
