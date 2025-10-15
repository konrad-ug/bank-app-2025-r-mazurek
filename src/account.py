import re

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
        self.balance = 0
        self.pesel = pesel if len(pesel) == 11 else "Invalid"
        if promo_code:
            if Utilities.qualifies_for_promo(promo_code, self.pesel):
                self.balance += 50
            
                