#!/usr/bin/env python3

import socket
import sys

# Standard loopback interface address (localhost)
HOST = '127.0.0.1'
# Port to listen on (non-privileged ports are > 1023)
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

	# CONNECTION: contact server in listen
	s.connect((HOST, PORT))

	# request to server
	request = input('Enter your request:\r\n')  
	s.sendall(request.encode('ascii'))

	# message from server
	msg = s.recv(1024).decode('ascii')
	print(msg)

	# reply from server
	reply = s.recv(1024).decode('ascii')
	print(reply)

	# close socket
	s.close()

