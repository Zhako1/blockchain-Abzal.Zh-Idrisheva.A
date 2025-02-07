import datetime
from merkle_tree import MerkleTree
from transaction import Transaction
from manual_hash import manual_hash

class Block:
    def __init__(self, transactions, previous_hash=''):
        self.transactions = transactions
        self.timestamp = datetime.datetime.now()
        self.previous_hash = previous_hash
        self.merkle_root = self.calculate_merkle_root()
        self.hash = self.calculate_hash()


    def calculate_merkle_root(self):
        if not self.transactions:
            return ''
        transaction_hashes = [tx.transaction_hash for tx in self.transactions]
        merkle_tree = MerkleTree(transaction_hashes)
        return merkle_tree.root.hash_value

    def calculate_hash(self):
        block_data = f"{self.merkle_root}{self.timestamp}{self.previous_hash}"
        return manual_hash(block_data)

    def to_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),  # Преобразуем в строку
            "previous_hash": self.previous_hash,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "hash": self.hash
        }
