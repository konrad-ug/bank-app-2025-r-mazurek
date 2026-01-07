import math, re, os, requests
from datetime import datetime
from smtp.smtp import SMTPClient

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
    def __init__(self, first_name: str, last_name: str, pesel: str, promo_code: str = None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0.0
        self.express_transfer_fee = 1.0
        self.pesel = (pesel if len(pesel) == 11 else "Invalid") if pesel else None
        if promo_code:
            if Utilities.qualifies_for_promo(promo_code, self.pesel):
                self.balance += 50
        self.history: list[float] = []
        
    def get_express_transfer_fee(self) -> float:
        return self.express_transfer_fee    
    
    def add_to_acc_history(self, transaction):
        if isinstance(transaction, float) or isinstance(transaction, int):
            self.history.append(transaction)        
    
    def receive_transfer(self, amount: float):
        if amount <= 0:
            print(f"Invalid receive_transfer amount: {amount}")
            return
        self.balance += amount
        self.add_to_acc_history(amount)
    def send_transfer(self, amount: float) -> bool:
        if amount <= 0:
            print(f"Invalid transfer amount: ${amount}")
            return False
        if self.balance - amount < 0:
            print("Balance of ${self.balance} is too small to send a ${amount} transfer.")
            return False
        
        self.balance -= amount
        self.add_to_acc_history(-amount)
        return True
    def send_express_transfer(self, amount: float):
        if amount <= 0:
            print(f"Invalid transfer amount of ${amount}")
            return
        if self.balance - amount < 0:
            print("Balance of ${self.balance} is too small to send a ${amount} transfer.")
            return
        
        self.balance -= amount + self.get_express_transfer_fee()
        self.add_to_acc_history(-amount)
        self.add_to_acc_history(-self.get_express_transfer_fee())
        
    def apply_for_loan(self, amount: float) -> bool:
        if not self.pesel:
            return False
        elif len(self.history) < 3:
            return False
        elif len(self.history) < 5:
            for entry in self.history[-3:]:
                if entry <= 0:
                    return False
            self.balance += amount
            return True
        else:
            historical_transaction_sum = sum(self.history[-5:])
            if historical_transaction_sum > amount:
                self.balance += amount
                return True
            else:
                return False
    def send_history_via_email(self, email: str) -> bool:
        today = datetime.now().strftime("%Y-%m-%d")
        if SMTPClient.send(f"Account Transfer History {today}",
                        f"Personal account history: {self.history}",
                        email):
            return True
        return False
        
    
class CompanyAccount(Account): # pragma: no cover
    def __init__(self, company_name: str, nip: str):
        super().__init__(first_name = None, last_name = None, pesel = None, promo_code = None)
        
        self.express_transfer_fee = 5.0
        self.company_name = company_name if isinstance(company_name, str) else "Invalid"
        if isinstance(nip, str) and len(nip) == 10:
            if self.verifiy_nip_with_gov_api(nip):
                self.nip = nip
            else:
                raise ValueError("Company not registered!!")
        else:
            self.nip = "Invalid"

    def verifiy_nip_with_gov_api(self, nip: str) -> bool:
        base_url = os.environ.get("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl/")
        today = datetime.now().strftime("%Y-%m-%d")
        url = f"{base_url}api/search/nip/{nip}?date={today}"

        try:
            response = requests.get(url, timeout=5)
            print(f"Api nip verify reponse: {response.text}")

            if response.ok:
                data = response.json()
                if data.get("result") and data["result"].get("subject"):
                    return data["result"]["subject"]["statusVat"] == "Czynny"

            return False

        except Exception as e:
            print(f"Error requesting gov api for nip verification: {e}")
            return False
    
    def apply_for_loan(self, amount):
        if self.balance >= amount * 2 and -1775 in self.history:
            self.balance += amount
            return True
        return False

    def send_history_via_email(self, email: str) -> bool:
        today = datetime.now().strftime("%Y-%m-%d")
        if SMTPClient.send(f"Account Transfer History {today}",
                        f"Company account history: {self.history}",
                        email):
            return True
        return False
    
class AccountRegistry:
    def __init__(self):
        self.accounts: list[Account] = []
    
    def add_account(self, account: Account):
        if not isinstance(account, Account) or account in self.accounts:
            return
        for acc in self.accounts:
            if acc.pesel == account.pesel:
                return
        self.accounts.append(account)
    
    def find_acc_by_pesel(self, pesel: str) -> Account:
        if not isinstance(pesel, str): return None
        for acc in self.accounts:
            if acc.pesel == pesel:
                return acc
        return None

    def delete_acc_by_pesel(self, pesel: str):
        if not isinstance(pesel, str): return
        for acc in self.accounts:
            if acc.pesel == pesel:
                self.accounts.remove(acc)
                return
    
    def return_all(self) -> list[Account]:
        return self.accounts
    
    def return_amount(self) -> int:
        return len(self.accounts)