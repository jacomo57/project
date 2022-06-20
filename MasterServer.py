import os
import select
import socket
from Globals import Globals
from Database import Database
from BlockFolder import BlockFolder
import pickle


def main():
    server = Server(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    server.bind()
    server.main_loop()


class Server:
    def __init__(self, ser_socket):
        self.mem = Globals()
        self.port = self.mem.port
        self.ser_socket = ser_socket
        self.pre_len = self.mem.pre_len
        self.cli_socket = None
        self.messages_to_send = []
        self.open_client_sockets = []
        self.ports_online = []
        self.dir_path = self.mem.path_used
        self.db = Database()

    def main_loop(self):
        self.make_dir_path()
        while True:
            print(self.ports_online)
            rlist, wlist, xlist = select.select([self.ser_socket] + self.open_client_sockets, [], [])
            for current_socket in rlist:
                if current_socket is self.ser_socket:
                    (new_socket, address) = self.ser_socket.accept()
                    self.open_client_sockets.append(new_socket)
                    print("Client accepted")
                else:
                    data = self.recv_message(current_socket).decode()
                    print(type(data))
                    if data == "exit":
                        self.open_client_sockets.remove(current_socket)
                        print("Connection with client closed")
                        self.protocol_message("Connection closed", True, current_socket)
                    else:
                        print("Received data")
                        print("data: ", data)
                        if data.__contains__("createuser"):
                            data = data.split("$")
                            self.user_to_db(data, current_socket)
                        elif data.__contains__("."):
                            self.get_port(data)
                            self.protocol_message("Yes", True, current_socket)
                        elif data.__contains__("login"):
                            data = data.split("$")
                            self.verify_log_in(data, current_socket)
                        elif data.__contains__("update"):
                            data = data.split("$")
                            self.update_gen(data, current_socket)
                        elif data.__contains__("load block"):
                            data = data.split()
                            self.load_block(data[-1], current_socket)
                        elif data.__contains__("save folder"):
                            data = data.split()
                            self.save_folder(data, current_socket)
                        elif data.__contains__("save file"):
                            data = data.split()
                            self.save_file(data, current_socket)
                        elif data == "upto":
                            self.update_dad_block(current_socket)
                        elif data.__contains__("get file"):
                            data = data.split()
                            self.get_file(data, current_socket)
                        elif data == "open address needed":
                            self.send_next_address(current_socket)

    def get_file(self, data, curr_socket):
        file_name = data[-1]
        self.load_block(file_name, curr_socket)

    def update_dad_block(self, curr_socket):  # Removes the block and resaves updated version.
        self.protocol_message("send block", True,curr_socket)
        block = pickle.loads(self.recv_message(curr_socket))
        os.remove(os.path.join(self.dir_path, block.block_name))
        self.dump_block(block)
        self.protocol_message("yes", True, curr_socket)

    def save_folder(self, data, curr_socket):
        block_name = data[2]
        prime = int(data[3])
        father_name = data[4]
        address = data[5]
        dad_block = self.load_block_server(father_name)
        new_block = dad_block.make_sub_block(block_name, prime, father_name, address)
        print(new_block)
        self.dump_block(new_block)
        self.protocol_message(pickle.dumps(new_block), False, curr_socket)

    def save_file(self, data, curr_socket):
        block_name = data[2]
        prime = int(data[3])
        father_name = data[4]
        address = data[5]
        self.protocol_message("send file", True, curr_socket)
        pickled_file = pickle.loads(self.recv_message(curr_socket))
        dad_block = self.load_block_server(father_name)
        new_block = dad_block.make_sub_file(block_name, prime, pickled_file, dad_block.block_name, address)
        self.dump_block(new_block)
        self.protocol_message(pickle.dumps(new_block), False, curr_socket)

    def load_block_server(self, block_name):
        try:
            file = open(os.path.join(self.dir_path, block_name), 'rb')
            block = pickle.load(file)
            print(block.block_name, "loaded")
            file.close()
            return block
        except:
            return False

    def dump_block(self, block):
        file = open(os.path.join(self.dir_path, block.block_name), 'ab')
        pickle.dump(block, file)
        print(block.block_name, "dumped at ", os.path.join(self.dir_path, block.block_name))
        file.close()

    def make_dir_path(self):
        try:
            os.mkdir(self.dir_path)
        except OSError as error:
            print(error)
        print(f'Directory is in {self.dir_path}')

    def load_block(self, block_name, curr_socket):
        try:
            file = open(os.path.join(self.dir_path, block_name), 'rb')
            block = pickle.load(file)
            print(block.block_name, "loaded")
            file.close()
            self.protocol_message(pickle.dumps(block), False, curr_socket)
        except:
            self.protocol_message("File doesn't exist", True, curr_socket)

    def update_gen(self, data, current_socket):
        username = data[-1]
        self.protocol_message("send block", True, current_socket)
        gen = self.recv_message(current_socket)
        gen = pickle.loads(gen)
        self.db.update_db_gen(gen, username)

    def verify_log_in(self, data, client_socket):
        name = data[1]
        if not self.db.verify_new_name(name):
            self.protocol_message("Send Block", True, client_socket)
            block = pickle.loads(self.recv_message(client_socket))
            if self.db.verify_block(name, block):
                self.protocol_message("Correct", True, client_socket)
                return True
            else:
                self.protocol_message("Incorrect", True, client_socket)
                return False
        else:
            self.protocol_message("Incorrect", True, client_socket)
            return False

    def send_next_address(self, curr_socket):  # Moves first address to last and sends to user.
        to_send = self.ports_online.pop(0)
        self.ports_online.append(to_send)
        self.protocol_message(pickle.dumps(to_send), False, curr_socket)

    def get_port(self, ip):
        to_save = [self.mem.userserver_port, ip]
        self.ports_online.append(to_save)

    def user_to_db(self, data, curr_socket):
        name = data[1]
        ip = data[-1]
        user_port = self.mem.userserver_port
        if self.db.verify_new_name(name):  # Create block for user, send to user save to db.
            block = BlockFolder(name)
            self.db.insert_user_data(name, block, ip, user_port)
            print("Inserted to db")
            self.dump_block(block)
            self.protocol_message(pickle.dumps(block), False, curr_socket)
        else:
            self.protocol_message("Name is already in use, please try another", True, curr_socket)

    def bind(self):
        self.ser_socket.bind(('0.0.0.0', self.port))
        print("Waiting for clients")
        self.ser_socket.listen(5)

    @staticmethod
    def protocol_message(message, is_text, curr_socket):
        length_msg = len(message)
        length_msg_str = str(length_msg)

        length_length = len(length_msg_str)
        length_length_str = str(length_length).zfill(2)

        curr_socket.send(length_length_str.encode())

        curr_socket.send(length_msg_str.encode())

        if is_text:
            curr_socket.send(message.encode())
            print("protocol_message: " + message)
        else:
            curr_socket.send(message)

    @staticmethod
    def recv_message(curr_socket):
        length_length_str = curr_socket.recv(2)
        if length_length_str == "":
            pass
        length_length_str = length_length_str.decode()
        length_length = int(length_length_str)

        msg_length_str = curr_socket.recv(length_length).decode()
        msg_length = int(msg_length_str)

        message = curr_socket.recv(msg_length)
        while len(message) < msg_length:
            message += curr_socket.recv(int(message) - len(message))
        return message


if __name__ == '__main__':
    main()
