# eBay to CSV

a Python-based eBay listing scraper for Windows + Linux

made from Template-pedia

## Installation

0. Ensure you have Firefox installed to the default location
1. Download and extract the .zip at <https://github.com/ElijahTyler/eBay-to-csv.git>
2. Open Terminal in the project directory and type `python -m pip install -r requirements.txt`

## Usage

Open Terminal in the project directory and type `python main.py`. This will prompt you for a search term. Once the search term is entered, the progam will open an automated Firefox window that scrapes eBay's first 240 entries of your search. Then, an AuctionListing object is created for each listing it finds. Lastly, `{your search term} Data.csv` will be created, compiling a data sheet of all AuctionListings objects in an easy-to-read format.
