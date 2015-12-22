import json
import random
import requests
import resurrected_name_gen
import threading
import urllib
import websocket

from user_util import *
import wikipedia

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
		rtm = self.slack.rtm.start()
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
				#print(message)

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
		(command,arg) = string_split_when(lambda c: c.isspace() or c=='.' or c==',' or c=='!' or c=='?',text)
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
		def wikipedia_summary(arg):
			def thread():
				try:
					(page,text) = wikipedia.summary(arg,3,auto_suggest=True,redirect=True)
					self.message_reply(message,"<"+page.url+"|*"+page.title+"* - Wikipedia>\n>>>"+text+"..")
				except wikipedia.DisambiguationError as e:
					self.message_reply(message,random.choice(["Tvetydigt","Var tydligare!","Vilket menar du?"])+"\n>>>"+str(e))
				except wikipedia.PageError:
					self.message_reply(message,random.choice(["En sådan artikel existerar inte!","Det där.. kunde inte hittas","Säker på att det där ens existerar?"]))
				except:
					self.message_reply(message,"Kunde inte nu.. Men prova senare kanske!")
			threading.Thread(target=thread).start()
			return True
		def google_ifeellucky(arg):
			def thread():
				try:
					self.message_reply(message,requests.head("https://www.google.com/search?btnI=I&q="+urllib.parse.quote(arg),allow_redirects=True).url)
				except:
					self.message_reply(message,"Kunde inte nu.. Men prova senare kanske!")
			threading.Thread(target=thread).start()
			return True
		def generate_name(arg):
			args = arg.split(" ")
			argn = len(args)

			try:
				length  = max(min(int(args[0]),10),3) if argn>0 else 6
				exclude = set(args[1]) if argn>1 else set()
			except:
				length  = 6
				exclude = set()

			self.message_reply(message,resurrected_name_gen.generate_name(length,exclude).title())
			return True

		# List of commands
		commands = {
			'help'      : help,
			'choice'    : choice,
			'choose'    : choice,
			'välj'      : choice,
			'eller'     : lambda arg: choice("Ja,Nej"),
			'bool'      : lambda arg: choice("Ja,Nej"),
			'fel'       : lambda arg: False,
			'false'     : lambda arg: False,
			'vad'       : lambda arg: echo(", ".join(commands.keys())),
			'kommandon' : lambda arg: echo(", ".join(commands.keys())),
			'säg'       : echo,
			'wiki'      : wikipedia_summary,
			'google'    : google_ifeellucky,
			'namn'      : generate_name,
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
