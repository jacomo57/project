import os
import select
import socket
from Globals import Globals
from BlockFolder import BlockFolder
import pickle


def main():
    server = UserServer(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    addresses_to_send = ["address1", "address2", "address3"]
    server.addresses_to_send = addresses_to_send
    server.bind()
    server.main_loop()


class UserServer:
    def __init__(self, ser_socket, port, pre_len=0):
        mem = Globals()
        self.port = port
        self.ser_socket = ser_socket
        self.pre_len = mem.pre_len
        self.cli_socket = None
        self.messages_to_send = []
        self.open_client_sockets = []
        self.dir_path = mem.path_used
        self.main_loop()

    def main_loop(self):
        while True:
            print("While start")
            rlist, wlist, xlist = select.select([self.ser_socket] + self.open_client_sockets, [], [])
            for current_socket in rlist:
                if current_socket is self.ser_socket:
                    (new_socket, address) = self.ser_socket.accept()
                    self.open_client_sockets.append(new_socket)
                else:
                    data = self.recv_message(current_socket).decode()
                    if data == "exit":
                        self.open_client_sockets.remove(current_socket)
                        print("Connection with client closed")
                        self.protocol_message("Connection closed", True, current_socket)
                    else:
                        print("Received data")
                        print("data: ", data)
                        if "send block" in data:  # Example: send block test1gg
                            data = data.split()
                            self.send_block(data[-1], current_socket)
                        elif "save block " in data:  # Example: save block test1. Next msg: *block*
                            data = data.split()
                            self.save_block(data, current_socket)

    def send_block(self, block_name, curr_socket):
        file = open(os.path.join(self.dir_path, block_name), 'rb')
        block = pickle.loads(file)
        print(block.block_name, "loaded")
        file.close()
        self.protocol_message(pickle.dump(block), False, curr_socket)
        return block

    def save_block(self, block_name, curr_socket):
        self.protocol_message("send block", True, curr_socket)
        block = self.recv_message()
        if self.is_pickle_stream(block):
            block = pickle.loads(block)
            self.dump_block(block)
            self.protocol_message(block.block_name, "dumped at ", os.path.join(self.dir_path, block.block_name))

    @staticmethod
    def is_pickle_stream(byte_obj):
        try:
            pickle.loads(byte_obj)
            return True
        except pickle.UnpicklingError:
            return False

    def dump_block(self, block, username=0):
        if username != 0:
            file = open(os.path.join(self.dir_path, block.block_name), 'ab')
        else:
            file = open(os.path.join(self.dir_path, block.block_name), 'ab')
        pickle.dump(block, file)
        print(block.block_name, "dumped at ", os.path.join(self.dir_path, block.block_name))
        file.close()

    def load_block(self, block_name, address=0):  # Address curr useless, when seperate pc's will be needed.
        if self.check_my_block(block_name):
            file = open(os.path.join(self.dir_path, block_name), 'rb')
            block = pickle.load(file)
            print(block.block_name, "loaded")
            file.close()
            return block
        else:
            print("Not your file to view")

    def bind(self):
        self.hostname = socket.gethostname()
        self.local_ip = socket.gethostbyname(self.hostname)
        self.ser_socket.bind(("0.0.0.0", self.port))
        print("Waiting for clients")
        self.ser_socket.listen(5)

    def send_waitint_messages(self):
        for message in self.messages_to_send:
            (curr_socket, data) = message
            self.protocol_message(data, True, curr_socket)
            self.messages_to_send.remove(message)

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
