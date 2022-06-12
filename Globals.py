import socket


class Globals:
    def __init__(self):
        self.port = 1726
        self.userserver_port = 1728
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        self.master_ip = local_ip
        self.pre_len = 2
        self.path_win = 'C:/CloudBlocks'
        self.path_used = self.path_win
