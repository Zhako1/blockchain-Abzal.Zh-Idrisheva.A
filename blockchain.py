from block import Block
from transaction import Transaction
from utxo import UTXO
import json

class Blockchain:
    def __init__(self):
        self.chain = []
        self.utxo = UTXO()  # Инициализация UTXO

    def add_block(self, transaction):
        if self.validate_transaction(transaction):
            new_block = Block([transaction], self.get_last_block_hash())
            self.chain.append(new_block)
            return True
        return False

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            json.dump([block.to_dict() for block in self.chain], f, default=str)

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            blocks = json.load(f)
            for block_data in blocks:
                block = Block(
                    transactions=[Transaction(**tx) for tx in block_data['transactions']],
                    previous_hash=block_data['previous_hash']
                )
                self.chain.append(block)

    def validate_transaction(self, transaction):
        return self.utxo.create_utxo(transaction)

    def get_last_block_hash(self):
        if not self.chain:
            return ''
        return self.chain[-1].hash  # Предполагается, что у класса Block есть атрибут hash

    def get_balance(self, address):
        return self.utxo.utxos.get(address, 0)  # Получение баланса через UTXO

    def get_blocks(self):
        return self.chain  # Возвращает все блоки
