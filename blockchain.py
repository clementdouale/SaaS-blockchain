import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []  # List to store our blockchain
        self.current_transactions = []  # List to store transactions before they are added to a new block
        self.new_block(previous_hash='1', proof=100)  # Create the genesis block

    def new_block(self, proof, previous_hash=None):
        # Creates a new Block and adds it to the chain
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),  # Current time
            'transactions': self.current_transactions,  # Transactions to be added
            'proof': proof,  # Proof given by the Proof of Work algorithm
            'previous_hash': previous_hash or self.hash(self.chain[-1]),  # Hash of the previous block
        }
        self.current_transactions = []  # Reset the list of transactions
        self.chain.append(block)  # Add the block to the chain
        return block

    def new_transaction(self, sender, recipient, amount):
        # Adds a new transaction to the list of transactions
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1  # The index of the block that will hold this transaction

    @staticmethod
    def hash(block):
        # Hashes a Block
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        # Simple Proof of Work Algorithm:
        # - Find a number p' such that hash(pp') contains 4 leading zeroes
        # - p is the previous proof, and p' is the new proof
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        # Validates the Proof
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"  # Check if hash has 4 leading zeroes
