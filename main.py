#!/usr/bin/python3

from slacker import Slacker
import json
import random
import sys
import websocket

# Username: tesutobot
# Icon: lain.png
# Full name: てすと﻿ＴＥＳＵＴＯ , ぼと
# Purpose: ＴＩＬＬ  ＦÖＲ  ＡＴＴ  ＴＥＳＴＡ  ＳＡＫＥＲ～

class Server(object):
	def __init__(self,slack):
		self.slack = slack
		self.data = None
		self.websocket = None
		self.users = {}
		self.channels = {}
		self.connected = False

	def rtm_connect(self):
		""" Connects using the Real Time Messaging method """

		# Requests RTM, and error checks
		rtm = slack.rtm.start()
		if not rtm.successful:
			raise SlackRtmConnectionError(rtm.error)

		# Store response data
		self.data = rtm.body
#		print(json.dumps(self.data,indent=4,sort_keys=True))

		# Connect to the websocket server for receiving RTM data
		self.websocket = websocket.create_connection(self.data['url'])
#		self.websocket.sock.setblocking(0)
		self.connected = True

	def handle_loop(self):
		if not self.connected:
			raise SlackNotConnectedError

		# Cache
		self_id = "<@"+self.data['self']['id']+">"
		self_name = self.data['self']['name']
		self_id_len = len(self_id)
		self_name_len = len(self_name)

		try:
			# For each received message (Waiting when not receiving)
			while True:
				message = json.loads(self.websocket.recv())
				print(message)

				# Match message type
				if message['type']=="message" and 'text' in message and 'user' in message:
					# Notification to the bot from someone?
					if message['text'].startswith(self_id):
						self.on_message(message,string_drop_while(lambda c: not c.isalnum(),message['text'][self_id_len:]))
					# Mentioned name of the bot?
					elif message['text'].startswith(self_name):
						self.on_message(message,string_drop_while(lambda c: not c.isalnum(),message['text'][self_name_len:]))
					# Private message from someone?
					elif message['channel'].startswith("D") and message['user']!=self.data['self']['id']:
						self.on_private_message(message)
		except KeyboardInterrupt:
			pass

		# Finalize
		self.websocket.close()
		self.connected = False

	def on_message(self,message,text):
		# Test whether the message is a command
		(command,arg) = string_split_when(lambda c: c.isspace(),text)
		if not self.on_command(message,command.lower(),arg):
			# Is this a question?
			if text.endswith("?"):
				# Answers to questions
				self.message_reply(message,random.choice(["Vet inte","Relativt","Hmm..","Beror på","...","Sluta","Var inte sådan nu"]))
			else:
				# Comments on stuff that can be said
				self.message_reply(message,text+"? "+random.choice(["Okej","mm","ok","Jaså?","bra"]))

	def on_private_message(self,message):
		self.message_reply(message,"Okej")

	def on_command(self,message,command,arg):
		# Command definitions
		def help(arg):
			self.message_reply(message,random.choice(["Kan inte hjälpa","Beklagar","Var inte så desperat"]))
			return True
		def choice(arg):
			self.message_reply(message,random.choice(arg.split(",")))
			return True
		def echo(arg):
			self.message_reply(message,arg)
			return True
		# List of commands
		commands = {
			'help': help,
			'choice': choice,
			'choose': choice,
			'välj': choice,
			'eller': lambda arg: choice("Ja,Nej"),
			'fel': lambda arg: False,
			'vad': lambda arg: echo(", ".join(commands.keys())),
		}

		# If the command is defined
		if command in commands:
			# It is a command, and if the command did not succeed
			if not commands[command](arg):
				self.message_reply(message,random.choice(["Förstår inte","?","Vad menar du?","Vad tänker du med?"]))
			return True
		else:
			# Not a command
			return False

	def message_reply(self,message,text):
		''' A simple reply to a message from an user '''
		self.slack.chat.post_message(message['channel'],"<@"+message['user']+">: "+text,as_user=True)

class SlackNotConnectedError(Exception):
	pass
class SlackRtmConnectionError(Exception):
	def __init__(self,error):
		self.error = error
	def __str__(self):
		return repr(self.error)

def string_drop_while(predicate,string):
	''' A string without the beginning matched by the predicate '''
	for (i,c) in enumerate(string):
		if not predicate(c):
			return string[i:]
	return ""

def string_take_while(predicate,string):
	''' A string with the beginning matched by the predicate '''
	for (i,c) in enumerate(string):
		if not predicate(c):
			return string[:i]
	return string

def string_split_when(predicate,string):
	''' Two strings separated from the middle part matched by the predicate '''
	i1 = None
	for (i,c) in enumerate(string):
		if i1==None:
			if predicate(c):
				i1 = i
		else:
			if not predicate(c):
				return (string[:i1],string[i:])
	return (string,"")

if __name__ == '__main__':
	with open('SLACK_TOKEN','r') as slack_token_file:
		slack_token = slack_token_file.read().replace('\n','')
	slack = Slacker(slack_token)
	server = Server(slack)
	server.rtm_connect()
	server.handle_loop()
