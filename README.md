# Swift Portal Downloader  
## Install Poetry  
Documentation can be found [https://www.python-poetry.org](https://www.python-poetry.org)  
Install poetry with pip: 
```
    pip install poetry
```
## Create Conda Environment with Python
```
    conda create --name env_name_here python=3.11
    conda activate env_name_here
```
## Install Package Locally  
In the repository's directory:
```
    poetry install
```
## Running the Program  
```
    conda activate env_name_here
    spd_tui
```
## Configuration File
To run the program successfully, a file called **config.yaml** must be in the current directory.  
It should contain the following elements:
```
    download_path: directory to download images  
    dtype_list: list containing a combination of ['auxil', 'bat', 'xrt', 'uvot', 'log']  
```
#### Config.yaml
Here is an example of a config.yaml file:
```
    download_path: 'Users/user/downloads'
    dtype_list: ['auxil', 'uvot', 'log']  
```
