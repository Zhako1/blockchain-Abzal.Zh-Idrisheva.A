import datetime
from merkle_tree import MerkleTree
from transaction import Transaction
from manual_hash import manual_hash

class Block:
    def __init__(self, transactions, previous_hash='', difficulty=2):
        self.transactions = [Transaction(**tx) if isinstance(tx, dict) else tx for tx in transactions]
        self.timestamp = datetime.datetime.now()
        self.previous_hash = previous_hash
        self.merkle_root = self.calculate_merkle_root()
        self.hash = self.calculate_hash()
        self.difficulty = difficulty


    def calculate_merkle_root(self):
        if not self.transactions:
            return ''
        transaction_hashes = [tx.transaction_hash for tx in self.transactions]
        merkle_tree = MerkleTree(transaction_hashes)
        return merkle_tree.root.hash_value

    def calculate_hash(self):
        block_data = f"{self.merkle_root}{self.timestamp}{self.previous_hash}"
        return manual_hash(block_data)
        
    def mine_block(self, difficulty, miner_address):
        nonce = 0
        while True:
            block_data = f"{self.merkle_root}{self.timestamp}{self.previous_hash}{nonce}{miner_address}"
            block_hash = manual_hash(block_data)  
            if block_hash[:difficulty] == "0" * difficulty:  
                self.hash = block_hash
                return nonce
            nonce += 1

    def to_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(), 
            "previous_hash": self.previous_hash,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "hash": self.hash
        }
