# Swift Portal Downloader
- A program to search and download data from the SWIFT dead portal ([www.swift.ac.uk/dead_portal/index.php](www.swift.ac.uk/dead_portal/index.php)).  

## Installation

Create a new conda environment:
```
    conda create --name swift_portal_downloader python=3.11
    conda activate swift_portal_downloader
```

### Pip Installation
```pip install swift_portal_downloader```

### Development Installation
#### Install Poetry  
Documentation about the poetry package can be found [here](https://www.python-poetry.org).  

#### Clone Repository
```
    git clone https://github.com/sjoset/swift_portal_downloader.git
```

#### Install Package Locally  
In the repository's directory:
```
    poetry install
```

## Usage
```
    conda activate swift_portal_downloader
    spd_tui
```
On first run, you will be prompted for some configuration options.
For information on usage, there is help available from the main menu.
