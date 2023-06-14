#!/usr/bin/env python3

import socket
import sys
import time
import os
import re

# Standard loopback interface address (localhost)
HOST = '127.0.0.1'
#HOST = sys.argv[1]
# Port to listen on (non-privileged ports are > 1023)
PORT = 8080
#PORT = int(sys.argv[2])

def get_hostname():
        return ('Welcom from '+str(socket.gethostname()))

def rot13(x):
        x=x.lower()
        alpha="abcdefghijklmnopqrstuvwxyz"
        return "".join(alpha[(alpha.find(c)+13)%26] for c in x)

def serve_request(conn):
	# receive request from client
	request = conn.recv(1024).decode('ascii')
	# print for debug	
	print(request)

	#control request
	m = re.match(r'^([A-Za-z]+)$', request)

#	reply = get_hostname()
#	conn.sendall(reply.encode('ascii'))
#	time.sleep(1)
#	conn.close()
	
	if not m:
		# wrong request
		conn.sendall('+ERR\r\n'.encode('ascii'))
	else:
		# right request
		# get parameters from request

		#x = m.group(1),	return a str
		
		# send response line
		msg = '+OK\r\n'
		conn.sendall(msg.encode('ascii'))
		# process request

		reply = rot13(request)

                # send reply
		conn.sendall(reply.encode('ascii'))
		# print for debug
		print(reply)

		# sleep for 1 second to wait the client to close the socket
		time.sleep(1)
		conn.close()

"""
The BSD server creates a socket, uses bind to attach that socket to a port,
and configures it as a listening socket.
This allows the server to receive incoming connection requests.
Afterwards, accept is called, which will block the socket,
until an incoming connection request is received
"""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	# AF_INET means using IPv4
	# SOCK_STREAM means using TCP
	# use SOCK_DGRAM for UDP

	# BINDING
	s.bind((HOST, PORT))
	# LISTEN
	s.listen()
	# LOOP
	while True:
		# ACCEPT
		conn, addr = s.accept()
		# fork, generating child
		pid = os.fork()
		# parent with pid > 0
		if pid > 0:
			"""
			print("I am parent process:")
			print("Process ID:", os.getpid())
			print("Child's process ID:", pid)
			"""
			# close parent process side socket
			conn.close()

		# child with pid = 0
		else:
			"""
			print("\nI am child process:")
			print("Process ID:", os.getpid())
			print("Parent's process ID:", os.getppid())
			"""

			# serve client request
			serve_request(conn)
			# close child process, parent process still running
			sys.exit()



