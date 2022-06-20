from Block import Block


class BlockFile(Block):
    def __init__(self, block_name, prev_hash, prime, pickled_file, father_name, address=0):
        super().__init__(("file_" + block_name), prev_hash, prime, father_name, address)
        self.pickled_file = pickled_file
