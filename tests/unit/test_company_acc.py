from src.account import CompanyAccount
import pytest

@pytest.fixture
def company_account():
    return CompanyAccount("Firma1", "0123456789")


class TestAccCreation:

    def test_acc_creation(self, company_account):
        assert company_account.company_name == "Firma1"
        assert company_account.nip == "0123456789"
        assert company_account.balance == 0

    @pytest.mark.parametrize("company_name,nip,expected_name,expected_nip", [
        ("Firma1", "01234567890", "Firma1", "Invalid"),
        (12, "0123456789", "Invalid", "0123456789"),
        (12, "01234567890", "Invalid", "Invalid"),
    ])
    def test_acc_creation_invalid(self, company_name, nip, expected_name, expected_nip):
        acc = CompanyAccount(company_name, nip)
        assert acc.company_name == expected_name
        assert acc.nip == expected_nip


class TestAccOperations:

    @pytest.mark.parametrize("initial,before,after,method", [
        (1010, 1010, 10, "send"),
        (0, 0, 1000, "receive"),
    ])
    def test_transfers(self, company_account, initial, before, after, method):
        company_account.balance = initial
        if method == "send":
            company_account.send_transfer(initial - after)
        else:
            company_account.receive_transfer(after - initial)
        assert company_account.balance == after

    @pytest.mark.parametrize("transfer_amount", [-10, 1000])
    def test_send_negative_or_insufficient(self, company_account, transfer_amount):
        company_account.balance = 0 if transfer_amount > 0 else 100
        balance_before = company_account.balance
        company_account.send_transfer(transfer_amount)
        assert company_account.balance == balance_before

    def test_receive_negative_transfer(self, company_account):
        balance_before = company_account.balance
        company_account.receive_transfer(-10)
        assert company_account.balance == balance_before


class TestAccExpressOperations:

    def test_express_transfer_send(self, company_account):
        company_account.balance = 1000
        transfer_amount = 900
        transfer_fee = company_account.get_express_transfer_fee()
        balance_before = company_account.balance

        company_account.send_express_transfer(transfer_amount)
        assert company_account.balance == balance_before - (transfer_amount + transfer_fee)

        company_account.balance = 100
        company_account.send_express_transfer(company_account.balance)
        assert company_account.balance == -company_account.get_express_transfer_fee()

        company_account.balance = 10
        company_account.send_express_transfer(100)
        assert company_account.balance == 10

        company_account.send_express_transfer(-10)
        assert company_account.balance == 10


class TestAccHistory:

    def test_acc_history(self, company_account):
        company_account.balance = 1000
        company_account.send_transfer(100)
        assert company_account.history == [-100.00]

        company_account.receive_transfer(150)
        assert company_account.history == [-100.00, 150.00]

        company_account.send_express_transfer(45)
        assert company_account.history == [-100, 150, -45, -company_account.get_express_transfer_fee()]
