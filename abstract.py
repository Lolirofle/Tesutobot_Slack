class Bot(object):
	''' Abstracts a bot '''

	def on_message(self,message,text):
		raise NotImplementedError

	def on_private_message(self,message):
		raise NotImplementedError

	def on_command(self,message,command,arg):
		raise NotImplementedError


class Client(object):
	''' Abstracts a client '''

	def message_reply(self,message,text):
		'''
		A simple reply to a message from an user.
		Implemented by a client.
		'''
		raise NotImplementedError


class Message(object):
	''' Abstracts a message '''

	def id(self):
		raise NotImplementedError

	def user_id(self):
		raise NotImplementedError

	def username(self):
		raise NotImplementedError

	def text(self):
		raise NotImplementedError

	def datetime(self):
		raise NotImplementedError

	def inner_data(self):
		raise NotImplementedError
