import select
import socket
from Block import Block
from Globals import Globals
from Database import Database
from BlockFolder import BlockFolder
import pickle
import os


def main():
    server = Server(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    addresses_to_send = ["address1", "address2", "address3"]
    server.addresses_to_send = addresses_to_send
    server.connect()
    server.main_loop()


class Server:
    def __init__(self, ser_socket, port=0, pre_len=0):
        mem = Globals()
        self.port = mem.port
        self.ser_socket = ser_socket
        self.pre_len = mem.pre_len
        self.cli_socket = None
        self.messages_to_send = []
        self.open_client_sockets = []
        self.addresses_to_send = []
        self.dir_path = mem.path_used
        self.db = Database()

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
                    if data == "" or data is None or "exit" in data or "quit" in data:
                        self.open_client_sockets.remove(current_socket)
                        print("Connection with client closed")
                        self.protocol_message("Connection closed", True, current_socket)
                    else:
                        print("Received data")
                        print(data)
                        if data.__contains__("createuser"):
                            data = data.split("$")
                            self.user_to_db(data, current_socket)
                        elif data.__contains__("login"):
                            data = data.split("$")
                            self.verify_log_in(data, current_socket)
                        elif data.__contains__("update"):
                            data = data.split("$")
                            self.update_gen(current_socket)
                        else:
                            if data == "open address needed":
                                self.send_next_address(current_socket)

    def update_gen(self, current_socket):
        self.protocol_message("send block", True, current_socket)
        gen = pickle.loads(self.recv_message(current_socket))
        print(gen)
        username = gen.block_name.split("_")
        self.db.update_db_gen(gen, username[-1])


    def verify_log_in(self, data, client_socket):
        name = data[1]
        password = data[2]
        if not self.db.verify_new_name(name):
            self.protocol_message("Send Block", True, client_socket)
            block = pickle.loads(self.recv_message(client_socket))
            if self.db.verify_block(name, block):
                self.protocol_message("Correct", True, client_socket)
                return True
            else:
                self.protocol_message("Incorrect", True, client_socket)
                return False

    def send_next_address(self, curr_socket):  # Moves first address to last and sends to user.
        to_send = self.addresses_to_send.pop(0)
        self.addresses_to_send.append(to_send)
        self.protocol_message(to_send, True, curr_socket)

    def user_to_db(self, data, curr_socket):
        name = data[1]
        password = data[2]
        if self.db.verify_new_name(name):  # Create block for user, send to user save to db.
            block = BlockFolder(name)
            self.db.insert_user_data(name, password, block)
            print("Inserted to db")
            self.protocol_message(pickle.dumps(block), False, curr_socket)
        else:
            self.protocol_message("Name is already in use, please try another", True, curr_socket)

    def connect(self):
        self.ser_socket.bind(('0.0.0.0', self.port))
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
