import random
import requests
import threading
import urllib

import morse
import resurrected_name_gen
import util
import wikipedia

# Username: tesutobot
# Icon: lain.png
# Full name: てすと﻿ＴＥＳＵＴＯ , ぼと
# Purpose: ＴＩＬＬ  ＦÖＲ  ＡＴＴ  ＴＥＳＴＡ  ＳＡＫＥＲ～

class TesutoBot(object):
	''' Abstract class/mixin, implementing a number of methods '''

	def message_reply(self,message,text):
		''' A simple reply to a message from an user '''
		raise NotImplementedError

	def on_message(self,message,text):
		# Test whether the message is a command
		(command,arg) = util.string_split_when(lambda c: c.isspace() or c=='.' or c==',' or c=='!' or c=='?',text)
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
				return False

			self.message_reply(message,resurrected_name_gen.generate_name(length,exclude).title())
			return True
		def to_morse(arg):
			self.message_reply(message,"```"+morse.convert(arg)+"```")
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
			'morse'     : to_morse,
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
