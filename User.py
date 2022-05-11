from Block import Block
import Client
import socket


def main():
    user = User("Jacomo", "pswd", 1727, socket.socket(socket.AF_INET, socket.SOCK_STREAM), 2)
    user.my_socket.send_user("createuser$" + user.user_name + "$" + user.password)
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
    user.block.doit()
    user.traverse(user.block)


class User:
    def __init__(self, user_name, password, port, my_socket, pre_len):
        self.prime_limit = 100
        self.prime_array = self.make_prime_array(1, self.prime_limit)
        self.curr_prime_index = 0
        self.user_name = user_name
        self.password = password
        # self.block = Block(user_name + password)
        self.port = port
        self.my_socket = my_socket
        self.pre_len = pre_len

    def connect(self):
        self.my_socket.connect(('127.0.0.1', self.port))
        print("Connection established")

    def send_user(self):
        self.protocol_message(self.user_name + "," + self.password, True)

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

    def protocol_message(self, message, is_text):
        length_msg = len(message)
        length_msg_str = str(length_msg)

        length_length = len(length_msg_str)
        length_length_str = str(length_length).zfill(2)

        self.my_socket.send(length_length_str.encode())

        self.my_socket.send(length_msg_str.encode())

        if is_text:
            self.my_socket.send(message.encode())
        else:
            self.my_socket.send(message)

    def recv_message(self):
        length_length_str = self.my_socket.recv(2)
        if length_length_str == "":
            pass
        length_length_str = length_length_str.decode()
        length_length = int(length_length_str)

        msg_length_str = self.my_socket.recv(length_length).decode()
        msg_length = int(msg_length_str)

        message = self.my_socket.recv(int(msg_length))
        while len(message) < int(msg_length):
            message += self.my_socket.recv(int(message) - len(message))
        return message.decode()


if __name__ == '__main__':
    main()
