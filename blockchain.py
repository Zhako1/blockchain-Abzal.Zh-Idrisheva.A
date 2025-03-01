from block import Block
from transaction import Transaction
from utxo import UTXO
import json
import logging


class Blockchain:
    def __init__(self, wallets):
        self.chain = []
        self.utxo = UTXO()  
        self.wallets = wallets  
        self.chain = []  
        self.mempool = []

    def add_block(self, transaction, miner_address):
        for transaction in block.transactions:
            if not self.validate_transaction(transaction):
                logging.error("Ошибка: Транзакция не прошла валидацию.")
                return False

        nonce = block.mine_block(difficulty, miner_address)  # Передаем miner_address
        logging.info(f"Nonce найден: {nonce}")

        self.chain.append(block)
        logging.info("Блок добавлен! Теперь блоков в цепи: %d", len(self.chain))

        mining_reward = 10  
        total_fee = sum(tx.fee for tx in block.transactions)  
        self.utxo.utxos[miner_address] += (mining_reward + total_fee)  
        logging.info(
            f"Баланс адреса {miner_address} обновлен на {mining_reward + total_fee}. Новый баланс: {self.utxo.utxos[miner_address]}")

        self.save_to_file('blockchain.json')
        return True
        

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            json.dump([block.to_dict() for block in self.chain], f, default=str)
            logging.info(f"Цепочка блоков сохранена в файл: {filename}")

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                blocks = json.load(f)
                for block_data in blocks:
                    block = Block(
                        transactions=[Transaction(**tx) for tx in block_data['transactions']],
                        previous_hash=block_data['previous_hash']
                    )
                    self.chain.append(block)
        except FileNotFoundError:
            logging.error("Файл не найден: %s", filename)
        except json.JSONDecodeError:
            logging.error("Ошибка при чтении файла: %s", filename)
        except Exception as e:
            logging.error("Ошибка при загрузке блоков: %s", str(e))

    def validate_transaction(self, transaction):
        # Проверка наличия средств
        if not self.utxo.create_utxo(transaction):
            logging.warning("Недостаточно средств для транзакции от %s на сумму %s.", transaction.sender, transaction.amount + transaction.fee)
            return False

        # Проверка подписи
        sender_public_key = self.wallets[transaction.sender].get_public_key()
        if not transaction.verify_signature(sender_public_key):
            logging.warning("Подпись транзакции от %s неверна.", transaction.sender)
            return False

        return True

    def get_last_block_hash(self):
        if not self.chain:
            return ''
        return self.chain[-1].hash  # Предполагается, что у класса Block есть атрибут hash

    def add_transaction_to_mempool(self, transaction):
        if self.validate_transaction(transaction):
            self.mempool.append(transaction)  # Добавляем в mempool
            return True
        return False
        
    def get_mempool(self):
        return self.mempool    
    
    def get_balance(self, address):
        return self.utxo.utxos.get(address, 0)  # Получение баланса через UTXO

    def get_blocks(self):
        return self.chain  # Возвращает все блоки

    def resolve_conflicts(self, new_chain):
        if len(new_chain) > len(self.chain):
            self.chain = new_chain
            return True
        return False
