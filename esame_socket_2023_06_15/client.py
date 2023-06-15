#!/usr/bin/env python3

import socket
import sys
import time
import json
import re

# Standard loopback interface address (localhost)
HOST = '127.0.0.1'
# Port to listen on (non-privileged ports are > 1023)
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

	# CONNECTION: contact server in listen
	s.connect((HOST, PORT))

	# asking user for filename
	request = input('inserisci un prefisso di rete con netmask in formato CIDR: ')
	
	# request to server

	m = re.match(r'^([0-9]+.[0-9]+.[0-9]+.[0-9]+)/([0-9]+)$', request)
	if m:
                ip=m.group(1)
                netmask=m.group(2)
                request = {"netid": ip,"netmaskCIDR":netmask}
                request_json = json.dumps(request)
                s.sendall(request_json.encode('ascii'))
                reply_json = s.recv(1024).decode('ascii')
                print(reply_json)

	# close socket
	else:
                print("-ERR")


	s.close()

