from web_requests import web_request
from broker_server import *
import config_noIoT as config_noIoT
omport server_config as server_config

# The broker server
def TCP(sock, addr): 
	while True:
		data = sock.recv(1024) 
		time.sleep(1) 
		if not data or data.decode() == '-quit-': 
			break
		print data
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

def format_data(data, d, v):
  ind = data["Inputs"]["input2"]["ColumnNames"].index(d)
  print (ind)
  data["Inputs"]["input2"]["Values"][0][ind] = v
  
  return data


request = web_request()
server = broker_server()
data = config_noIoT.data_format
data = format_data(data, "temperature", 20)
data = format_data(data, "humidity", 20)

#request.send_request(data, config_noIoT.web_url, config_noIoT.api_key)
try:
   thread.start_new_thread( server.server_thread, (server_config.HOST, server_config.PORT, ) )
   #thread.start_new_thread( client_thread, (sys.argv[1], PORT, ) )
except:
   print "Error: unable to start thread"

while 1:
   pass
