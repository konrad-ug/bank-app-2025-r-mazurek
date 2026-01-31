import pytest
import requests
import random

BASE_URL = "http://127.0.0.1:5000/api/accounts"


class TestPerformance:

    def test_create_delete_performance(self):
        for _ in range(100):
            pesel = f"{random.randint(10000000000, 99999999999)}"
            payload = {
                "first_name": "Waldek",
                "last_name": "Test",
                "pesel": pesel
            }

            create_resp = requests.post(BASE_URL, json=payload, timeout=0.5)
            assert create_resp.status_code == 201

            delete_resp = requests.delete(f"{BASE_URL}/{pesel}", timeout=0.5)
            assert delete_resp.status_code == 200

    def test_incoming_transfers_performance(self):
        pesel = f"{random.randint(10000000000, 99999999999)}"
        payload = {
            "first_name": "Transfer",
            "last_name": "Perf",
            "pesel": pesel
        }

        requests.post(BASE_URL, json=payload)

        transfer_amount = 10
        transfer_data = {
            "type": "incoming",
            "amount": transfer_amount
        }

        for _ in range(100):
            resp = requests.post(f"{BASE_URL}/{pesel}/transfer", json=transfer_data, timeout=0.5)
            assert resp.status_code == 200

        get_resp = requests.get(f"{BASE_URL}/{pesel}")
        assert get_resp.json()["balance"] == 100 * transfer_amount