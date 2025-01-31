import json
from block import Block
from utxo import UTXO
from transaction import Transaction

class Blockchain:
    def __init__(self):
        self.chain = [Block([])]
        self.utxo = UTXO()
        self.load_transactions()

    def add_block(self, transaction):
        if self.validate_transaction(transaction):
            previous_block = self.chain[-1]
            new_block = Block([transaction], previous_block.hash)
            self.chain.append(new_block)
            self.save_transactions()
            return True
        return False

    def validate_transaction(self, transaction):
        return self.utxo.create_utxo(transaction)

    def save_transactions(self):
        with open('transactions.json', 'w') as f:
            transactions = [tx.to_dict() for block in self.chain for tx in block.transactions]
            json.dump(transactions, f)

    def load_transactions(self):
        try:
            with open('transactions.json', 'r') as f:
                transactions = json.load(f)
                for tx_data in transactions:
                    transaction = Transaction(tx_data['sender'], tx_data['recipient'], tx_data['amount'], tx_data['fee'])
                    self.add_block(transaction)
        except FileNotFoundError:
            pass
