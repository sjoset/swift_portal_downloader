import os
import shutil

name_conversion = {}

def convert_names(t_list: str):
    converted_t_list = []
    for (t_id, t_name) in t_list:
        if t_name in name_conversion:
            new_name = name_conversion[f'{t_name}']
            t_elem = (t_id, new_name)
            converted_t_list.append(t_elem)
    return t_list

def search_download_dir(t_list: str, download_path: str):
    parent_dirs = [dir for dir in os.list_dir(download_path) if os.path.isdir(dir)]
    all_sub_dirs = []
    for par_dir in parent_dirs:
        sub_dirs = [sub_dir for sub_dir in os.list_dir(par_dir) if os.path.isdir(sub_dir)]
        all_sub_dirs.append(sub_dirs)
    spliced_t_list = []
    duplicates = 0
    for (t_id, t_name) in t_list:
        if (t_id in all_sub_dirs):
            duplicates += 1
        else:
            t_elem = (t_id, t_name)
            spliced_t_list.append(t_elem)
    new_data = len(spliced_t_list)
    return (new_data, duplicates, spliced_t_list)

def merge_download_files(t_name: str, t_id: str, download_path: str):
    return

def remove_incomplete_downloads(download_path: str):
    dirs = [dir for dir in os.list_dir(download_path) if os.path.isdir(dir)]
    for dir in dirs:
        if dir.isnumeric():
            shutil.rmtree(f"{download_path}/{dir}")
    return
