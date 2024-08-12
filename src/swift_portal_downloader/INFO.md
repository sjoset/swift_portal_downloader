# Swift Dead Portal Downloader
A program to search and download images from the swift dead portal ([www.swift.ac.uk/dead_portal/index.php](www.swift.ac.uk/dead_portal/index.php)).  
## Searching the poral 
- Given two options (**mass search comets** and **specific query**). 
- Mass search will search the portal for 
the terms "C/", "P/", and "Comet" and generate the observation list (which contains all observation id(s) and canonical names).  
- Specific search query will allow you to search the portal for a term and gernerate the observation list based on the results.  
- All observation list files will be downloaded to the observation list path or current working directory as **"portal_search_results.csv"**.    
## Downloading
- Will download all observation id(s) found in the observation list.
- The observation list must be in the current working directory.  
- All files will be downloaded as uncompressed files. If swift adds compressed downloading, then this program may be updated at a later date.
- Directory will be formatted as follows: **download_dir/canonical_name/observation_id/data_type**
## Naming scheme
- The swift portal stores the target names based on the name assigned by the operator using the instrument. 
As such there is a wide variety of different target names for the same comet (ie: C/2013US10CatalinaOrbit3 and CometCatalinaOrbit1 
are both C/2013US10 data).
- When searching the portal, we convert this swift target name to a canonical name by using regular expressions search operations. However, some
names cannot be converted using this method, and a manual naming scheme is used.
- If a swift target name is not able to be converted when generating the observation list and it is not found in the naming scheme, then you will
be required to enter the canonical name and update the naming scheme.
- The manual naming scheme can be viewed or edited at any time.

