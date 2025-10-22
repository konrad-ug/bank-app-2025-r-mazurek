from src.account import Account

class TestAccCreation:
    def test_account_creation(self):
        account = Account("John", "Doe", "12345678910")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0
        assert account.pesel == "12345678910"
        
    def test_acc_creation_invalid_pesel(self):
        account_no_pesel = Account("John", "Doe", "1234567891011")
        assert account_no_pesel.pesel == "Invalid"
        account_pesel_too_short = Account("John", "Doe", "123")
        assert account_pesel_too_short.pesel == "Invalid"
        account_pesel_too_long = Account("John", "Doe", "1234567891011")
        assert account_pesel_too_long.pesel == "Invalid"
        
    def test_acc_creation_with_promo_code(self):
        account_valid_promo = Account("John", "Doe", "12345678910", "PROMO_XYZ")
        assert account_valid_promo.balance == 50
        account_valid_promo_2 = Account("John", "Doe", "12345678910", "PROMO_HSA")
        assert account_valid_promo_2.balance == 50
        account_space_before_promo_code = Account("John", "Doe", "12345678910", " PROMO_XYZ")
        assert account_space_before_promo_code.balance == 50
        account_space_after_promo_code = Account("John", "Doe", "12345678910", "PROMO_XYZ  ")
        assert account_space_after_promo_code.balance == 50
        account_invalid_promo_too_short = Account("John", "Doe", "12345678910", "PROMO_HJ")
        assert account_invalid_promo_too_short.balance == 0
        account_invalid_promo_too_short_2= Account("John", "Doe", "12345678910", "PROMO_X")
        assert account_invalid_promo_too_short_2.balance == 0
        account_invalid_promo_too_short_3= Account("John", "Doe", "12345678910", "PROMO_")
        assert account_invalid_promo_too_short_3.balance == 0
        account_promo_code_spaces_only = Account("John", "Doe", "12345678910", "PROMO_   ")
        assert account_promo_code_spaces_only.balance == 0
        account_invalid_promo_too_long = Account("John", "Doe", "12345678910", "PROMO_ZXCV")
        assert account_invalid_promo_too_long.balance == 0
        account_invalid_promo_too_long2 = Account("John", "Doe", "12345678910", "PROMO_ZOHJASDJOIXCV")
        assert account_invalid_promo_too_long2.balance == 0
        
        account_valid_promo_too_old = Account("John", "Doe", "59123456789", "PROMO_XYZ")
        assert account_valid_promo_too_old.balance == 0
        
class TestAccOperations:
    def test_send_transfer(self):
        account = Account("John", "Doe", "1234567819")
        account.balance = 1010
        transfer_amount = 1000
        balance_before = account.balance
        account.send_transfer(transfer_amount)
        balance_after = account.balance
        
        assert balance_after == balance_before - transfer_amount
        
    def test_receive_transfer(self):
        account = Account("John", "Doe", "1234567819")
        transfer_amount = 1000
        balance_before = account.balance
        account.receive_transfer(transfer_amount)
        balance_after = account.balance
        
        assert balance_after == balance_before + transfer_amount
        
    def test_send_negative_transfer(self):
        account = Account("John", "Doe", "1234567819")
        transfer_amount = -10
        balance_before = account.balance
        account.send_transfer(transfer_amount)
        balance_after = account.balance
        
        assert balance_after == balance_before
        
    def test_receive_negative_transfer(self):
        account = Account("John", "Doe", "1234567819")
        transfer_amount = -10
        balance_before = account.balance
        account.receive_transfer(transfer_amount)
        balance_after = account.balance
        
        assert balance_after == balance_before

class TestAccExpressOperations:
    def test_express_transfer_send(self):
        account = Account("John", "Doe", "12345678910")
        account.balance = 1000
        
        transfer_amount = 900
        transfer_fee = account.get_express_transfer_fee()
        balance_before = account.balance
        account.send_express_transfer(900)
        
        assert account.balance == balance_before - (transfer_amount + transfer_fee)
        
        account.balance = 100
        account.send_express_transfer(account.balance)
        
        assert account.balance == -account.get_express_transfer_fee()
        