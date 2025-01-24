from block import Block

class Blockchain:
    def __init__(self):
        self.chain = [Block("Генезис блогы")]

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = Block(data, previous_block.hash)
        self.chain.append(new_block)

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.previous_hash != previous_block.hash:
                return False
            if current_block.hash != current_block.calculate_hash():
                return False
        return True

if __name__ == "__main__":
    from block import Block
    blockchain = Blockchain()
    blockchain.add_block("Блок 1")
    blockchain.add_block("Блок 2")
    for block in blockchain.chain:
        print(f"Блок: {block.hash}, Деректер: {block.data}")
