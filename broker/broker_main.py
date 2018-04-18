#from web_requests import web_request
import socket
import time
import threading
import thread
import sys
#from broker_server import *
import config_noIoT as config_noIoT
import server_config as server_config

# -*- coding: utf-8 -*-  
import requests  
import urllib  
import json  
import hashlib  
import base64
import os
from keyWordExtractUpdate import findWord  
URL = "http://api.xfyun.cn/v1/service/v1/iat"  
APPID = "xxx"  
API_KEY = "xxx" 

data = config_noIoT.data_format
sensor_value = config_noIoT.sensor_value
user_input = config_noIoT.user_input
activators_state = config_noIoT.activators_state
activators_lock_timer = config_noIoT.activators_lock_timer

def lock_countdown():
        global activators_lock_timer
        for i in range(len(activators_lock_timer["Values"])):
                if activators_lock_timer["Values"][i] > 0:
                        activators_lock_timer["Values"][i] -= 1;
        time.sleep(1000)


def format_data(raw_data):
	global data
	length = len(raw_data.split(';'))-1
		
	for i in range(0, length):
                k = raw_data.split(';')[i].split(':')[0]
                v = raw_data.split(';')[i].split(':')[1]
                if sensor_value["ColumnNames"].count(k):
			ind = sensor_value["ColumnNames"].index(k)
			sensor_value["Values"][0][ind] = v
                if user_input["ColumnNames"].count(k):
			ind = user_input["ColumnNames"].index(k)
			user_input["Values"][0][ind] = v
			
def update_activators():
	global sensor_value
	global activators_state

	input_ind = user_input["ColumnNames"].index("sleepStatus")
	output_ind = activators_state["ColumnNames"].index("ledStatus")
        if user_input["Values"][0][input_ind] == "1": # if the user is sleeping
		activators_state["Values"][0][output_ind] = "1" # trun off the LED
		
	input_ind = user_input["ColumnNames"].index("joyStatus")
	output_ind = activators_state["ColumnNames"].index("curtainStatus")
	if user_input["Values"][0][input_ind] == "1": # left
		next_state = float(activators_state["Values"][0][output_ind]) - 0.1 # drag the curtain to left
		if next_state > 0:
			activators_state["Values"][0][output_ind] = str(next_state)
		else :
			activators_state["Values"][0][output_ind] = "0"
	elif user_input["Values"][0][input_ind] == "2": #right
		next_state = float(activators_state["Values"][0][output_ind]) + 0.1 # trun off the LED
		if next_state <=1 :
			activators_state["Values"][0][output_ind] = str(next_state)
		else :
			activators_state["Values"][0][output_ind] = "1"
		
def format_response():
	global sensor_value
	global activators_state
	
	response = ""
	for i in range(len(activators_state["ColumnNames"])):
		response = response + activators_state["ColumnNames"][i] + ":" + activators_state["Values"][0][i] + ";"
	print ("response: " + response)
	return response


# The broker server
def TCP(sock, addr): 
        while True:
	        raw_data = sock.recv(1024) 
	        time.sleep(1) 
	        if not raw_data or raw_data.decode() == '-quit-': 
	        	break
	        print raw_data
	        format_data(raw_data)
	        update_activators()
	        response = format_response()
                print response
                sock.sendall(response)
	        
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
		TCP(sock, addr)
		sock, addr = s.accept()
		
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
		
# Audio input
def getHeader():  
    curTime = str(int(time.time()))  
    param = "{\"engine_type\": \"sms16k\", \"aue\": \"raw\"}"  
    paramBase64 = base64.b64encode(param)  
  
    m2 = hashlib.md5()  
    m2.update(API_KEY + curTime + paramBase64)  
    checkSum = m2.hexdigest()  
    header ={  
        'X-CurTime':curTime,  
        'X-Param':paramBase64,  
        'X-Appid':APPID,  
        'X-CheckSum':checkSum,  
        'Content-Type':'application/x-www-form-urlencoded; charset=utf-8',  
    }  
    return header 

def audio_action(x):
	global activators_state
	if x == 0:
	if x == 1:
		
	if x == 2: #turn on the light
		
	if x == 3: #turn off the light.
		
	if x == 4:
	if x == 5:
	if x == 6:
	if x == 7:
	if x == 8:

def audio_main():  
    while (1):
		os.system("sudo arecord -D \"plughw:1,0\" -r 16000 -f \"Signed 16 bit Little Endian\" iotTest.wav")
		f = open("iotTest.wav", 'rb')  
		file_content = f.read()  
		base64_audio = base64.b64encode(file_content)  
		body = urllib.urlencode({'audio': base64_audio})  
	  
		r = requests.post(URL,headers=getHeader(),data=body)  
		result = json.loads(r.content)  
	  
		if result["code"] == "0":  
			print "success, data = " + result["data"]  
			text = result["data"]
		else:  
			print r.text
			return  
		
		#print type(text)
		#text = u'咖啡'
		#print text
		#print type(text)
		audio_action(findWord(text))
		#print findWord(text)
		
		#print type(text.decode("utf-8"))
		#print findWord(text.decode("utf-8"))
    return  

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
