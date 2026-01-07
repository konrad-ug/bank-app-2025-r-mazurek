from src.account import CompanyAccount
import pytest
from unittest.mock import patch

@pytest.fixture
def mock_gov_api_valid():
    with patch('src.account.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": {
                "subject": {
                    "statusVat": "Czynny",
                    "name": "Test Company"
                },
                "requestId": "123"
            }
        }
        yield mock_get

@pytest.fixture
def company_account(mock_gov_api_valid):
    return CompanyAccount("Firma1", "0123456789")


class TestAccCreation:

    def test_acc_creation(self, company_account):
        assert company_account.company_name == "Firma1"
        assert company_account.nip == "0123456789"
        assert company_account.balance == 0

    def test_acc_creation_invalid_length(self):
        with patch('src.account.requests.get') as mock_get:
            acc = CompanyAccount("Firma1", "123")
            assert acc.nip == "Invalid"
            mock_get.assert_not_called()

    def test_acc_creation_raises_error_if_not_registered(self):
        with patch('src.account.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {
                "result": {
                    "subject": None
                }
            }

            with pytest.raises(ValueError, match="Company not registered!!"):
                CompanyAccount("Firma Krzak", "0123456789")


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
        
class TestBusinessLoans:

    @pytest.mark.parametrize("account_balance,account_history,expected_decision", [
        (2000, [100, 5000, -1775], True),
        (200, [100, 100], False),
        (200, [-1775, 100], False),
        (2000, [100, 200, -1700], False)
    ])
    def test_business_loans(self, company_account, account_balance, account_history, expected_decision):
        loan_amount = 1000
        
        company_account.balance = account_balance
        company_account.history = account_history
        
        if expected_decision is True:
            assert company_account.apply_for_loan(loan_amount) is True 
            assert company_account.balance == account_balance + loan_amount
        else:
            assert company_account.apply_for_loan(loan_amount) is False
            assert company_account.balance == account_balance
            
        
