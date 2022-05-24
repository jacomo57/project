from Block import Block


class BlockFolder(Block):
    def __init__(self, block_name, prev_hash=None, prime=None, address=0):
        if prev_hash:
            super().__init__(block_name, prev_hash, prime)
        else:
            super().__init__(block_name)
        self.address = address  # Will get from server repository later.

    def make_sub_block(self, block_name, prime, address):  # Need to check the type of block and create accordingly.
        block = BlockFolder(block_name, self.hash, prime, address)
        self.children.append(block)
        return block
