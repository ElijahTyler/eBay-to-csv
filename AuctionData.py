import json
import csv

class AuctionData:
    def __init__(self, jason = None) -> None:
        # takes in a .json file generated from dictionary of AuctionListings
        self.names = []
        self.conditions = []
        self.prices = []
        self.links = []
        if not jason:
            return
        with open(jason, 'r') as f:
            self.data = json.load(f)
            for a in self.data:
                item = self.data[a]
                self.names.append(item["name"])
                self.conditions.append(item["condition"])
                self.prices.append(item["price"])
                self.links.append(item["link"])

    def generate_csv(self, name = None):
        if not name:
            name = "AuctionData.csv"
        if not name.endswith(".csv"):
            name += ".csv"
        
        with open(name, 'w', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Name", "Condition", "Price", "Link"])

            for i in range(len(self.names)):
                writer.writerow([self.names[i], self.conditions[i], self.prices[i], self.links[i]])
        
        print(f"CSV file generated: {name}")