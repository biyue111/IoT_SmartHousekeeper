#from web_requests import web_request
import socket
import time
import threading
import thread
import sys
#from broker_server import *
import config_noIoT as config_noIoT
import server_config as server_config

data = config_noIoT.data_format
sensor_value = config_noIoT.sensor_value
user_input = config_noIoT.user_input
activators_state = config_noIoT.activators_state
activators_lock_timer = config_noIoT.activators_lock_timer

def format_data(raw_data):
	global data
	length = len(raw_data.split(';'))-1
		
	for i in range(0, length):
		try:
			ind = sensor_value["ColumnNames"].index(raw_data.split(';')[i].split(':')[0])
			#if ind
			sensor_value["Values"][0][ind] = raw_data.split(';')[i].split(':')[1]
		try:
			ind = user_input["ColumnNames"].index(raw_data.split(';')[i].split(':')[0])
			#if ind
			user_input["Values"][0][ind] = raw_data.split(';')[i].split(':')[1]
			
def update_activators():
	input_ind = sensor_value["ColumnNames"].index("sleepStatus")
	output_ind = activators_state["ColumnNames"].index("ledStatus")
	if sensor_value["Values"][0][input_ind] = "1" # if the user is sleeping
		activators_state["Values"][0][output_ind] = "0" # trun off the LED
		
def format_response():
	


# The broker server
def TCP(sock, addr): 
	raw_data = sock.recv(1024) 
	time.sleep(1) 
	if not raw_data or raw_data.decode() == '-quit-': 
		break
	print raw_data
	format_data(raw_data)
	update_activators()
	response = format_response()
        sock.send(data.decode('utf-8').upper().encode())
	
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
		
# Send request to ML Studio	
def send_request(self, data, url, api_key):
	body = str.encode(json.dumps(data))
	headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
	req = urllib2.Request(url, body, headers) 
	try:
	    response = urllib2.urlopen(req)
	    # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
	    # req = urllib.request.Request(url, body, headers) 
	    # response = urllib.request.urlopen(req)
	    result = response.read()
	    print(result) 
	except urllib2.HTTPError, error:
	    print("The request failed with status code: " + str(error.code))
	    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
	    print(error.info())
	    print(json.loads(error.read()))

#request = web_request()
#server = broker_server()

#request.send_request(data, config_noIoT.web_url, config_noIoT.api_key)
try:
   thread.start_new_thread( server_thread, (server_config.HOST, server_config.PORT, ) )
   #thread.start_new_thread( client_thread, (sys.argv[1], PORT, ) )
except:
   print "Error: unable to start thread"

while 1:
   pass
