from slacker import Slacker
import json
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
		rtm = slack.rtm.start()
		if not rtm.successful:
			raise SlackRtmConnectionError(rtm.error)

		self.data = rtm.body
#		print(json.dumps(self.data,indent=4,sort_keys=True))

		self.websocket = websocket.create_connection(self.data['url'])
#		self.websocket.sock.setblocking(0)
		self.connected = True

	def handle_loop(self):
		if not self.connected:
			raise SlackNotConnectedError

		try:
			while True:
				message = json.loads(self.websocket.recv())
				if message['type']=="message":
					if message['text'].startswith("<@"+self.data['self']['id']+">"):
						slack.chat.post_message(message['channel'],"<@"+message['user']+">: Okej",as_user=True)
					elif message['channel'].startswith("D") and message['user']!=self.data['self']['id']:
						slack.chat.post_message(message['channel'],"Okej",as_user=True)
				print(message)
		except KeyboardInterrupt:
			pass

		self.websocket.close()
		self.connected = False

class SlackNotConnectedError(Exception):
	pass
class SlackRtmConnectionError(Exception):
	def __init__(self,error):
		self.error = error
	def __str__(self):
		return repr(self.error)


with open('SLACK_TOKEN','r') as slack_token_file:
    slack_token = slack_token_file.read().replace('\n','')
slack = Slacker(slack_token)
server = Server(slack)
server.rtm_connect()
server.handle_loop()
#ws.send("Hello, World")

# Send messages
#for line in sys.stdin:
#	slack.chat.post_message('#bot',line,as_user=True)
