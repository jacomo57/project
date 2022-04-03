from Block import Block
import socket


def main():
    user = User("Jacomo", "pswd")
    print(user.user_name)
    print(user.password)
    print(user.prime_array)
    block1 = user.block.make_sub_block("data2", user.get_next_prime())
    block2 = user.block.make_sub_block("data3", user.get_next_prime())
    # SECOND STEP BLOCK2
    block21 = block2.make_sub_block("data4", user.get_next_prime())
    block22 = block2.make_sub_block("data5", user.get_next_prime())
    # THIRD STEP BLOCK 22
    block221 = block22.make_sub_block("DESTINATION REACHED", user.get_next_prime())
    user.traverse(user.block)


class User:
    def __init__(self, user_name, password):
        self.prime_limit = 100
        self.prime_array = self.make_prime_array(1, self.prime_limit)
        self.curr_prime_index = 0
        self.user_name = user_name
        self.password = password
        self.block = Block(user_name + password)

    def traverse(self, block):
        for child in block.children:
            child.doit()
            self.traverse(child)

    @staticmethod
    def make_prime_array(lower, upper):
        prime_list = []
        num = 2
        while len(prime_list) < 100:
            prime = True
            if num == 1:
                prime = False
            for i in range(2, num):
                if num % i == 0:
                    prime = False
            if prime:
                prime_list.append(num)
            num += 1
        return prime_list

    def get_next_prime(self):
        self.curr_prime_index += 1
        if self.curr_prime_index > self.prime_limit:
            self.prime_array = self.make_prime_array(self.prime_limit, self.prime_limit + 100)
            self.prime_array += 100
            return self.prime_array[self.curr_prime_index]
        return self.prime_array[self.curr_prime_index]


if __name__ == '__main__':
    main()
