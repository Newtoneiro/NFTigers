import hashlib


class Block:
    def __init__(self, transactions, previous_hash):
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(
            str(self.transactions).encode('utf-8')
            + str(self.previous_hash).encode('utf-8')
        )
        return sha.hexdigest()

    def is_valid(self):
        if self.hash != self.calculate_hash():
            return False
        return True

    def get_hash(self):
        return self.hash
