from Globals import Globals
import socket
import pickle
import os
from GUI import Toplevel1 as GUI
import tkinter as tk
from BlockFolder import BlockFolder


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
        self.master_address = (mem.master_ip, self.port)
        self.master_socket = 0
        self.pre_len = mem.pre_len
        self.dir_path = mem.path_used
        self.make_dir_path()
        self.gui = None
        self.curr_address = 0
        self.block_list = []
        self.u_server_socket = 0

    def start_gui(self):
        root = tk.Tk()
        root.protocol('WM_DELETE_WINDOW', root.destroy)  # Creates a toplevel widget.
        top1 = root
        self.gui = GUI(self, top1)

    def main_loop(self):
        self.connect(self.master_address)
        self.start_gui()
        self.master_socket.close()
        return

    def exit_program_temp(self):
        self.protocol_message_temp("exit", True)
        answer = self.recv_message_temp().decode()
        if answer == "Connection closed":
            self.u_server_socket.close()
            return True
        else:
            return False

    def exit_program(self):
        self.protocol_message("exit", True)
        answer = self.recv_message().decode()
        if answer == "Connection closed":
            return True
        else:
            return False

    def create_folder(self, dad_block, folder_name):  # Need to update gen in db and file if gen updated
        prime = self.get_next_prime()
        self.protocol_message("open address needed", True)
        address = pickle.loads(self.recv_message())
        self.temp_connect(address)
        block_for_update = dad_block.make_sub_block((folder_name + "-" + self.user_name), prime, dad_block.block_name, address)  # To update local dad
        self.protocol_message_temp(f'save folder {(folder_name + "-" + self.user_name)} {prime} {dad_block.block_name} {address}', True)
        new_block = self.recv_message_temp()
        if self.is_pickle_stream(new_block):
            new_block = pickle.loads(new_block)
        else:
            print(new_block)
        self.update_dad_block(dad_block)
        print("create_folder block ", new_block)
        if dad_block.block_name.__contains__("gen_"):
            self.protocol_message(f'update${self.user_name}', True)
            if dad_block.block_name.__contains__("gen_"):
                if self.recv_message().decode() == "send block":  # updates db if folder is gen's child
                    self.protocol_message(pickle.dumps(self.block), False)
        print("Folder created")
        self.exit_program_temp()
        self.block_list.append(new_block)
        return new_block

    def create_file(self, dad_block, file_name, pickled_file):
        prime = self.get_next_prime()
        self.protocol_message("open address needed", True)
        address = pickle.loads(self.recv_message())
        self.temp_connect(address)
        block_for_update = dad_block.make_sub_file((file_name + "-" + self.user_name), prime, pickled_file, dad_block.block_name, address)  # To update local dad
        self.protocol_message_temp(f'save file {(file_name + "-" + self.user_name)} {prime} {dad_block.block_name} {address}', True)
        response = self.recv_message_temp().decode()
        self.protocol_message_temp(pickle.dumps(pickled_file), False)
        new_block = self.recv_message_temp()
        if self.is_pickle_stream(new_block):
            new_block = pickle.loads(new_block)
        else:
            print(new_block)
        self.update_dad_block(dad_block)
        if dad_block.block_name.__contains__("gen_"):
            self.protocol_message(f'update${self.user_name}', True)
            if self.recv_message().decode() == "send block":  # updates db if folder is gen's child
                if dad_block.block_name.__contains__("gen_"):
                    self.protocol_message(pickle.dumps(self.block), False)
        print("File created")
        self.exit_program_temp()
        self.block_list.append(new_block)
        return new_block

    def update_dad_block(self, block):  # Removes the block and resaves updated version.
        if "gen_" in block.block_name:
            os.remove(os.path.join(self.dir_path, block.block_name))
            self.dump_block(block)
        self.protocol_message_temp("upto", True)
        resp = self.recv_message_temp()
        self.protocol_message_temp(pickle.dumps(block), False)
        print(self.recv_message_temp())

    def dump_block(self, block):
        file = open(os.path.join(self.dir_path, block.block_name), 'ab')
        pickle.dump(block, file)
        print(block.block_name, "dumped at ", os.path.join(self.dir_path, block.block_name))
        file.close()

    def get_file(self, file_name):
        address = self.get_address_by_name(file_name)
        self.temp_connect(address)
        self.protocol_message_temp("get file " + file_name, True)
        file = self.recv_message_temp()
        if self.is_pickle_stream(file):
            file = pickle.loads(file)
            self.dump_block(file)
            return file
        else:
            print(file)
            return False

    def load_block(self, block_name):
        if block_name.__contains__("gen"):
            gen = self.load_gen_block(block_name)
            self.block_list.append(gen)
            print(self.block_list)
            return gen
        if self.check_my_block(block_name):
            address = self.get_address_by_name(block_name)
            if address:
                self.temp_connect(address)
                self.protocol_message_temp("load block " + block_name, True)
                response = self.recv_message_temp()
                self.exit_program_temp()
                if self.is_pickle_stream(response):
                    block = pickle.loads(response)
                    self.block_list.append(block)
                    print(self.block_list)
                    return block
        print("Not your file to view")

    def temp_connect(self, address):
        print("In connect")
        self.u_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(address)
        self.u_server_socket.connect((address[1], address[0]))
        print("Connection established")

    def get_address_by_name(self, block_name):
        for block in self.block_list:
            if block.children:
                for child in block.children:
                    if child[0] == block_name:  # Compare names
                        return child[1]

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

    def connect(self, address):
        print("In connect")
        self.master_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(address)
        self.master_socket.connect((address[0], address[1]))
        print("Connection established")

    def log_in(self, username):
        if self.verify_log_in(username):
            self.user_name = username
            return True
        else:
            print("One or more credentials are incorrect, please try again.")
        return False

    def verify_log_in(self, username):
        self.protocol_message(f'login${username}', True)
        if self.recv_message().decode() == "Send Block":
            try:
                block_gen = self.load_gen_block("gen_" + username)
                self.protocol_message(pickle.dumps(block_gen), False)
                answer = self.recv_message().decode()
                print(answer)
                if answer == "Correct":
                    self.block = block_gen
                    return True
            except:
                print("No file found")
                return False
            if answer == "Incorrect": return False
        else:
            return False

    def load_gen_block(self, block_name):
        if self.check_my_block(block_name):
            file = open(os.path.join(self.dir_path, block_name), 'rb')
            block = pickle.load(file)
            print(block.block_name, "loaded")
            file.close()
            return block
        else:
            print("Not your file to view")

    def create_user(self, username):
        print(username)
        if self.send_user(username):
            self.user_name = username
            return True
        else:
            print("This username is already taken, please try another")
        return False

    def send_user(self, username):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        self.protocol_message(f'createuser${username}${ip_address}', True)
        gen = self.recv_message()
        if self.is_pickle_stream(gen):
            gen = pickle.loads(gen)
            self.block = gen
            self.dump_gen_block(gen)
            print(f'User {username} created successfully')
            return True
        else:
            return False

    def dump_gen_block(self, block):
        file = open(os.path.join(self.dir_path, block.block_name), 'ab')
        pickle.dump(block, file)
        print(block.block_name, "dumped at ", os.path.join(self.dir_path, block.block_name))
        file.close()

    @staticmethod
    def is_pickle_stream(byte_obj):
        try:
            pickle.loads(byte_obj)
            return True
        except pickle.UnpicklingError:
            return False

    # metadata = [child_name, address, self.hash]
    def traverse(self, child_name):
        print("child name ", child_name)
        block_to_traverse = self.load_block(child_name)
        self.block_list.append(block_to_traverse)
        if isinstance(block_to_traverse, BlockFolder):
            for child in block_to_traverse.children:
                try:
                    self.traverse(child[0])
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

        self.master_socket.send(length_length_str.encode())

        self.master_socket.send(length_msg_str.encode())

        if is_text:
            self.master_socket.send(message.encode())
        else:
            self.master_socket.send(message)

    def recv_message(self):
        length_length_str = ""
        try:
            length_length_str = self.master_socket.recv(2)
        except socket.timeout as e:
            print("Receive timeout occurred")

        if length_length_str == "":
            return None
        length_length_str = length_length_str.decode()
        length_length = int(length_length_str)

        msg_length_str = ""
        try:
            msg_length_str = self.master_socket.recv(length_length).decode()
        except socket.timeout as e:
            print("Receive timeout occurred")

        if msg_length_str == "":
            return None
        msg_length = int(msg_length_str)

        message = ""
        try:
            message = self.master_socket.recv(int(msg_length))
        except socket.timeout as e:
            print("Receive timeout occurred")
        if message == "":
            return None
        while len(message) < int(msg_length):
            message += self.master_socket.recv(int(message) - len(message))
        return message

    def protocol_message_temp(self, message, is_text):
        length_msg = len(message)
        length_msg_str = str(length_msg)

        length_length = len(length_msg_str)
        length_length_str = str(length_length).zfill(2)

        self.u_server_socket.send(length_length_str.encode())

        self.u_server_socket.send(length_msg_str.encode())

        if is_text:
            self.u_server_socket.send(message.encode())
        else:
            self.u_server_socket.send(message)

    def recv_message_temp(self):
        length_length_str = ""
        try:
            length_length_str = self.u_server_socket.recv(2)
        except socket.timeout as e:
            print("Receive timeout occurred")

        if length_length_str == "":
            return None
        length_length_str = length_length_str.decode()
        length_length = int(length_length_str)

        msg_length_str = ""
        try:
            msg_length_str = self.u_server_socket.recv(length_length).decode()
        except socket.timeout as e:
            print("Receive timeout occurred")

        if msg_length_str == "":
            return None
        msg_length = int(msg_length_str)

        message = ""
        try:
            message = self.u_server_socket.recv(int(msg_length))
        except socket.timeout as e:
            print("Receive timeout occurred")
        if message == "":
            return None
        while len(message) < int(msg_length):
            message += self.u_server_socket.recv(int(message) - len(message))
        return message


if __name__ == '__main__':
    main()