#!/usr/bin/python
# -*- coding: utf-8 -*-	 
import requests	 
import time	 
import urllib  
import json	 
import hashlib	
import base64
import os
import socket
from keyWordExtractUpdate import findWord
import server_config as server_config
import keys as keys
  
#URL = "http://api.xfyun.cn/v1/service/v1/iat"  
#APPID = "xxx"  
#API_KEY = "xxx"	 
  
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
  
def main():	 
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	addr = (server_config.AUDIO_SERVER_HOST, server_config.AUDIO_SERVER_PORT)
	while True:
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
			
		word = str(findWord(text))
		print ("word:"+word)
		s.sendto(word, addr)

	s.close()
	return	
  
if __name__ == '__main__':	
	main()	
