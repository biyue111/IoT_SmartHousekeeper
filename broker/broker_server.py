import SocketServer
import socket
import sys

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print '{} :{}'.format(self.client_address[0], self.data)
        
class broker_server():
  def __init__(self):
    pass
  
  # Define the server function
  def server_thread(HOST, PORT):
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    print "The server start at port %s" % ( PORT )
    server.serve_forever()
