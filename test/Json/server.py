#!/usr/bin/env python3

import socket
import sys
import time
import os
import re
import json

# Standard loopback interface address (localhost)
HOST = '127.0.0.1'
# Port to listen on (non-privileged ports are > 1023)
PORT = 8080

def serve_request(conn):
	# receive request from client
	request_json = conn.recv(1024).decode('ascii')
	# print for debug	
	print(request_json)

	# filename file to be found
	request = json.loads(request_json)
	filename = request["filename"]

	# find client file in directory files
	files = os.listdir('files')
	found = False
	for f in files:
		if filename == f:
			found = True
			break

	# control
	if not found:
		# file not found
		conn.sendall(f'ERR: File {filename} not found\r\n'.encode('ascii'))
	else:
		# file found
		conn.sendall(f'OK: File {filename} found, sending information...\r\n'.encode('ascii'))

		# process request
		filesize = os.stat(f'files/{filename}').st_size	# return size in Bytes
		reply = {"filename": filename, "filesize": str(filesize)}
		reply_json = json.dumps(reply)

		# send reply
		time.sleep(0.5)
		conn.sendall(reply_json.encode('ascii'))
		conn.sendall(f'\n<{filesize} bytes of file content>'.encode('ascii'))

		# opening file found and reading content
		f = open(f'files/{filename}', "r")
		content = f.read()
		f.close()

		# send content to client
		time.sleep(1)
		conn.sendall(content.encode('ascii'))

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



