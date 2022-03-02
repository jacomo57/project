

class Blockchain:

    def __init__(self, user):
        self.User = user
        self.block = self.create_genesis_block()

    def create_genesis_block(self): #When creating genesis block will soon need to have user id in it!


