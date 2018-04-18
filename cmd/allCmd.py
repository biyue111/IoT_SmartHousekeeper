#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
#from curtain import *
def cmd_curtain_right(x, temp):
	while temp < x:
		temp = temp + 1
		hashes = '=' * int((temp)/100.0 * bar_length)
		spaces = ' ' * (bar_length - len(hashes))
		sys.stdout.write("\rPercent: [%s] %d%% "%(hashes + spaces, temp))
		sys.stdout.flush()
		time.sleep(0.01)
	return temp
	

def cmd_curtain_left(x, temp):
	while temp > x:
		temp = temp - 1
		hashes = '=' * int((temp)/100.0 * bar_length)
		spaces = ' ' * (bar_length - len(hashes))
		sys.stdout.write("\rPercent: [%s] %d%% "%(hashes + spaces, temp))
		sys.stdout.flush()	    
	    time.sleep(0.01)
	return temp


def cmd_curtain(x): # x is a number between 0~1
	# use edgar's curtain.py
	# copy output's part here
	hashes = '=' * int((temp)/100.0 * bar_length)
	spaces = ' ' * (bar_length - len(hashes))
	sys.stdout.write("\rPercent: [%s] %d%% "%(hashes + spaces, temp))
	sys.stdout.flush()
	time.sleep(0.01)

def cmd_airCondition(x):  # x=1 open/ 0 close
	if x==0:
		print "close air condition"
	else:
		print "open air condition"

def cmd_coffee(x): # x=1 / 2
	if x==1: hot coffee
		print "Do you want a cup of hot coffee?"
	else:
		print "Do you want a cup of cold coffee?"
