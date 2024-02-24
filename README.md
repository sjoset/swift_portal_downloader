# Swift Portal Downloader  
## Install poetry  
Documentation can be found [https://www.python-poetry.org](https://www.python-poetry.org)  
Install poetry with pip: 
```
    pip install poetry
```
## Create conda environment with python
```
    conda create --name env_name_here python=3.11
    conda activate env_name_here
```
## Install package locally  
In the repository's directory:
```
    poetry install
```
## Running the program  
```
    conda activate env_name_here
    spd_tui
```
## Config file  
To run the program, a file called **config.yaml** must be in the current directory.  
### config.yaml
```
    download_path: directory to download images  
    dtype_list: list containing a combination of ['auxil', 'bat', 'xrt', 'uvot', 'log']  
```
