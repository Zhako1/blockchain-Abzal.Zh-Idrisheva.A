class UTXO:
    def __init__(self):
        self.utxos = {}
        self.initial_balance = 100

    def create_utxo(self, transaction):
        if transaction.sender not in self.utxos:
            self.utxos[transaction.sender] = self.initial_balance
        if self.utxos[transaction.sender] >= transaction.amount + transaction.fee:
            self.utxos[transaction.sender] -= (transaction.amount + transaction.fee)
            self.utxos[transaction.recipient] = self.utxos.get(transaction.recipient, 0) + transaction.amount
            return True
        return False
