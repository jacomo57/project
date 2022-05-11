import datetime
import hashlib


def main():
    gen = Block()
    print(gen)
    block2 = Block("This is block2", gen.get_hash())
    print(block2)


class Block:
    def __init__(self, data, prev_hash=0, my_prime=2):
        self.prev_hash = prev_hash
        self.timestamp = self.get_time_stamp()
        self.data = data  # Only addresses
        self.my_prime = my_prime
        self.hash = self.get_hash()  # Previous hash * my_prime
        self.children = []

    def get_hash(self):
        if self.prev_hash == 0:
            return hashlib.sha256(self.data.encode()).hexdigest() * self.my_prime
        else:
            return self.prev_hash * self.my_prime

    @staticmethod
    def get_time_stamp():
        return datetime.datetime.now()

    def __str__(self):
        return f"Prime: {self.my_prime} Time Stamp: {self.timestamp} Addresses: {self.data}"

    def make_sub_block(self, data, prime):
        block = Block(data, self.hash, prime)
        self.children.append(block)
        return block

    def doit(self):
        print(f"Block Info - {self}, I have {len(self.children)} children")


if __name__ == '__main__':
    main()
