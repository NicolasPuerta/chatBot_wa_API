from models import MongoDB

class Database:
    def __init__(self):
        self.db = MongoDB()
        self.collection = self.db.collection

    def get_collection(self):
        return self.collection

    def insert_one(self, data):
        return self.collection.insert_one(data)

    def find(self, from_number):
        return self.collection.find({"from": from_number}).limit(1)

    def update_one(self, data):
        return self.collection.update_one({
            "from_number": data["from_number"]
        }, {"$set": data}, upsert=True)