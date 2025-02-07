from manual_hash import manual_hash

class Transaction:
    def __init__(self, sender, recipient, amount, fee, transaction_hash=None, signature=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.fee = fee
        self.transaction_hash = transaction_hash or self.calculate_hash()
        self.signature = signature

    def calculate_hash(self):
        transaction_data = f"{self.sender}{self.recipient}{self.amount}{self.fee}"
        return manual_hash(transaction_data)

    def sign_transaction(self, private_key):
        # Подпись транзакции
        self.signature = private_key[0]  # Упрощено для демонстрации

    def verify_signature(self, public_key):
        # Проверка подписи
        return self.signature == public_key[0]  # Упрощено для демонстрации

    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "fee": self.fee,
            "transaction_hash": self.transaction_hash,
            "signature": self.signature
        }
