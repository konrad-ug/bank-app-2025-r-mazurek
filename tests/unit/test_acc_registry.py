from src.account import AccountRegistry, Account, CompanyAccount
import pytest
from unittest.mock import patch

@pytest.fixture
def account_registry():
    return AccountRegistry()

@pytest.fixture
def personal_account():
    return Account("Janusz", "Kowalski", "80010100000") 

@pytest.fixture
def other_personal_account():
    return Account("Anna", "Nowak", "90050511111") 

@pytest.fixture
def company_account():
    with patch.object(CompanyAccount, 'verifiy_nip_with_gov_api', return_value=True):
        return CompanyAccount("Budimex", "0123456789")

class TestAccountRegistry:
    
    def test_add_account_adds_to_registry(self, account_registry, personal_account):
        account_registry.add_account(personal_account)

        assert len(account_registry.accounts) == 1
        assert account_registry.accounts[0] is personal_account
        
    def test_add_multiple_accounts(self, account_registry, personal_account, company_account):
        account_registry.add_account(personal_account)
        account_registry.add_account(company_account)
        
        assert len(account_registry.accounts) == 2
        
    def test_add_invalid_account(self, account_registry):
        account_registry.add_account("nie_konto")
        
        assert len(account_registry.accounts) == 0
    
    def test_find_by_pesel_success(self, account_registry, personal_account):
        account_registry.add_account(personal_account)
        
        found_account = account_registry.find_acc_by_pesel("80010100000")
        
        assert found_account is personal_account
        
    def test_find_by_pesel_not_found(self, account_registry, personal_account):
        account_registry.add_account(personal_account)
        
        found_account = account_registry.find_acc_by_pesel("99999999999") 
        
        assert found_account is None
        
    def test_find_by_pesel_empty_registry(self, account_registry):
        found_account = account_registry.find_acc_by_pesel("12345678901")
        assert found_account is None

    def test_add_account_duplicate_pesel(self, account_registry, personal_account, other_personal_account):
        account_registry.add_account(personal_account)
        
        duplicate_account = Account("Duplikat", "Testowy", "80010100000")
        
        account_registry.add_account(duplicate_account) 
        
        assert len(account_registry.accounts) == 1
        
    def test_return_all_empty(self, account_registry):
        assert account_registry.return_all() == []
        
    def test_return_all_multiple(self, account_registry, personal_account, other_personal_account):
        account_registry.add_account(personal_account)
        account_registry.add_account(other_personal_account)
        
        assert account_registry.return_all() == [personal_account, other_personal_account]
        
    def test_return_amount_empty(self, account_registry):
        assert account_registry.return_amount() == 0
        
    def test_return_amount_multiple(self, account_registry, personal_account, other_personal_account):
        account_registry.add_account(personal_account)
        account_registry.add_account(other_personal_account)
        
        assert account_registry.return_amount() == 2