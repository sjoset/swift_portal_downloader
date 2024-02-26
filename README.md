# Swift Portal Downloader  
## Install Poetry  
Documentation about the poetry package can be found [here](https://www.python-poetry.org).  
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
This will install all the packages needed to compile and run the program.
## Running the Program  
```
    conda activate env_name_here
    spd_tui
```
## Configuration File
To run the program successfully, a file named **config.yaml** must be in the current directory.  
It should contain the following elements:
```    
    download_path: 'directory to store downloaded images'  
    dtype_list: list containing a combination of ['auxil', 'bat', 'xrt', 'uvot', 'log']  
    obs_list_path: 'directory to store any generated observation lists'
```
*Note:* **download_path** *and* **dtype_list** *are required to be in your config file, but* **obs_list_path** *is optional (if no input is found, it will default to the current working directory)*  
#### Config.yaml
Here is an example of a config.yaml file:
```
    download_path: 'Users/user/downloads'
    dtype_list: ['auxil', 'uvot', 'log']  
```
