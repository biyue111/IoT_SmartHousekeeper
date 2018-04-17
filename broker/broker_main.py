from web_requests import web_request
import socket
import time
import threading
import thread
import sys
#from broker_server import *
import config_noIoT as config_noIoT
import server_config as server_config

data = config_noIoT.data_format

# The broker server
def TCP(sock, addr): 
	while True:
		raw_data = sock.recv(1024) 
		time.sleep(1) 
		if not raw_data or raw_data.decode() == '-quit-': 
			break
		print raw_data
		format_data(raw_data)
        #sock.send(data.decode('utf-8').upper().encode()) 
	
	sock.close() 
	#print('Connection from %s:%s closed.' %addr) 

def server_thread(HOST, PORT):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, PORT))
	s.listen(1) 
	print('Server is running...')
	sock, addr = s.accept()
	print('Accept new connection from %s.' %addr[0])
	while True:
		sock, addr = s.accept()
		TCP(sock, addr)

def format_data(raw_data):
	global data
	length = len(data.split(';'))-1
		
	for i in range(0, length):
		ind = data["Inputs"]["input2"]["ColumnNames"].index(data.split(';')[i].split(':')[0])
		#if ind
		data["Inputs"]["input2"]["Values"][0][ind] = v = data.split(';')[i].split(':')[1]

request = web_request()
#server = broker_server()

#request.send_request(data, config_noIoT.web_url, config_noIoT.api_key)
try:
   thread.start_new_thread( server_thread, (server_config.HOST, server_config.PORT, ) )
   #thread.start_new_thread( client_thread, (sys.argv[1], PORT, ) )
except:
   print "Error: unable to start thread"

while 1:
   pass
