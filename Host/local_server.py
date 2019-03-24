from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
import socket

class ftp_server:
    def __init__(self):
        self.authorizer = DummyAuthorizer()
        self.authorizer.add_anonymous(".", perm="elradfmw") #Make direcory the home direcory of the host machine (which can be navigated by ftp.cwd)
        handler = FTPHandler
        handler.authorizer = self.authorizer
        handler.banner = "You have connected sucessfully!"
        self.server = ThreadedFTPServer((socket.gethostname(), 1026), handler) #Make IP the IP of the host machine
    def run(self):
        self.server.serve_forever()
