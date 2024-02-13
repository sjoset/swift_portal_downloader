def get_swift_wget_commands(tid: str, dtype: str, overwrite: bool) -> List[str]:

    # for any given target id, there may be multiple observations in their own directories,
    # with the naming scheme {target id}001/, {target id}002/, etc.
    # so we let the server give us the appropriate wget commands because it knows how
    # many observations each target id has
    
    if overwrite is False:
        overwrite_option = '-nc'
    else:
        overwrite_option = ''
        
    # this page returns a script with wget commands to download our data
    base_wget_url = f'https://www.swift.ac.uk/archive/download.sh?reproc=1&tid={tid}&source=obs&subdir={dtype}'
    wget_response = requests.get(base_wget_url)
    wget_commands = [line for line in wget_response.text.splitlines() if 'wget' in line]
    urls = [command.split()[-1] for command in wget_commands]
    
    # -nc ==> no clobber: don't replace already downloaded files
    # -q ==> quiet mode, no output
    # -w 2 ==> wait 2 seconds between files
    # -nH ==> don't create a directory based on the host, in this case no folder named www.swift.ac.uk/
    # --cut-dirs=2 ==> remove the /archive/reproc/ folders on the server from being created locally
    # -r ==> recursive: grab everything under this folder on the server
    # --reject ... ==> specify files that we don't want from the server
    adjusted_wget_commands = ['wget ' + overwrite_option + ' -q -w 2 -nH --cut-dirs=2 -r --no-parent --reject index.html*,robots.txt* ' + url for url in urls]
    
    return adjusted_wget_commands

def swift_download_uncompressed(tid: str, dtype: str, dest_dir: pathlib.Path = None, overwrite: bool = False) -> None:
    
    # given a Swift target id and type of data, this function downloads the uncompressed
    # data to the directory dest_dir
    
    # get our download commands from the server
    wget_commands = get_swift_wget_commands(tid=tid, dtype=dtype, overwrite=overwrite)
    if wget_commands is None:
        print("No wget commands to execute, skipping downloads...")
        return
    
    # change folders if we need to
    old_cwd = os.getcwd()
    if dest_dir is not None:
        os.chdir(dest_dir)
    print(f"Downloading {dtype} data of target id {tid} to {os.getcwd()} ...")
    
    # run each command to grab the individual observations for this target id
    for command in wget_commands:
        presult = subprocess.run(command.split())
        if presult.returncode != 0:
            print(f"Non-zero return code {presult.returncode} for {command}!")
    
    # change folders back
    os.chdir(old_cwd)

def swift_download_compressed(tid: str, tname: str, dtype: str, archive_type: str, dest_dir: pathlib.Path, overwrite: bool = False) -> None:

    """
        Downloads an archive of Swift data from swift.ac.uk to dest_dir

        Parameters
        ----------
        tid : string
            The target ID to be downloaded, e.g. '00020405'
        tname: string
            The name of the target, e.g. 'CometC/2031US10(Catalina)'
        dtype: string
            The type of data being downloaded, e.g. 'uvot'
        archive_type: string
            One of 'zip' or 'tar' to download the corresponding type
        dest_dir: pathlib.Path
            Directory to place files
        overwrite: bool
            Whether or not to overwrite the file if it already exists
    """
    
    # change folders if we need to
    old_cwd = os.getcwd()
    if dest_dir is not None:
        os.chdir(dest_dir)
    
    # name the archive with the target id and data type, because the server returns 'download.tar' no matter what
    out_file_stem = pathlib.Path(tid + f"_{dtype}")
    
    # download
    if archive_type == 'zip':
        print(f"Downloading .zip archives is broken server-side so is currently unsupported.")
    if archive_type == 'tar':
        swift_download_compressed_tar(tid=tid, tname=tname, dtype=dtype, out_file_stem=out_file_stem, overwrite=overwrite)

    os.chdir(old_cwd)
    return

def swift_download_compressed_tar(tid: str, tname: str, dtype: str, out_file_stem: pathlib.Path, overwrite: bool) -> None:

    out_file = out_file_stem.with_suffix('.tar')
    if out_file.exists() and overwrite is False:
        print(f"Found {str(out_file)} and overwriting was forbidden, skipping download.")
        return
    
    # build our urls and params to send the server
    swift_referer_base_url = 'https://www.swift.ac.uk/archive/prepdata.php'
    swift_download_portal_base_url = 'https://www.swift.ac.uk/archive/download.tar'

    referer_url = f"{swift_referer_base_url}?tid={tid}&source=obs&name={tname}&referer=portal"
    params = {
        'reproc': '1',
        'tid': tid,
        'source': 'obs',
        'subdir': dtype,
    }

    # lie to the server
    request_header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': referer_url,
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Sec-GPC': '1',
    }

    print(f"Attempting to download {tid} of {tname} to {out_file}, please wait ...")
    response = requests.get(swift_download_portal_base_url, params=params, headers=request_header)
    print(f"Requested data from {response.url}, response code {response.status_code} ...")

    # name the output file if it wasn't passed in an argument
    with open(out_file, 'wb') as f:
        f.write(response.content)
    
    print(f"Wrote {str(out_file)}.")

    return:
    
def download_files(tlist: str, dtype_list: str, dest_dir: pathlib.Path, download_type: str -> None:
    # downloads the files for 2+ results when searching
    # iterates over each requested data type and observation collected from get_multi_tlists()
    for dtype in dtype_list:
        for tid, tname in tlist:
            if download_type == 'uncompressed':
                    swift_download_uncompressed(tid=tid, dtype=dtype, dest_dir=dest_dir)
            if download_type in ['tar', 'zip']:
                   swift_download_compressed(tid=tid, tname=tname, dtype=dtype, archive_type=download_type, dest_dir=dest_dir)
