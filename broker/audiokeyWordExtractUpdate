#!/usr/bin/python
# -*- coding: utf-8 -*-
def findWord(sentence):
# 帮我开一下灯
# 帮我把灯开一下
# 0 是 yes
# 1 否 no
# 2 开灯 Please turn on the light.
# 3 关灯 Please turn off the light.
# 4 开空调 Please open the air condition.
# 5 关空调 Please close the air condition.
# 6 拉开窗帘 Please pull the curtain.
# 7 关上窗帘 Please draw the curtain.
# 8 咖啡服务 I want to drink a cup of coffee.

	engSent = ['Yes',
				'No',
				'Please turn on the light',
				'Please turn off the light',
				'Please open the air condition',
				'Please close the air condition',
				'Please pull the curtain',
				'Please draw the curtain',
				'I want to drink a cup of coffee'] 

	posWords = [u'打开',u'拉开',u'开']
	posNum = len(posWords)
	negWords = [u'关闭',u'关上',u'拉上',u'关']
	negNum = len(negWords)
	
	# get the associated machine
	machineName = -1

	#print sentence
	#print u"灯"

	if (sentence.find(u'灯')>=0):
		machineName = 1  # 2 3
	elif (sentence.find(u'空调')>=0):
		machineName = 2  # 4 5
	elif (sentence.find(u'窗帘')>=0):
		machineName = 3  # 6 7

	#print machineName
	# get the associated activation
	state = -1
	for word in posWords:
		if sentence.find(word)>=0:
			state = 0
	for word in negWords:
		if sentence.find(word)>=0:
			state = 1
	#print state
	if (machineName>=0 and state>=0):
		#print "hhhhh"
		#print machineName
		if state: # close
			print engSent[2*machineName+1]
			return 2*machineName+1
		else: # open
			print engSent[2*machineName]
			return 2*machineName
		

	#coffee service
	if (sentence.find(u'咖啡')>=0):
		print engSent[8]
		return 8

	# should detect rejectWords first cause rejectWords always contain agreeWords
	# or we could use 不 to detect [算了算了]
	rejectWords = [u'不行',u'不好',u'不可以',u'不同意', u'不要', u'不']
	agreeWords = [u'好的',u'可以',u'行',u'同意',u'好',u'要']

	for word in rejectWords:
		if (sentence.find(word)>=0):
			print engSent[1]
			return 1
	for word in agreeWords:
		if sentence.find(word)>=0:
			print engSent[0]
			return 0

	return -1

		
