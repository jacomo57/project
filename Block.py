import datetime
import hashlib


class Block:
    def __init__(self, block_name, prev_hash=0, my_prime=2, father_name=0, address=0):
        self.prev_hash = prev_hash
        self.timestamp = self.get_time_stamp()
        self.my_prime = my_prime
        if prev_hash == 0:
            self.block_name = "gen_" + block_name
        else:
            self.block_name = block_name
        self.hash = self.get_hash(block_name)  # Previous hash * my_prime
        self.address = address
        self.father_name = father_name

    def get_hash(self, block_name):
        if self.prev_hash == 0:
            return hashlib.sha256(block_name.encode()).hexdigest()
        else:
            return self.prev_hash

    @staticmethod
    def get_time_stamp():
        return datetime.datetime.now()

    def __str__(self):
        return f"Name: {self.block_name}, Prime: {self.my_prime}, Time Stamp: {self.timestamp}"

    def __repr__(self):
        return f"Block Info - {self}"