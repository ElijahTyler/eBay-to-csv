from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from AuctionListings import AuctionListings
from AuctionData import AuctionData

from bs4 import BeautifulSoup
from sys import platform
import os, time
import time
import json
import re

def init_firefox(headless=False):
    opts = FirefoxOptions()

    if platform == "win32":
        opts.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        dev_null = "nul"
        driver_executable = 'geckodriver.exe'
    elif platform in ["linux", "linux2"]:
        dev_null = "/dev/null"
        driver_executable = 'geckodriver'
    else:
        print("Unsupported OS. Exiting program...")
        exit(1)

    if headless:
        opts.add_argument("--headless")
    opts.add_argument("--ignore-certificate-errors")
    opts.add_argument("--start-maximized")

    driver = webdriver.Firefox(options = opts, executable_path = driver_executable, service_log_path = dev_null)
    return driver

def main(url_list, search_term):
    start_time = time.time()

    auction_list = []
    for USER_URL in url_list:
        print("Loading Selenium (firefox)...")
        driver = init_firefox(headless=False)

        print("Loading ebay.com URL...")
        driver.get(USER_URL)

        # finds one or more numbers at the end of the data-view attribute
        data_view_re = re.compile("mi:1686|iid:\d+$")
        id_re = re.compile("item[a-zA-Z0-9]+")

        entries = []
        timeout = 0
        while not entries:
            time.sleep(1)
            html = driver.execute_script("return document.documentElement.outerHTML")
            soup = BeautifulSoup(html, 'html.parser')
            entries = soup.find_all(attrs={"data-view": data_view_re, "id": id_re})
            timeout += 1
            if timeout > 10:
                print(f"Timeout reached. Ending program...")
                driver.close()
                break

        for entry in entries:
            al = AuctionListings(str(entry))
            auction_list.append(al)

        driver.close()

    print(f"Success! Results found: {len(auction_list)}")
    
    with open("listings.json", "w") as f:
        listing = 1
        auction_dict = {}
        for auction in auction_list:
            auction_dict[listing] = auction.to_dict()
            listing += 1
        json.dump(auction_dict, f, indent=4)

    # create .csv file
    obj = AuctionData('listings.json')
    obj.generate_csv(search_term.title() + " Data.csv")

    # delete .json file
    os.remove("listings.json")

    # time taken to 2 decimal points
    total_time = round(time.time() - start_time, 2)
    print(f"Time taken: {total_time} seconds")

if __name__ == "__main__":
    search_term = input("Enter search term: ")
    # sort_by_price = ["", "&_sop=15"][input("Sort by price? (y/n): ").lower() == "y"]
    sort_by_price = ""
    url1 = f"https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2047675.m570.l1313&_nkw={search_term}&_sacat=0&_ipg=240{sort_by_price}"
    urls = [url1]
    main(urls, search_term)