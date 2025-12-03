import pytest
import requests
import random

BASE_URL = "http://127.0.0.1:5000/api/accounts"

@pytest.fixture
def unique_pesel():
    return f"{random.randint(10000000000, 99999999999)}"


@pytest.fixture
def created_account(unique_pesel):
    account_data = {
        "first_name": "Jan",
        "last_name": "Testowy",
        "pesel": unique_pesel,
    }
    response = requests.post(BASE_URL, json=account_data)
    assert response.status_code == 201
    return account_data


def test_create_account(unique_pesel):
    payload = {
        "first_name": "Anna",
        "last_name": "Nowak",
        "pesel": unique_pesel
    }

    response = requests.post(BASE_URL, json=payload)

    assert response.status_code == 201
    data = response.json()
    assert "has been created" in data["message"]

    check_response = requests.get(f"{BASE_URL}/{unique_pesel}")
    assert check_response.status_code == 200
    assert check_response.json()["first_name"] == "Anna"


def test_get_account_by_pesel(created_account):
    pesel = created_account["pesel"]

    response = requests.get(f"{BASE_URL}/{pesel}")

    assert response.status_code == 200
    data = response.json()
    assert data["pesel"] == pesel
    assert data["first_name"] == created_account["first_name"]
    assert "balance" in data


def test_get_non_existent_account():
    non_existent_pesel = "00000000000"

    response = requests.get(f"{BASE_URL}/{non_existent_pesel}")

    assert response.status_code == 404
    assert response.json()["message"] == "Account not found"


def test_update_account(created_account):
    pesel = created_account["pesel"]
    new_last_name = "Zaktualizowana"

    patch_payload = {
        "last_name": new_last_name
    }

    response = requests.patch(f"{BASE_URL}/{pesel}", json=patch_payload)
    assert response.status_code == 200

    get_response = requests.get(f"{BASE_URL}/{pesel}")
    updated_data = get_response.json()

    assert updated_data["last_name"] == new_last_name
    assert updated_data["first_name"] == created_account["first_name"]


def test_delete_account(created_account):
    pesel = created_account["pesel"]

    response = requests.delete(f"{BASE_URL}/{pesel}")
    assert response.status_code == 200

    check_response = requests.get(f"{BASE_URL}/{pesel}")
    assert check_response.status_code == 404

def test_create_duplicate_account(created_account):
    payload = {
        "first_name": "Clone",
        "last_name": "Person",
        "pesel": created_account["pesel"]
    }

    response = requests.post(BASE_URL, json=payload)

    assert response.status_code == 409
    assert "Account already exists" in response.json()["message"]

def test_transfer_incoming(created_account):
    pesel = created_account["pesel"]
    transfer_data = {
        "amount": 1000,
        "type": "incoming"
    }

    response = requests.post(f"{BASE_URL}/{pesel}/transfer", json=transfer_data)

    assert response.status_code == 200
    assert "Zlecenie przyjeto do realizacji" in response.json()["message"]

    get_response = requests.get(f"{BASE_URL}/{pesel}")
    assert get_response.json()["balance"] == 1000


def test_transfer_outgoing_success(created_account):
    pesel = created_account["pesel"]

    requests.post(f"{BASE_URL}/{pesel}/transfer", json={"amount": 500, "type": "incoming"})

    transfer_data = {
        "amount": 200,
        "type": "outgoing"
    }
    response = requests.post(f"{BASE_URL}/{pesel}/transfer", json=transfer_data)

    assert response.status_code == 200

    get_response = requests.get(f"{BASE_URL}/{pesel}")
    assert get_response.json()["balance"] == 300


def test_transfer_outgoing_insufficient_funds(created_account):
    pesel = created_account["pesel"]

    transfer_data = {
        "amount": 100,
        "type": "outgoing"
    }

    response = requests.post(f"{BASE_URL}/{pesel}/transfer", json=transfer_data)

    assert response.status_code == 422
    assert "Transfer failed" in response.json()["message"]


def test_transfer_account_not_found():
    non_existent_pesel = "99999999999"
    transfer_data = {
        "amount": 100,
        "type": "incoming"
    }

    response = requests.post(f"{BASE_URL}/{non_existent_pesel}/transfer", json=transfer_data)

    assert response.status_code == 404
    assert "Account not found" in response.json()["message"]


def test_transfer_invalid_type(created_account):
    pesel = created_account["pesel"]
    transfer_data = {
        "amount": 100,
        "type": "invalid"
    }

    response = requests.post(f"{BASE_URL}/{pesel}/transfer", json=transfer_data)

    assert response.status_code == 400
    assert "Invalid type provided" in response.json()["message"]