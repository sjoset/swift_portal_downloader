# Swift Dead Portal Downloader
A program to search and download images from the swift dead portal ([www.swift.ac.uk/dead_portal/index.php](www.swift.ac.uk/dead_portal/index.php)).  
## Searching the poral 
- Given two options (**mass search comets** and **specific query**). 
- Mass search will search the portal for 
the terms "C/", "P/", and "Comet" and generate the observation list (which contains all observation id(s) and conventional names).  
- Specific search query will allow you to search the portal for a term and gernerate the observation list based on that.  
- All observation list files will be downloaded to the current working directory as **"portal_search_results.csv"**.    
## Downloading
- Will download all observation id(s) found in the observation list.
- All files will be downloaded as uncompressed files. If swift adds compressed downloading, then this program may be updated at a later date.
- Directory will be formatted as follows: **download_dir/conventional_name/observation_id/data_type**
## Naming scheme
- The swift portal stores the image names based on the name assigned by the operator using the instrument. 
As such there is a wide varity of different names for the same comet (ie: C/2013US10CatalinaOrbit3 and CometCatalinaOrbit1 
both are C/2013US10 images).
- When searching the portal, we convert this swift name to a conventional name by using the regular expressions search operation,
however, some names cannot be convered like this, thus a manual naming scheme is used to convert the swift name to the conventional name.
- If a swift name is not able to be convered when generating the observation list and it is not found in the naming scheme, then you will
be required to enter the conventional name and update the name scheme.
- The manual name scheme can be viewed or edited at any time.
