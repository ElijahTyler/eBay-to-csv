from bs4 import BeautifulSoup
import re

class AuctionListings:
    def __init__(self, obj = None) -> None:
        if not obj:
            self.name = None
            self.condition = None
            self.price = None
        else:
            def extract_nums(string): # returns -1 if no numbers found
                temp = re.sub("[^.0-9]", "", string)
                if temp:
                    return float(temp)
                else:
                    return -1
            
            soup = BeautifulSoup(obj, 'html.parser')

            # item name
            self.name = soup.find(attrs={"aria-level": "3"}).text.replace("amp;", "").strip().replace("New Listing", "")

            # condition
            self.condition = soup.find(attrs={"class": "SECONDARY_INFO"}).text.strip()

            # price
            self.price = soup.find(attrs={"class": "s-item__price"}).text.replace("\n","").strip().split(" ")
            if len(self.price) > 1:
                self.price = [extract_nums(self.price[0]), extract_nums(self.price[-1])]
            else:
                self.price = extract_nums(self.price[0])

            # link
            self.link = soup.find('a')['href']

    def __str__(self) -> str:
        return f'Name: {self.name}\nCondition: {self.condition}\nPrice: {self.price}\nLink: {self.link}'

    def to_dict(self) -> dict:
        # make dictionary of all attributes
        return {
            "name": self.name,
            "condition": self.condition,
            "price": self.price,
            "link": self.link
        }
