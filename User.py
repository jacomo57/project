import fcntl

from Globals import Globals
import socket
import pickle
import os
from GUI import Toplevel1 as GUI
import tkinter as tk
from UserServer import UserServer
from Networker import Networker


def main():
    user = User()
    user.main_loop()


class User:

    def __init__(self, port=0, pre_len=0):
        mem = Globals()
        self.prime_limit = 100
        self.prime_array = self.make_prime_array(1, self.prime_limit)
        self.curr_prime_index = 0
        self.user_name = 0
        self.block = None
        self.port = mem.port
        self.master_address = ('127.0.0.1', self.port)
        self.my_socket = 0
        self.pre_len = mem.pre_len
        self.dir_path = mem.path_used
        self.make_dir_path()
        self.gui = None
        self.curr_address = 0

    def start_gui(self):
        root = tk.Tk()
        root.protocol('WM_DELETE_WINDOW', root.destroy)  # Creates a toplevel widget.
        top1 = root
        self.gui = GUI(self, top1)

    def main_loop(self):
        self.connect(self.master_address)
        self.start_gui()
        self.my_socket.close()
        return

    def make_userserver(self):
        self.hostname = socket.gethostname()
        self.local_ip = socket.gethostbyname(self.hostname)
        self.protocol_message(self.local_ip, True)

    def exit_program(self):
        self.protocol_message("exit", True)
        answer = self.recv_message().decode()
        if answer == "Connection closed":
            return True
        else:
            return False

    def create_folder(self, dad_block, folder_name, networker):  # Need to update gen in db and file if gen updated
        networker.get_to_work("open address needed", True, self.my_socket)
        new_block = dad_block.make_sub_block((folder_name + self.user_name), self.get_next_prime(),
                                             dad_block.block_name, pickle.loads(networker.answer))
        networker.answer = new_block
        self.update_dad_block(dad_block)
        print("create_folder block ", new_block)
        self.protocol_message(f'update${self.user_name}', True)  #
        if self.recv_message().decode() == "send block":  # updates db if folder is gen's child
            if self.block.block_name.__contains__("gen_"):
                self.protocol_message(pickle.dumps(self.block), False)
        self.dump_block(new_block)
        print("Folder created")
        return new_block

    def check_for_answer(self):
        pass

    def create_file(self, dad_block, file_name, pickled_file):
        self.protocol_message("open address needed", True)
        address = self.recv_message()
        new_block = dad_block.make_sub_file(file_name + self.user_name, self.get_next_prime(), pickled_file,
                                            dad_block.block_name, address)
        print(new_block)
        self.update_dad_block(dad_block)
        self.protocol_message(f'update${self.user_name}', True)
        if self.recv_message().decode() == "send block":  # updates db if folder is gen's child
            if dad_block.block_name.__contains__("gen_"):
                self.protocol_message(pickle.dumps(self.block), False)
        self.dump_block(new_block)
        print("File created")
        return new_block

    def update_dad_block(self, block):  # Removes the block and resaves updated version.
        os.remove(os.path.join(self.dir_path, block.block_name))
        self.dump_block(block)

    def dump_block(self, block, username=0):
        if username != 0:
            file = open(os.path.join(self.dir_path, block.block_name), 'ab')
        else:
            file = open(os.path.join(self.dir_path, block.block_name), 'ab')
        pickle.dump(block, file)
        print(block.block_name, "dumped at ", os.path.join(self.dir_path, block.block_name))
        file.close()

    def load_block(self, block_name, is_gen=False, address=0,):  # Here gives networker work instead of load itself.
        if is_gen:
            if self.check_my_block(block_name):
               file = open(os.path.join(self.dir_path, block_name), 'rb')
               block = pickle.load(file)
               print(block.block_name, "loaded")
               file.close()
               return block
            else:
                print("Not your file to view")
                return
        self.networker.get_to_work()
        # if self.check_my_block(block_name):
        #    file = open(os.path.join(self.dir_path, block_name), 'rb')
        #    block = pickle.load(file)
        #    print(block.block_name, "loaded")
        #    file.close()
        #    return block
        # else:
        #    print("Not your file to view")


    # def begin_create_load_block(self, block_name, address=0):
    #     self.load_block(block_name, address)
    #     self.gui.root.after(1100, self.end_load_block)
    #     pass
    #
    # def end_load_block_and_begin_create_folder(self):
    #     if self.networker.answer is not None:
    #         self.create_folder(self.networker.answer, new_name)

    def check_my_block(self, block_name):  # Check to see if username matches the block selected
        try:
            if block_name.__contains__("gen_"):
                return True
            block_name_len = -(len(self.user_name))
            if block_name[block_name_len:] == self.user_name:
                return True
        except:
            print("No block name entered")
            return False

    def make_dir_path(self):
        try:
            os.mkdir(self.dir_path)
        except OSError as error:
            print(error)
        print(f'Directory is in {self.dir_path}')
        return self.dir_path

    def connect(self, address):
        print("In connect")
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(address)
        self.my_socket.connect((address[0], address[1]))
        print("Connection established")

    def log_in(self, username):
        while True:
            if self.verify_log_in(username):
                self.user_name = username
                return True
                break
            else:
                print("One or more credentials are incorrect, please try again.")
            break
        return False

    def verify_log_in(self, username):
        self.protocol_message(f'login${username}', True)
        if self.recv_message().decode() == "Send Block":
            block_gen = self.load_block("gen_" + username, os.path.join(self.dir_path, "gen_" + username))
            self.protocol_message(pickle.dumps(block_gen), False)
            answer = self.recv_message().decode()
            print(answer)
            if answer == "Correct":
                self.block = block_gen
                return True
            if answer == "Incorrect": return False
        else:
            return False

    def create_user(self, username):
        while True:
            print(username)
            if self.send_user(username):
                self.user_name = username
                return True
                break
            else:
                print("This username is already taken, please try another")
            break
        return False

    def send_user(self, username):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        self.protocol_message(f'createuser${username}${ip_address}', True)
        gen = self.recv_message()
        if self.is_pickle_stream(gen):
            gen = pickle.loads(gen)
            self.block = gen
            self.dump_block(gen, username)
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

    # metadata = [child_name, address, self.hash]
    def traverse(self, child_name, address=0):  # This + load_block will need update when it's separate computers.
        block_to_traverse = self.load_block(child_name, address)  # Address curr useless till seperate pc's.
        print(block_to_traverse)
        try:
            for child in block_to_traverse.children:
                self.traverse(child[0], child[1])
        except:
            print("Error: load block returned none")

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
        length_length_str = ""
        try:
            length_length_str = self.my_socket.recv(2)
        except socket.timeout as e:
            print("Receive timeout occurred")

        if length_length_str == "":
            return None
        length_length_str = length_length_str.decode()
        length_length = int(length_length_str)

        msg_length_str = ""
        try:
            msg_length_str = self.my_socket.recv(length_length).decode()
        except socket.timeout as e:
            print("Receive timeout occurred")

        if msg_length_str == "":
            return None
        msg_length = int(msg_length_str)

        message = ""
        try:
            message = self.my_socket.recv(int(msg_length))
        except socket.timeout as e:
            print("Receive timeout occurred")
        if message == "":
            return None
        while len(message) < int(msg_length):
            message += self.my_socket.recv(int(message) - len(message))
        return message


if __name__ == '__main__':
    main()
