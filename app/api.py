from flask import jsonify, request, Flask
from src.account import Account, CompanyAccount, AccountRegistry

app = Flask(__name__)
registry = AccountRegistry()


@app.route("/api/accounts", methods=["GET"])
def get_accounts():
    print("Get all accounts request received")
    accounts = registry.return_all()

    accounts_data = []
    for acc in accounts:
        if isinstance(acc, CompanyAccount):
            accounts_data.append({
                "type": "company",
                "company_name": acc.company_name,
                "nip": acc.nip,
                "balance": acc.balance
            })
        else:
            accounts_data.append({
                "type": "personal",
                "first_name": acc.first_name,
                "last_name": acc.last_name,
                "pesel": acc.pesel,
                "balance": acc.balance
            })

    return jsonify(accounts_data), 200


@app.route("/api/accounts", methods=["POST"])
def create_account():
    print("Create new account request received")
    data = request.get_json()

    if "nip" in data and "company_name" in data:
        account = CompanyAccount(company_name=data["company_name"], nip=data["nip"])
        registry.add_account(account)
        return jsonify({"message": f"Company Account {account.company_name} has been created"}), 201

    elif "first_name" in data and "last_name" in data and "pesel" in data:
        account = Account(first_name=data["first_name"],
                          last_name=data["last_name"],
                          pesel=data["pesel"],
                          promo_code=data.get("promo_code"))

        registry.add_account(account)
        return jsonify({"message": f"Account {account.first_name} {account.last_name} has been created"}), 201

    return jsonify({"error": "Invalid data provided"}), 400


@app.route("/api/accounts/count", methods=["GET"])
def get_account_count():
    print("Get account count request received")
    # Poprawiono metodę na return_amount() zgodnie z account.py
    account_count = registry.return_amount()
    return jsonify({"count": account_count}), 200


@app.route("/api/accounts/<pesel>", methods=["GET"])
def get_account_by_pesel(pesel):
    print("Get account by pesel request received")
    account = registry.find_acc_by_pesel(pesel)

    if account:
        return jsonify({
            "first_name": account.first_name,
            "last_name": account.last_name,
            "pesel": account.pesel,
            "balance": account.balance
        }), 200
    return jsonify({"message": "Account not found"}), 404


@app.route("/api/accounts/<pesel>", methods=["PATCH"])
def update_account(pesel):
    print("Update account request received")
    data = request.get_json()

    account = registry.find_acc_by_pesel(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404

    if "first_name" in data:
        account.first_name = data["first_name"]
    if "last_name" in data:
        account.last_name = data["last_name"]
    if "balance" in data:
        account.balance = data["balance"]
    if "pesel" in data:
        account.pesel = data["pesel"]

    return jsonify({"message": f"Account {pesel} updated successfully"}), 200


@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    print("Delete account request received")
    account = registry.find_acc_by_pesel(pesel)
    if not account:
        return jsonify({"message": "Account not found"}), 404

    registry.delete_acc_by_pesel(pesel)
    return jsonify({"message": f"Account {pesel} has been deleted"}), 200


if __name__ == '__main__':
    app.run(debug=True)