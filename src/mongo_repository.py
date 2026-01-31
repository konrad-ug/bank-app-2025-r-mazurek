from pymongo import MongoClient
import os
from src.account import Account, CompanyAccount


class MongoAccountsRepository:
    def __init__(self):
        host = os.environ.get('MONGO_HOST', 'localhost')
        self.client = MongoClient(f"mongodb://{host}:27017/")
        self.db = self.client["bank_system"]
        self.collection = self.db["accounts"]

    def save_all(self, accounts):
        self.collection.delete_many({})

        for account in accounts:
            self.collection.insert_one(account.to_dict())

    def load_all(self):
        documents = self.collection.find()
        accounts = []

        for doc in documents:
            if doc.get("type") == "company":
                acc = CompanyAccount(doc["company_name"], doc["nip"])
            else:
                acc = Account(doc["first_name"], doc["last_name"], doc["pesel"])

            acc.balance = doc["balance"]
            acc.history = doc["history"]
            accounts.append(acc)

        return accounts