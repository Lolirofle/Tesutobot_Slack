import json
import websocket

import bot
import util

class Server(bot.TesutoBot):
	def __init__(self,slack):
		self.slack = slack
		self.data = None
		self.websocket = None
		self.users = {}
		self.channels = {}
		self.connected = False
		self.on_init()

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
		self_id = "<@%s>" % (self.data['self']['id'],)
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
						self.on_message(message,util.string_drop_while(lambda c: not c.isalnum(),message['text'][self_id_len:]))
					# Mentioned name of the bot?
					elif message['text'].startswith(self_name):
						self.on_message(message,util.string_drop_while(lambda c: not c.isalnum(),message['text'][self_name_len:]))
					# Private message from someone?
					elif message['channel'].startswith("D") and message['user']!=self.data['self']['id']:
						self.on_private_message(message)
		except KeyboardInterrupt:
			pass

		# Finalize
		self.websocket.close()
		self.connected = False

	def message_reply(self,message,text):
		self.slack.chat.post_message(
			message['channel'],
			text if message['channel'].startswith("D") else ("<@%s>: %s" % (message['user'],text)),
			as_user=True
		)

class SlackNotConnectedError(Exception):
	pass
class SlackRtmConnectionError(Exception):
	def __init__(self,error):
		self.error = error
	def __str__(self):
		return repr(self.error)
