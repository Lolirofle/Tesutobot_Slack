#!/usr/bin/env python3

from slacker import Slacker

import slack_client

if __name__ == '__main__':
	with open('SLACK_TOKEN','r') as slack_token_file:
		slack_token = slack_token_file.read().replace('\n','')
	slack = Slacker(slack_token)
	server = slack_client.Server(slack)
	server.rtm_connect()
	server.handle_loop()

	# Send messages from stdin
	#for line in sys.stdin:
	#	slack.chat.post_message('#bot',line,as_user=True)
