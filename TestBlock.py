from Project.Block import Block


def main():
    gen = TestBlock()
    print(gen)
    block2 = TestBlock(gen.index + 1, gen.get_hash(), "This is block2")
    print(block2)


class TestBlock(Block): #index=0, prev_hash=0, data=0, curr_hash=0
    def next(self):
        pass



if __name__ == '__main__':
    main()