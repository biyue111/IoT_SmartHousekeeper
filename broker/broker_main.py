#!/usr/bin/python
# -*- coding: utf-8 -*-	 
import socket
import time
import threading
import thread
import sys
#from broker_server import *
import config_noIoT as config_noIoT
import server_config as server_config
import keys as keys

import requests	 
import urllib  
import json	 
import hashlib	
import base64
import os
from keyWordExtractUpdate import findWord
from web_requests import web_requests

import ast

data = config_noIoT.data_format
sensor_value = config_noIoT.sensor_value
user_input = config_noIoT.user_input
activators_state = config_noIoT.activators_state
activators_lock_timer = config_noIoT.activators_lock_timer

def lock_countdown():
	while 1:
		global activators_lock_timer
		for i in range(len(activators_lock_timer["Values"][0])):
			if activators_lock_timer["Values"][0][i] > 0:
				activators_lock_timer["Values"][0][i] -= 1
			#print (activators_lock_timer["ColumnNames"][i] + ":" + str(activators_lock_timer["Values"][0][i]))
		time.sleep(1)

def lock_set(k, l_time):
	global activators_lock_timer
	ind = activators_lock_timer["ColumnNames"].index(k)
	activators_lock_timer["Values"][0][ind] = l_time



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
			
def update_activators_before_send():
		# Update the activators_state with the user_input before sending to client raspberrys
	global sensor_value
	global activators_state

	input_ind = user_input["ColumnNames"].index("sleepStatus")
	output_ind = activators_state["ColumnNames"].index("ledStatus")
	if user_input["Values"][0][input_ind] == "1": # if the user is sleeping
		activators_state["Values"][0][output_ind] = "1" # trun off the LED
		lock_set("ledStatus", config_noIoT.lock_time)
		
	input_ind = user_input["ColumnNames"].index("joyStatus")
	output_ind = activators_state["ColumnNames"].index("curtainStatus")
	if user_input["Values"][0][input_ind] == "1": # left
		next_state = float(activators_state["Values"][0][output_ind]) - 0.1 # drag the curtain to left
		if next_state > 0:
			activators_state["Values"][0][output_ind] = str(next_state)
		else :
			activators_state["Values"][0][output_ind] = "0"
		lock_set("curtainStatus", config_noIoT.lock_time)

	elif user_input["Values"][0][input_ind] == "2": #right close the curtain
		next_state = float(activators_state["Values"][0][output_ind]) + 0.1 # trun off the LED
		if next_state <=1 :
			activators_state["Values"][0][output_ind] = str(next_state)
		else :
			activators_state["Values"][0][output_ind] = "1"
		lock_set("curtainStatus", config_noIoT.lock_time)
		
def update_activators_after_send():
	#Only give one coffee
	global sensor_value
	global activators_state

	ind = activators_state["ColumnNames"].index("coffeeStatus")
	if activators_state["Values"][0][ind] == "1":
		activators_state["Values"][0][ind] = "0"
				

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
	raw_data = sock.recv(1024) 
	time.sleep(1) 
	if not raw_data or raw_data.decode() == '-quit-': 
		return
	print raw_data
	format_data(raw_data)
	update_activators_before_send()
	response = format_response()
	update_activators_after_send()
	# print response
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
	m2.update(keys.AUDIO_API_KEY + curTime + paramBase64)  
	checkSum = m2.hexdigest()  
	header ={  
	'X-CurTime':curTime,  
	'X-Param':paramBase64,	
	'X-Appid':keys.AUDIO_APPID,	 
	'X-CheckSum':checkSum,	
	'Content-Type':'application/x-www-form-urlencoded; charset=utf-8',	
	}  
	return header 

def audio_action(x):
	global activators_state
	if x == 0: # Yes (give me a coffee)
		ind = activators_state["ColumnNames"].index("coffeeStatus")
		if activators_state["Values"][0][ind] == "-1":
			activators_state["Values"][0][ind] = "1"						
			lock_set("coffeeStatus", config_noIoT.lock_time)
				
	if x == 1: # No (I don't want coffee)
		ind = activators_state["ColumnNames"].index("coffeeStatus")
		if activators_state["Values"][0][ind] == "-1":
			activators_state["Values"][0][ind] = "1"						
			lock_set("coffeeStatus", config_noIoT.lock_time)
		
	if x == 2: #turn on the light
		ind = activators_state["ColumnNames"].index("ledStatus")   
		activators_state["Values"][0][ind] = "0"
		lock_set("ledStatus", config_noIoT.lock_time)
		
	if x == 3: #turn off the light.
		ind = activators_state["ColumnNames"].index("ledStatus")   
		activators_state["Values"][0][ind] = "1"
		lock_set("ledStatus", config_noIoT.lock_time)
		
	#if x == 4:
	#if x == 5:
	if x == 6: #Open the curtain
		ind = activators_state["ColumnNames"].index("curtainStatus")
		activators_state["Values"][0][ind] = "0"
		lock_set("curtainStatus", config_noIoT.lock_time)
	if x == 7: #Close the curtain
		ind = activators_state["ColumnNames"].index("curtainStatus")
		activators_state["Values"][0][ind] = "1"
		lock_set("curtainStatus", config_noIoT.lock_time)
	if x == 8:
		ind = activators_state["ColumnNames"].index("coffeeStatus")
		activators_state["Values"][0][ind] = "1" # give user a cup of coffe
		lock_set("coffeeStatus", config_noIoT.lock_time)

def audio_main():  
	while (1):
		r_input = raw_input("Recording time")
		if r_input == '':
				print("Please write the recording time")
				continue
		os.system("sudo arecord -D \"plughw:1,0\" -d "+str(r_input)+" -r 16000 -f \"Signed 16 bit Little Endian\" iotTest.wav")
		f = open("iotTest.wav", 'rb')  
		file_content = f.read()	 
		base64_audio = base64.b64encode(file_content)  
		body = urllib.urlencode({'audio': base64_audio})  
	  
		r = requests.post(keys.AUDIO_URL,headers=getHeader(),data=body)	 
		result = json.loads(r.content)	
	  
		if result["code"] == "0":  
			print "success, data = " + result["data"]  
			text = result["data"]
		else:  
			print r.text
			return	
		
		audio_action(findWord(text))
	return
	
# Web request part
def web_response_action(target_activator, res):
	res_dict = ast.literal_eval(res)
	value = res_dict["Results"]["output1"]["value"]["Values"][0][0]
	print (target_activator + "web value:" + value)
	ind = activators_lock_timer["ColumnNames"].index(target_activator)
	if activators_lock_timer["Values"][0][ind] == 0:
		if target_activator == "coffeeStatus":
			if value == "True":
				activators_state["Values"][0][ind] = "-1"
		else:
			activators_state["Values"][0][ind] = value
	
def format_web_request_data():
	global sensor_value
	f_data = config_noIoT.data_format
	for i in range(len(sensor_value["ColumnNames"])):
		cn = sensor_value["ColumnNames"][i]
		data_ind = f_data["Inputs"]["input1"]["ColumnNames"].index(cn)
		f_data["Inputs"]["input1"]["Values"][0][data_ind] = sensor_value["Values"][0][i]
	return f_data

	
def web_request_thread():
	request = web_requests()
	#server = broker_server()
	while 1:
		f_data = format_web_request_data()
		print("f_data")
		res = request.send_request(f_data, keys.LED_ML_URL, keys.LED_ML_API_KEY)
		web_response_action("ledStatus", res)
		res = request.send_request(f_data, keys.COFFEE_ML_URL, keys.COFFEE_ML_API_KEY)
		web_response_action("coffeeStatus", res)
		res = request.send_request(f_data, keys.CURTAIN_ML_URL, keys.CURTAIN_ML_API_KEY)
		web_response_action("curtainStatus", res)
		time.sleep(3)


try:
   thread.start_new_thread( server_thread, (server_config.HOST, server_config.PORT, ) )
   thread.start_new_thread( audio_main, ())
   thread.start_new_thread( web_request_thread, ())
   thread.start_new_thread( lock_countdown, ())
   #thread.start_new_thread( client_thread, (sys.argv[1], PORT, ) )
except:
   print "Error: unable to start thread"

while 1:
   pass

