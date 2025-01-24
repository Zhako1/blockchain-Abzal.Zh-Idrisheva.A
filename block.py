import datetime
from manual_hash import manual_hash

class Block:
    def __init__(self, data, previous_hash=''):
        self.data = data
        self.timestamp = datetime.datetime.now()
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = f"{self.data}{self.timestamp}{self.previous_hash}"
        return manual_hash(block_data)

if __name__ == "__main__":
    block = Block("Блок мысалы", "12345")
    print(f"Хэш блока: {block.hash}")
