import unittest
from unittest.mock import MagicMock, patch
from src.mongo_repository import MongoAccountsRepository
from src.account import Account


class TestMongoRepository(unittest.TestCase):

    def setUp(self):
        self.mock_client = MagicMock()
        self.mock_db = MagicMock()
        self.mock_collection = MagicMock()

        self.mock_client.__getitem__.return_value = self.mock_db
        self.mock_db.__getitem__.return_value = self.mock_collection

        with patch('src.mongo_repository.MongoClient', return_value=self.mock_client):
            self.repo = MongoAccountsRepository()

    def test_save_all(self):
        account = Account("Wladek", "Test", "12345678901")
        accounts = [account]

        self.repo.save_all(accounts)

        self.repo.collection.delete_many.assert_called_once_with({})

        self.repo.collection.insert_one.assert_called()
        inserted_data = self.repo.collection.insert_one.call_args[0][0]
        self.assertEqual(inserted_data["pesel"], "12345678901")

    def test_load_all(self):
        mock_data = [{
            "first_name": "Jan",
            "last_name": "Kowalski",
            "pesel": "90010112345",
            "balance": 100.0,
            "history": [100.0],
            "type": "personal"
        }]
        self.repo.collection.find.return_value = mock_data

        loaded_accounts = self.repo.load_all()

        self.assertEqual(len(loaded_accounts), 1)
        self.assertEqual(loaded_accounts[0].first_name, "Jan")
        self.assertEqual(loaded_accounts[0].balance, 100.0)