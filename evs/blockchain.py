import hashlib
import time
from .models import Block

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_data = []
        self.create_block(nonce=0, previous_hash='0')

    def create_block(self, nonce, previous_hash):
        block = Block.objects.create(
            hash_code='',
            previous_block=None,
            data='',
            nonce=str(nonce),
        )
        self.current_data = []
        self.chain.append(block)
        return block

    def add_block_data(self, data):
        self.current_data.append(data)

    def hash_block(self, block):
        encoded_block = (
            str(block.id)
            + str(block.data)
            + str(block.nonce)
        )
        hash_value = hashlib.sha256(encoded_block.encode()).hexdigest()
        return hash_value

    def proof_of_work(self, block, leading_zeros):
        while True:
            block.nonce = str(int(block.nonce) + 1)
            hash_value = self.hash_block(block)
            if hash_value[:leading_zeros] == '0' * leading_zeros:
                break
        return hash_value

    def add_block(self, data, leading_zeros):
        previous_block = self.chain[-1]
        previous_hash = self.hash_block(previous_block)
        new_block = self.create_block(nonce=0, previous_hash=previous_hash)
        self.add_block_data(data)
        new_block.nonce = self.proof_of_work(new_block, leading_zeros)

        # Recalculate the hash using the updated nonce value
        new_block.hash_code = format(int(self.hash_block(new_block), 16), '0{}x'.format(leading_zeros))

        return new_block
