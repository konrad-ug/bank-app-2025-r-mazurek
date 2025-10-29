from src.account import CompanyAccount

class TestAccCreation: 
    def test_acc_creation(self):
        companyName = "Firma1"
        companyNIP = "0123456789"
        companyAccount = CompanyAccount(companyName, companyNIP)
        
        assert companyAccount.company_name == companyName
        assert companyAccount.nip == companyNIP
        assert companyAccount.balance == 0
    
    def test_acc_creation_invalid_nip(self):
        companyName = "Firma1"
        companyNIP = "01234567890"
        companyAccount = CompanyAccount(companyName, companyNIP)
        
        assert companyAccount.nip == "Invalid"
    
    def test_acc_creation_invalid_company_name(self):
        companyName = 12
        companyNIP = "0123456789"
        companyAccount = CompanyAccount(companyName, companyNIP)
        
        assert companyAccount.company_name == "Invalid"
        
    def test_acc_creation_invalid_nip_and_company_name(self):
        companyName = 12
        companyNIP = "01234567890"
        companyAccount = CompanyAccount(companyName, companyNIP)
        
        assert companyAccount.nip == "Invalid"
        assert companyAccount.company_name == "Invalid"
        
class TestAccOperations:

    def test_send_transfer(self):
        companyName = "Firma1"
        companyNIP = "0123456789"
        account = CompanyAccount(companyName, companyNIP)
        
        account.balance = 1010
        transfer_amount = 1000
        balance_before = account.balance
        account.send_transfer(transfer_amount)
        balance_after = account.balance
        
        assert balance_after == balance_before - transfer_amount
        
    def test_receive_transfer(self):
        companyName = "Firma1"
        companyNIP = "0123456789"
        account = CompanyAccount(companyName, companyNIP)
        
        transfer_amount = 1000
        balance_before = account.balance
        account.receive_transfer(transfer_amount)
        balance_after = account.balance
        
        assert balance_after == balance_before + transfer_amount
        
    def test_send_negative_transfer(self):
        companyName = "Firma1"
        companyNIP = "0123456789"
        account = CompanyAccount(companyName, companyNIP)
        transfer_amount = -10
        balance_before = account.balance
        account.send_transfer(transfer_amount)
        balance_after = account.balance
        
        assert balance_after == balance_before
        
    def test_send_transfer_insufficient_funds(self):
        companyName = "Firma1"
        companyNIP = "0123456789"
        account = CompanyAccount(companyName, companyNIP)
        transfer_amount = 1000
        account.balance = 100
        balance_before = account.balance
        account.send_transfer(transfer_amount)
        balance_after = account.balance
        
        assert balance_before == balance_after
        
    def test_receive_negative_transfer(self):
        companyName = "Firma1"
        companyNIP = "0123456789"
        account = CompanyAccount(companyName, companyNIP)
        transfer_amount = -10
        balance_before = account.balance
        account.receive_transfer(transfer_amount)
        balance_after = account.balance
        
        assert balance_after == balance_before
        
class TestAccExpressOperations:
    def test_express_transfer_send(self):
        account = CompanyAccount("Firma1", "0123456789")
        account.balance = 1000
        
        transfer_amount = 900
        transfer_fee = account.get_express_transfer_fee()
        balance_before = account.balance
        account.send_express_transfer(900)
        
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
    def test_acc_history(self):
        account = CompanyAccount("Firma1", "0123456789")
        account.balance = 1000
        
        account.send_transfer(100)
        
        assert account.history == [-100.00]
        
        account.receive_transfer(150)
        
        assert account.history == [-100.00, 150.00]
        
        account.send_express_transfer(45)
        
        assert account.history == [-100, 150, -45, -account.get_express_transfer_fee()]