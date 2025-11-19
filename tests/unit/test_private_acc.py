from src.account import Account
import pytest

@pytest.fixture
def account():
    return Account("John", "Doe", "12345678910")


class TestAccCreation:

    def test_account_creation(self, account):
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0
        assert account.pesel == "12345678910"

    @pytest.mark.parametrize("pesel", [
        "1234567891011",
        "123",
    ])
    def test_acc_creation_invalid_pesel(self, pesel):
        acc = Account("John", "Doe", pesel)
        assert acc.pesel == "Invalid"

    @pytest.mark.parametrize("pesel,promo,balance", [
        ("12345678910", "PROMO_XYZ", 50),
        ("12345678910", "PROMO_HSA", 50),
        ("12345678910", " PROMO_XYZ", 50),
        ("12345678910", "PROMO_XYZ  ", 50),
        ("12345678910", "PROMO_HJ", 0),
        ("12345678910", "PROMO_X", 0),
        ("12345678910", "PROMO_", 0),
        ("12345678910", "PROMO_   ", 0),
        ("12345678910", "PROMO_ZXCV", 0),
        ("12345678910", "PROMO_ZOHJASDJOIXCV", 0),
        ("59123456789", "PROMO_XYZ", 0),
    ])
    def test_acc_creation_with_promo_code(self, pesel, promo, balance):
        acc = Account("John", "Doe", pesel, promo)
        assert acc.balance == balance


class TestAccOperations:

    @pytest.mark.parametrize("initial,before,after", [
        (1010, 1010, 10),
        (1000, 0, 1000),
    ])
    def test_transfers(self, account, initial, before, after):
        account.balance = initial
        if before > after:
            account.send_transfer(initial - after)
        else:
            account.receive_transfer(after - initial)
        assert account.balance == after

    @pytest.mark.parametrize("transfer_amount", [-10, 1000])
    def test_send_negative_or_insufficient(self, account, transfer_amount):
        account.balance = 0 if transfer_amount > 0 else 100
        balance_before = account.balance
        account.send_transfer(transfer_amount)
        assert account.balance == balance_before

    def test_receive_negative_transfer(self, account):
        balance_before = account.balance
        account.receive_transfer(-10)
        assert account.balance == balance_before


class TestAccExpressOperations:

    def test_express_transfer_send(self, account):
        account.balance = 1000
        transfer_amount = 900
        transfer_fee = account.get_express_transfer_fee()
        balance_before = account.balance
        account.send_express_transfer(transfer_amount)
        assert account.balance == balance_before - (transfer_amount + transfer_fee)

        account.balance = 100
        account.send_express_transfer(account.balance)
        assert account.balance == -account.get_express_transfer_fee()

        account.balance = 10
        account.send_express_transfer(100)
        assert account.balance == 10

        account.send_express_transfer(-10)
        assert account.balance == 10


class TestAccHistory:

    def test_acc_history(self, account):
        account.balance = 1000
        account.send_transfer(100)
        assert account.history == [-100.00]
        account.receive_transfer(150)
        assert account.history == [-100.00, 150.00]
        account.send_express_transfer(45)
        assert account.history == [-100, 150, -45, -account.get_express_transfer_fee()]


class TestSubmitForLoan:

    def test_no_pesel(self):
        account = Account("John", "Doe", pesel=None)
        assert account.apply_for_loan(100) is False

    @pytest.mark.parametrize("history,expected,balance_change", [
        ([100, 200], False, 0),
        ([50, 100, 200], True, 100),
        ([10, 20, 30, 40], True, 100),
        ([100, -50, 200], False, 0),
        ([10, 20, -5, 30], False, 0),
        ([10, 20, 30, 40, 50], True, 100),
        ([0, 0, 20, 30, 51], True, 100),
        ([10, 10, 10, 10, 10], False, 0),
        ([20, 20, 20, 20, 20], False, 0),
    ])
    def test_apply_for_loan_cases(self, account, history, expected, balance_change):
        account.history = history
        account.balance = 0
        result = account.apply_for_loan(100)
        assert result is expected
        assert account.balance == balance_change
