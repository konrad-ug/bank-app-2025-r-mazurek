import math, re

class Utilities:
    @staticmethod
    def get_birth_year_from_pesel(pesel: str) -> int:
        birth_year = int(pesel[:2])
        century = 1900 if int(pesel[2:4]) <= 12 else 2000
        return birth_year + century
    
    @staticmethod
    def qualifies_for_promo(promo_code: str, pesel: str) -> bool:
        valid_promo_code_pattern = r"PROMO_.{3}"
        if re.fullmatch(valid_promo_code_pattern, promo_code.strip()):
            if Utilities.get_birth_year_from_pesel(pesel) > 1960:
                return True
            else:
                print("Age outside of promo requirements")
        else:
            print("invalid promo code was given")
        return False
    

class Account:
    def __init__(self, first_name, last_name, pesel, promo_code = None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0.0
        self.express_transfer_fee = 1.0
        self.pesel = (pesel if len(pesel) == 11 else "Invalid") if pesel else None
        if promo_code:
            if Utilities.qualifies_for_promo(promo_code, self.pesel):
                self.balance += 50
    def get_express_transfer_fee(self) -> float:
        return self.express_transfer_fee            
    
    def receive_transfer(self, amount: float):
        if amount <= 0:
            print(f"Invalid receive_transfer amount: {amount}")
            return
        self.balance += amount
    def send_transfer(self, amount: float):
        if amount <= 0:
            print(f"Invalid transfer amount: ${amount}")
            return
        if self.balance - amount < 0:
            print("Balance of ${self.balance} is too small to send a ${amount} transfer.")
            return
        
        self.balance -= amount
    def send_express_transfer(self, amount: float):
        if amount <= 0:
            print(f"Invalid transfer amount of ${amount}")
            return
        if self.balance - amount < 0:
            print("Balance of ${self.balance} is too small to send a ${amount} transfer.")
            return
        
        self.balance -= amount + self.get_express_transfer_fee()
    
class CompanyAccount(Account):
    def __init__(self, company_name: str, nip: str):
        super().__init__(first_name = None, last_name = None, pesel = None, promo_code = None)
        
        self.express_transfer_fee = 5.0
        self.nip = nip if type(nip) == str and len(nip) == 10 else "Invalid"
        self.company_name = company_name if type(company_name) == str else "Invalid"