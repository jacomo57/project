import datetime
import hashlib
from Project import Data


def main():
    gen = Block()
    print(gen)
    block2 = Block(gen.index + 1, gen.get_hash(), "This is block2")
    print(block2)



class Block:
    def __init__(self, index=0, prev_hash=0, data=0):
        self.index = index
        self.prev_hash = prev_hash
        self.timestamp = self.get_time_stamp()
        self.data = data
        self.curr_hash = self.get_hash()# Need to find correct encryption for me, add key to here/user.
        # self.key = 0 if genesis else self.get_key()  # Supposed to be proof I was in previous blocks.


    def get_hash(self):
        return hashlib.sha256(str(self.data).encode()).hexdigest()

    def get_key(self):  # Everytime I am in block user gets key from block, then key is needed to decode next block.
        return 1

    def get_time_stamp(self):
        return datetime.datetime.now()

    def __str__(self):
        return "Index " + str(self.index) + " Previous Hash: " + str(self.prev_hash) + " Time Stamp: " + str(self.timestamp) + " Addresses: " + \
               str(self.data) + "\nHash: " + str(self.curr_hash)


if __name__ == '__main__':
    main()
