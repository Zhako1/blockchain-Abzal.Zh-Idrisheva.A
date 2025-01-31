from manual_hash import manual_hash

class MerkleNode:
    def __init__(self, left=None, right=None, hash_value=''):
        self.left = left
        self.right = right
        self.hash_value = hash_value

class MerkleTree:
    def __init__(self, transactions):
        self.root = self.build_tree(transactions)

    def build_tree(self, transactions):
        if len(transactions) == 0:
            return None
        if len(transactions) == 1:
            return MerkleNode(hash_value=manual_hash(transactions[0]))

        hashed_transactions = [manual_hash(tx) for tx in transactions]

        while len(hashed_transactions) > 1:
            if len(hashed_transactions) % 2 != 0:
                hashed_transactions.append(hashed_transactions[-1])  # Duplicate last hash if odd
            new_level = []
            for i in range(0, len(hashed_transactions), 2):
                combined_hash = hashed_transactions[i] + hashed_transactions[i + 1]
                new_level.append(manual_hash(combined_hash))
            hashed_transactions = new_level

        return MerkleNode(hash_value=hashed_transactions[0])
