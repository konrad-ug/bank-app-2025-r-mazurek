import pytest
from unittest.mock import patch
from datetime import datetime
from src.account import Account, CompanyAccount


class TestMailSending:

    @pytest.fixture
    def account(self):
        return Account("Jan", "Kowalski", "12345678910")

    @pytest.fixture
    def company_account(self):
        with patch.object(CompanyAccount, 'verifiy_nip_with_gov_api', return_value=True):
            return CompanyAccount("Firma Janusz", "1234567890")

    def test_send_email_personal_account_success(self, account):
        account.add_to_acc_history(100)
        account.add_to_acc_history(-50)
        email = "jan@test.test"
        today = datetime.now().strftime("%Y-%m-%d")
        expected_subject = f"Account Transfer History {today}"
        expected_body = f"Personal account history: [100, -50]"

        with patch('src.account.SMTPClient.send', return_value=True) as mock_send:
            result = account.send_history_via_email(email)

            assert result is True
            mock_send.assert_called_once_with(expected_subject, expected_body, email)

    def test_send_email_personal_account_failure(self, account):
        email = "jan@test.test"

        with patch('src.account.SMTPClient.send', return_value=False) as mock_send:
            result = account.send_history_via_email(email)

            assert result is False
            mock_send.assert_called_once()

    def test_send_email_company_account_success(self, company_account):
        company_account.add_to_acc_history(5000)
        email = "biuro@firma.pl"
        today = datetime.now().strftime("%Y-%m-%d")
        expected_subject = f"Account Transfer History {today}"
        expected_body = f"Company account history: [5000]"

        with patch('src.account.SMTPClient.send', return_value=True) as mock_send:
            result = company_account.send_history_via_email(email)

            assert result is True
            mock_send.assert_called_once_with(expected_subject, expected_body, email)