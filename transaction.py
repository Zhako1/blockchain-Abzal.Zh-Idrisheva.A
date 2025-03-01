from manual_hash import manual_hash
import logging

class Transaction:
    def __init__(self, sender, recipient, amount, fee, transaction_hash=None, signature=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.fee = fee
        self.transaction_hash = transaction_hash or self.calculate_hash()
        self.signature = signature
        self.is_verified_logged = False

    def calculate_hash(self):
        transaction_data = f"{self.sender}{self.recipient}{self.amount}{self.fee}"
        return manual_hash(transaction_data)

    def sign_transaction(self, private_key):
        transaction_data = f"{self.sender}{self.recipient}{self.amount}{self.fee}"
        data_to_hash = transaction_data + str(private_key[1])
        hashed_data = int(manual_hash(data_to_hash), 16) % private_key[1]  # Делаем число <= N
        self.signature = hex(pow(hashed_data, private_key[0], private_key[1]))[2:]  

    def verify_signature(self, public_key):
        transaction_data = f"{self.sender}{self.recipient}{self.amount}{self.fee}"
        data_to_hash = transaction_data + str(public_key[1])
        expected_hash = int(manual_hash(data_to_hash), 16) % public_key[1]  # Снова ограничиваем число
        decrypted_signature = pow(int(self.signature, 16), public_key[0], public_key[1])  # Расшифровка

        if decrypted_signature == expected_hash:
            if not self.is_verified_logged:  # Проверяем флаг
                logging.info("Подпись верна.")
                self.is_verified_logged = True
            return True
        else:
            logging.info("[VERIFY] Подпись неверна.")
            return False

    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "fee": self.fee,
            "transaction_hash": self.transaction_hash,
            "signature": self.signature
        }
