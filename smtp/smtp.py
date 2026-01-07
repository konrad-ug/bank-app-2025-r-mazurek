class SMTPClient: #
    @staticmethod
    def send(self, subject: str, text: str, email_address: str) -> bool:
        ## mock send
        if isinstance(email_address, str):
            return True
        return False