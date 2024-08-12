# Swift Portal Downloader
- A program to search and download data from the SWIFT dead portal ([www.swift.ac.uk/dead_portal/index.php](www.swift.ac.uk/dead_portal/index.php)).  

# Configuration
- If there is no file named ```spd_config.yaml``` in the current directory, you will be prompted for some information about where to store downloads and what type of SWIFT data you want.
- These choices will be saved into ```spd_config.yaml``` in plain text and may be edited at will.

# The Comet Database
- The first step is gather all of the known comet observations from the SWIFT servers into a local database.
- This only needs to be done the first time you run this program, or when you want to see if there are new observations available.
- Only observations with names that match 'C/', 'Comet', or 'P/' are included - if there are any observations of comets not named this way by SWIFT,
they will not be found by this tool.

Database Columns
- ```swift_target_name```: The name given to the observation by the SWIFT operator, which has not always used standard comet designations.
- ```target_id```: Unique ID for a set of observations of the given target.
- ```number_of_observations```: The number of observations in the set for ```target_id```.
- ```canonical_name```: Standardized comet designations extracted from ```swift_target_name``` - it is possible for this to fail, so please report those cases as issues on github.

The menu option ```Comet database info``` will let you search the local database by comet designation to see what is available.

# Downloading

- The menu option ```Download comet data``` will let you search the local database by comet designation and download the associated data.
- If any data has been downloaded already, it will not be re-downloaded.
- Only the type(s) of data specified in ```spd_config.yaml``` will be downloaded.
- All target IDs that are available will be downloaded - there is currently no option to select which target IDs.
