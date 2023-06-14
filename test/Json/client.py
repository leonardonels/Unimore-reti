#!/usr/bin/env python3

import socket
import sys
import time
import json

# Standard loopback interface address (localhost)
HOST = '127.0.0.1'
# Port to listen on (non-privileged ports are > 1023)
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

	# CONNECTION: contact server in listen
	s.connect((HOST, PORT))

	# asking user for filename
	filename = input('Enter filename you want download: ')
	
	# request to server
	request = {"filename": filename}
	request_json = json.dumps(request)
	s.sendall(request_json.encode('ascii'))

	# msg from server
	msg = s.recv(1024).decode('ascii')
	print(msg)

	# control msg
	if msg.split(' ')[0] == 'OK:':
		# reply from server
		time.sleep(1)
		reply_json = s.recv(1024).decode('ascii')
		# print for debug
		print(reply_json)

		# content from server
		content = s.recv(1024).decode('ascii')

		# create new file filename and write content in it
		f = open(filename, "w")
		f.write(content)
		f.close()

	# close socket
	s.close()

