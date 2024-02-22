import os
import shutil

def prepare_download_dir(tlist: str, download_path: str):
    tnames = [tname for (tid, tname) in tlist]
    for dir_name in tnames:
        if os.path.exists(f'{download_path}/{dir_name}'):
            pass
        else:
            os.mkdir(f'{download_path}/{dir_name}')
    return

def remove_incomplete_downloads(download_path: str, working_path: str):
    os.chdir(download_path)
    dirs = [dir for dir in os.listdir() if os.path.isdir(dir)] 
    for dir in dirs:
        if dir.isnumeric():
            shutil.rmtree(f"{download_path}/{dir}")
    os.chdir(working_path)
    return
