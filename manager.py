import csv
import os


class StockManager:
    def __init__(self, file="data/stock.csv"):
        self.file = file
        self.items = []
        self.load()

    # Load items from csv file
    def load(self):
        if not os.path.exists(self.file):
            return

        with open(self.file, newline="") as f:
            reader = csv.DictReader(f)
            self.items = list(reader)

    # Save item to csv file
    def save(self):
        with open(self.file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "qty", "image"])
            writer.writeheader()
            writer.writerows(self.items)

    # Add new item
    def add_new_item(self, name):
        for item in self.items:
            if item["name"] == name:
                return

        self.items.append({"name": name, "qty": "0", "image": ""})
        self.save()

    # Add item to stock
    def add_item_in_stock(self, name, qty):
        for item in self.items:
            if item["name"] == name:
                item["qty"] = str(int(item["qty"]) + int(qty))
                self.save()
                return

        self.items.append({"name": name, "qty": str(qty), "image": ""})
        self.save()

    def update_image(self, name, path):
        for item in self.items:
            if item["name"] == name:
                item["image"] = path
        self.save()

    def update_qty(self, name, new_qty):
        if new_qty < 0:
            return

        for item in self.items:
            if item["name"] == name:
                item["qty"] = str(new_qty)
                break
        self.save()

    def delete_item_by_name(self, name):
        self.items = [i for i in self.items if i["name"] != name]
        self.save()

    def get_items(self):
        return self.items