# Gamza_OSINT
            _____   ___  ___  ___ ______  ___
            |  __ \ / _ \ |  \/  ||___  / / _ \
            | |  \// /_\ \| .  . |   / / / /_\ \
            | | __ |  _  || |\/| |  / /  |  _  |
            | |_\ \| | | || |  | |./ /___| | | |
            \____/\_| |_/\_|  |_/\_____/\_| |_/
            _____  _____  _____  _   _  _____ 
            |  _  |/  ___||_   _|| \ | ||_   _|
            | | | |\ `--.   | |  |  \| |  | |  
            | | | | `--. \  | |  | . ` |  | |  
            \ \_/ //\__/ / _| |_ | |\  |  | |  
             \___/ \____/  \___/ \_| \_/  \_/  

**Automatically extracts text from the image and estimates the location based on the text.**

Open Source Intelligence (OSINT) refers to information obtained from public sources such as SNS and the web. 

OSINT information collection is the most basic method of investigation in cybercrime investigation and investigation, and it is a task that requires search technology from various perspectives.
The theme of this project is the "Image Location Information Inquiry System", which was intended to provide meaningful information by focusing on location information among various disclosed information. 

To this end, related place data was collected through search engine crawling based on text data extracted from images. 

The search results of two search engines, Google and Naver, were used to avoid bias against one search result when crawling the search engine.

Only meaningful location data is selected from the collected data to provide information on a place in the image.

Location information is limited to Korea, and for this purpose, road name/districting address information provided by the Korean government and Naver's map search API were used. 

Through these programs, it was intended to help quickly and conveniently collect information when location information on images acquired during cybercrime investigations and investigations is needed.

## Usage

0. Setting Google Cloud Vision API and Get a key from Google Cloud, Naver Map API
1. Insert Data Config ini ( File Path, Google Key, etc..)
2. Run app.py and Wait processing



