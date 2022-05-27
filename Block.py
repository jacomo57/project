import datetime
import hashlib


def main():
    gen = Block()
    print(gen)
    block2 = Block("This is block2", gen.get_hash())
    print(block2)


class Block:
    def __init__(self, block_name, prev_hash=0, my_prime=2, address=0):
        self.prev_hash = prev_hash
        self.timestamp = self.get_time_stamp()
        self.my_prime = my_prime
        if prev_hash == 0:
            self.block_name = "gen_" + block_name
        else:
            self.block_name = block_name
        self.hash = self.get_hash(block_name)  # Previous hash * my_prime
        self.address = address
        self.children = []

    def get_hash(self, block_name):
        if self.prev_hash == 0:
            return hashlib.sha256(block_name.encode()).hexdigest() * self.my_prime
        else:
            return self.prev_hash * self.my_prime

    def metadata(self, address, child_name):
        metadata = [child_name, address, self.hash]
        return metadata


    @staticmethod
    def get_time_stamp():
        return datetime.datetime.now()

    def __str__(self):
        return f"Name: {self.block_name}, Prime: {self.my_prime}, Time Stamp: {self.timestamp}, {len(self.children)} children"

    def __repr__(self):  # Needs to be abstract/overridden in ancestors.
        return f"Block Info - {self}, {len(self.children)} children"


if __name__ == '__main__':
    main()
