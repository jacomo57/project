from Block import Block
from BlockFile import BlockFile


class BlockFolder(Block):
    def __init__(self, block_name, prev_hash=None, prime=None, father_name=0, address=0):
        if prev_hash:
            super().__init__(block_name, prev_hash, prime, father_name)
        else:
            super().__init__(block_name)
        self.address = address
        self.children = []

    def make_sub_block(self, block_name, prime, father_name, address):
        block = BlockFolder(block_name, self.hash, prime, father_name, address)
        self.children.append(self.metadata(block_name, address, self.block_name))
        return block

    def make_sub_file(self, block_name, prime, pickeld_file, father_name, address=0):
        block = BlockFile(block_name, self.hash, prime, pickeld_file, father_name)
        self.children.append(self.metadata(("file_" + block_name), address, self.block_name))
        print(self.children)
        return block

    def metadata(self, child_name, address, dad_name):  # When creating child, pass child name+address and save to self.children
        metadata = [child_name, address, dad_name]
        return metadata

    def __str__(self):
        return f"Name: {self.block_name}, Prime: {self.my_prime}, Address: {self.address} Time Stamp: {self.timestamp}, {len(self.children)} children"
