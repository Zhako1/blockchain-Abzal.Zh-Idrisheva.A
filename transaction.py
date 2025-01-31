from manual_hash import manual_hash

class Transaction:
    def __init__(self, sender, recipient, amount, fee):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.fee = fee
        self.transaction_hash = self.calculate_hash()

    def calculate_hash(self):
        transaction_data = f"{self.sender}{self.recipient}{self.amount}{self.fee}"
        return manual_hash(transaction_data)

    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "fee": self.fee,
            "transaction_hash": self.transaction_hash
        }
