from behave import *
import requests

URL = "http://127.0.0.1:5000"


@step('I create an account using name: "{name}", last name: "{last_name}", pesel: "{pesel}"')
def create_account(context, name, last_name, pesel):
    json_body = {
        "first_name": name,
        "last_name": last_name,
        "pesel": pesel
    }
    create_resp = requests.post(URL + "/api/accounts", json=json_body)
    assert create_resp.status_code == 201


@step('Account registry is empty')
def clear_account_registry(context):
    response = requests.get(URL + "/api/accounts")
    if response.status_code == 200:
        accounts = response.json()
        for account in accounts:
            pesel = account.get("pesel")
            if pesel:
                requests.delete(URL + f"/api/accounts/{pesel}")


@step('Number of accounts in registry equals: "{count}"')
def is_account_count_equal_to(context, count):
    response = requests.get(URL + "/api/accounts/count")
    assert response.status_code == 200
    assert str(response.json()["count"]) == str(count)


@step('Account with pesel "{pesel}" exists in registry')
def check_account_with_pesel_exists(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200
    assert response.json()["pesel"] == pesel


@step('Account with pesel "{pesel}" does not exist in registry')
def check_account_with_pesel_does_not_exist(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 404


@when('I delete account with pesel: "{pesel}"')
def delete_account(context, pesel):
    response = requests.delete(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200


@when('I update "{field}" of account with pesel: "{pesel}" to "{value}"')
def update_field(context, field, pesel, value):
    valid_fields = ["first_name", "last_name"]

    if field == "name": field = "first_name"
    if field == "surname": field = "last_name"

    if field not in valid_fields:
        raise ValueError(f"Invalid Field: {field}. Must be one of {valid_fields}")

    json_body = {field: value}
    response = requests.patch(URL + f"/api/accounts/{pesel}", json=json_body)
    assert response.status_code == 200


@then('Account with pesel "{pesel}" has "{field}" equal to "{value}"')
def field_equals_to(context, pesel, field, value):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200
    data = response.json()

    actual_value = str(data.get(field))
    assert actual_value == value, f"Expected {field} to be {value}, but got {actual_value}"


@when('I make an "{transfer_type}" transfer of "{amount}" to account with pesel "{pesel}"')
@when('I make an "{transfer_type}" transfer of "{amount}" from account with pesel "{pesel}"')
def make_transfer(context, transfer_type, amount, pesel):
    json_body = {
        "amount": float(amount),
        "type": transfer_type
    }
    response = requests.post(URL + f"/api/accounts/{pesel}/transfer", json=json_body)
    assert response.status_code == 200