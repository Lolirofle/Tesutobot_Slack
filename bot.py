import datetime
import random
import requests
import threading
import traceback
import urllib

import hangman
import morse
import resurrected_name_gen
import util
import vasttrafik
import wikipedia

# Username: tesutobot
# Icon: lain.png
# Full name: てすと﻿ＴＥＳＵＴＯ , ぼと
# Purpose: ＴＩＬＬ  ＦÖＲ  ＡＴＴ  ＴＥＳＴＡ  ＳＡＫＥＲ～

class TesutoBot(object):
	''' Abstract class/mixin, implementing a number of methods '''

	def message_reply(self,message,text):
		'''
		A simple reply to a message from an user.
		Implemented by a client.
		'''
		raise NotImplementedError

	def on_init(self):
		# Vasttrafik initialization
		def read_file():
			with open('VASTTRAFIK_ID','r') as f:
				return f.read().replace('\n','')
		try:
			self.vasttrafik = vasttrafik.Vasttrafik(read_file)
		except Exception as e:
			self.vasttrafik = e
			traceback.print_tb(e.__traceback__)

		# Hangman initialization
		self.hangman = None

	def on_message(self,message,text):
		# Test whether the message is a command
		(command,arg) = util.string_split_when(lambda c: c.isspace() or c=='.' or c==',' or c=='!' or c=='?',text)
		if not self.on_command(message,command.lower(),arg):
			# Is this a question?
			if text.endswith("?"):# TODO: Check for "hur" and filter some answers
				# Answers to questions
				self.message_reply(message,random.choice(["Vet inte","Relativt","Hmm..","Beror på","...","Sluta","Var inte sådan nu"]))
			else:
				# Comments on stuff that can be said
				self.message_reply(message,"%s? %s" % (text,random.choice(["Okej","mm","ok","Jaså?","bra"])))

	def on_private_message(self,message):
		self.on_message(message,message['text'])

	def on_command(self,message,command,arg):
		# Command definitions
		def help(arg):
			self.message_reply(message,random.choice(["Kan inte hjälpa","Beklagar","Var inte så desperat"]))
			return True
		def choice(arg):
			self.message_reply(message,random.choice(arg.split(",")))# TODO: Determine which delimiter it is "eller", ",", " ", "|"
			return True
		def echo(arg):
			self.message_reply(message,arg)
			return True
		def wikipedia_summary(arg):
			def thread():
				try:
					(page,text) = wikipedia.summary(arg,3,auto_suggest=True,redirect=True)
					self.message_reply(message,"<%s|*%s* - Wikipedia>\n>>>%s.." % (page.url,page.title,text))
				except wikipedia.DisambiguationError as e:
					self.message_reply(message,"%s\n>>>%s" % (random.choice(["Tvetydigt","Var tydligare!","Vilket menar du?"]),str(e)))
				except wikipedia.PageError:
					self.message_reply(message,random.choice(["En sådan artikel existerar inte!","Det där.. kunde inte hittas","Säker på att det där ens existerar?"]))
				except:
					self.message_reply(message,"Kunde inte nu.. Men prova senare kanske!")
			threading.Thread(target=thread).start()
			return True
		def google_ifeellucky(arg):
			def thread():
				try:
					self.message_reply(message,requests.head("https://www.google.com/search?btnI=I&q=%s" % (urllib.parse.quote(arg),),allow_redirects=True).url)# TODO: Use the requests builtin parameter escape
				except:
					self.message_reply(message,"Kunde inte nu.. Men prova senare kanske!")
			threading.Thread(target=thread).start()
			return True
		def generate_name(arg):
			# Argument parsing
			args = arg.split(" ")
			argn = len(args)

			# Try to convert the arguments to valid input data to the name generator
			try:
				length  = max(min(int(args[0]),10),3) if argn>0 else 6
				exclude = set(args[1]) if argn>1 else set()
			except:
				return False

			self.message_reply(message,resurrected_name_gen.generate_name(length,exclude).title())
			return True
		def to_morse(arg):
			self.message_reply(message,"```%s```" % (util.string_char_translate(arg.upper(),morse.table),))
			return True
		def full_datetime(arg):
			self.message_reply(message,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S\n*%A* v %W*, dag *%j* på året"))
			return True
		def dice(arg):
			# Argument parsing
			if arg:
				args = arg.split(" ")
				argn = len(args)
			else:
				argn = 0

			# Try to convert the arguments to integers with bounds
			try:
				count = max(min(int(args[0]),10),1) if argn>0 else 1
				faces = max(min(int(args[1]),100000),1) if argn>1 else 6
			except:
				return False

			# Roll the dices
			dices = [random.randint(1,faces) for i in range(count)]

			# Print the dice states
			self.message_reply(message,"*%d* / %d : [%s]" % (sum(dices),count*faces,"] [".join(map(str,dices))))
			return True
		def vasttrafik_hallplats(arg):
			# Check whether initialization of vasttrafik succeeded
			if isinstance(self.vasttrafik,Exception):
				self.message_reply(message,"Kan inte nu, tyvärr. %s hände." % type(self.vasttrafik).__name__)
				return true

			# Check whether the input was valid (non-empty)
			arg = arg.strip()
			if not arg:
				self.message_reply(message,"Var då?")
				return True

			def map_departure(departure):
				''' Pretty printed (formatted) output for one departure from its data '''
				if 'rtDate' in departure and 'rtTime' in departure:
					time   = datetime.datetime.strptime("%s %s" % (departure['date']  ,departure['time']  ),'%Y-%m-%d %H:%M')
					rtTime = datetime.datetime.strptime("%s %s" % (departure['rtDate'],departure['rtTime']),'%Y-%m-%d %H:%M')
					timeDelta = (rtTime-time).total_seconds()/60
					timeString = ('%s ±%-3d' if timeDelta==0 else '%s %-+4d') % (departure['time'],timeDelta)
				else:
					timeString = "%s(?) " % departure['time']

				return "%s: [%s] %s (Läge %s)" % (
					timeString,
					departure['name'],
					departure['direction'],
					departure['rtTrack'] if 'rtTrack' in departure else departure['track']
				)

			def thread():
				# Try to fetch location and a departure table from the location
				try:
					location = self.vasttrafik.location(arg.lower().replace(' ','_'))
					self.message_reply(message,"Hållplats *%s*\n```%s```" % (location['name'],"\n".join(map(map_departure,self.vasttrafik.departures(location['id'],datetime.datetime.now())))))
				except Exception as e:
					self.message_reply(message,"Förväntade mig att få en tidtabell på hållplatsen, men fick istället en %s" % (type(e).__name__,))
			threading.Thread(target=thread).start()
			return True
		def hangman_game(arg):
			(subcommand,arg) = util.string_split_when(lambda c: c.isspace(),arg)
			if subcommand=='guess':
				if self.hangman==None:
					self.message_reply(message,"Kör inget. Vill spela, eller?")
				else:
					if arg:
						if arg[0].isalpha():
							try:
								has_won = self.hangman.guess_char(arg[0].lower())
								self.message_reply(message,"```%s```" % str(self.hangman))
								if has_won:
									self.hangman = None
							except hangman.GameOverError:
								self.message_reply(message,"Tyvärr, det var: %s" % self.hangman.word)
								self.hangman = None
						else:
							self.message_reply(message,"Kan bara gissa med bokstäver ur alfabetet!")
					else:
						self.message_reply(message,"Ingen gissning?")
			elif subcommand=='new':
				self.hangman = hangman.Hangman(arg.lower() if arg else "test")
				self.message_reply(message,"```%s```" % str(self.hangman))
			elif subcommand=='show' or subcommand=='state':
				self.message_reply(message,"```%s```" % str(self.hangman))
			elif subcommand=='reveal':
				if self.hangman==None:
					self.message_reply(message,"Kör inget. Vill spela, eller?")
				else:
					self.hangman.reveal()
					self.message_reply(message,"```%s```" % str(self.hangman))
					self.hangman = None
			else:# TODO: set art <bool>, lives <uint>
				self.message_reply(message,"*Möjliga kommandon för hänga gubbe:*\nguess, new, reveal, show|state, help|?")
				# https://sv.wiktionary.org/wiki/Special:RandomInCategory/Svenska/(Alla_uppslag|Adverb|Adjektiv|Verb|Substantiv)
			return True
		def shutdown(arg):
			raise ShutdownReason("Shutdown command: %s %s" % (command,arg))# TODO: issued by whom? at what time and date?

		# List of commands
		commands = {
			'help'         : help,
			'choice'       : choice,
			'choose'       : choice,
			'välj'         : choice,
			'eller'        : lambda arg: choice("Ja,Nej"),
			'bool'         : lambda arg: choice("Ja,Nej"),
			'fel'          : lambda arg: False,
			'false'        : lambda arg: False,
			'vad'          : lambda arg: echo(", ".join(commands.keys())),
			'kommandon'    : lambda arg: echo(", ".join(commands.keys())),
			'säg'          : echo,
			'wiki'         : wikipedia_summary,
			'google'       : google_ifeellucky,
			'namn'         : generate_name,
			'morse'        : to_morse,
			'yt'           : lambda arg: echo("<https://www.youtube.com/results?search_query=%s|Search: *%s* - YouTube>" % (urllib.parse.quote(arg),arg)),
			'date'         : full_datetime,
			'time'         : full_datetime,
			'datum'        : full_datetime,
			'tid'          : full_datetime,
			'dice'         : dice,
			'roll'         : dice,
			'tärning'      : dice,
			'baklänges'    : lambda arg: echo(arg[::-1]),
			'ord-baklänges': lambda arg: echo(" ".join(arg.split(" ")[::-1])),
			'hangman'      : hangman_game,
			'hållplats'    : vasttrafik_hallplats,
			'bussar'       : vasttrafik_hallplats,
			'spårvagnar'   : vasttrafik_hallplats,
			'god'          : lambda arg: echo("God %s!" % arg),
			'shutdown'     : shutdown,
			'terminate'    : shutdown,
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

class ShutdownReason(Exception):
	pass
