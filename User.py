from Block import Block
from BlockFolder import BlockFolder
from BlockFile import BlockFile
from Globals import Globals
import socket
import pickle
import os


def main():
    user = User("Jacomo", "pswd")
    user.main_loop()


class User:

    def __init__(self, user_name, password, port=0, pre_len=0):
        mem = Globals()
        self.prime_limit = 100
        self.prime_array = self.make_prime_array(1, self.prime_limit)
        self.curr_prime_index = 0
        self.user_name = user_name
        self.password = password
        self.block = None
        self.port = mem.port
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pre_len = mem.pre_len
        self.dir_path = mem.path_used
        self.make_dir_path()

    def main_loop(self):
        close_connection = False
        self.connect()
        start_input = input("Do you want to sign up or log in?")
        if start_input == "sign up":
            self.create_user()
        elif start_input == "log in":
            self.log_in()
        while True:
            message = input("Enter your request")

            if message.__contains__("folder"):
                message = message.split()  # Example of input: 'folder block1'
                self.protocol_message("open address needed", True)
                address = self.recv_message()
                self.create_folder(self.block, address, message[1])  # Need to be able to be on different blocks in tree
            elif message.__contains__("traverse"):
                message = message.split()
                self.traverse(message[-1])
            elif message.__contains__("load"):
                message = message.split()
                block = self.load_block(message[-1])
                print(block)
            else:
                self.protocol_message(message, True)
                answer = self.recv_message().decode()
                print(answer)
                if answer == "Connection closed":
                    close_connection = True
            if close_connection:
                break

        self.my_socket.close()

    def create_folder(self, dad_block, address, folder_name):  # Need to update gen in db and file if gen updated
        block = dad_block.make_sub_block(folder_name, self.get_next_prime(), address)
        self.update_dad_block(dad_block)
        self.protocol_message("")  # Send to server block + username, server updated block in database by name.
        self.dump_block(block)
        print("Folder created")

    def update_dad_block(self, block):  # Removes the block and resaves updated version.
        os.remove(os.path.join(self.dir_path, block.block_name))
        self.dump_block(block)

    def dump_block(self, block):
        file = open(os.path.join(self.dir_path, block.block_name), 'ab')
        pickle.dump(block, file)
        print("File dumped")
        file.close()

    def load_block(self, block_name):
        file = open(os.path.join(self.dir_path, block_name), 'rb')
        block = pickle.load(file)
        print("File loaded")
        file.close()
        return block

    def add_file(self, address, file_name):
        pass

    def make_dir_path(self):
        try:
            os.mkdir(self.dir_path)
        except OSError as error:
            print(error)
        print(f'Directory is in {self.dir_path}')
        return self.dir_path

    def connect(self):
        self.my_socket.connect(('127.0.0.1', self.port))
        print("Connection established")

    def log_in(self):
        while True:
            username = input("Username: ")
            password = input("Password: ")
            # I want this to open file explorer and i could pick gen block.
            if self.verify_log_in(username, password):
                print("Logged in")
                break
            else:
                print("One or more credentials are incorrect, please try again.")
            break

    def verify_log_in(self, username, password):
        self.protocol_message(f'login${username}${password}', True)
        print("Message sent to server")
        if self.recv_message().decode() == "Send Block":
            print("In send block if")
            block_gen = self.load_block("Genesis_" + username)
            self.protocol_message(pickle.dumps(block_gen), False)
            answer = self.recv_message().decode()
            print(answer)
            if answer == "Correct":
                self.block = block_gen
                return True
            if answer == "Incorrect": return False
        else:
            return False

    def create_user(self):  # Needs to receive gen from server and update self.block
        while True:
            username = input("Username: ")
            password = input("Password: ")
            if self.send_user(username, password):
                break
            else:
                print("This username is already taken, please try another")
            break

    def send_user(self, username, password):
        self.protocol_message(f'createuser${username}${password}', True)
        print("Message sent to server")
        gen = self.recv_message()
        if self.is_pickle_stream(gen):
            gen = pickle.loads(gen)
            self.block = gen
            self.dump_block(gen)
            print(f'User {username} created successfully')
            return True
        else:
            return False

    @staticmethod
    def is_pickle_stream(byte_obj):
        try:
            pickle.loads(byte_obj)
            return True
        except pickle.UnpicklingError:
            return False

    def traverse(self, block_name):  # When block children will be metadata not actual blocks, needs update.
        block_to_traverse = self.load_block(block_name)
        print(block_to_traverse)
        for child in block_to_traverse.children:
            self.traverse(child.block_name)  # Will need to change when children will be metadata.

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
        return message


if __name__ == '__main__':
    main()
