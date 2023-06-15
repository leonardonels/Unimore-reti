#!/usr/bin/env python3

import socket
import sys
import time
import os
import re
import json
import ipaddress

# Standard loopback interface address (localhost)
HOST = '127.0.0.1'
# Port to listen on (non-privileged ports are > 1023)
PORT = 8080

def verifica_coerenza(indirizzo_ipv4, netmask):
    try:
        # Converte l'indirizzo IP e la netmask in un oggetto IPv4Interface
        interfaccia = ipaddress.IPv4Interface(f"{indirizzo_ipv4}/{netmask}")
        
        # Verifica se l'indirizzo di rete corrisponde all'indirizzo IP fornito
        return str(interfaccia.network.network_address) == indirizzo_ipv4
    except ValueError:
        return False


def calcola_indirizzi_sottorete(indirizzo_ipv4, netmask):
        # Crea un oggetto di tipo IPv4Network utilizzando l'indirizzo IPv4 e la netmask
        rete = ipaddress.IPv4Network(f"{indirizzo_ipv4}/{netmask}", strict=False)
    
        # Ottieni l'indirizzo IP minimo e massimo della sottorete
        indirizzo_minimo = rete.network_address + 1
        indirizzo_massimo = rete.broadcast_address - 1
    
        return str(indirizzo_minimo), str(indirizzo_massimo)

def serve_request(conn):
	# receive request from client
	request_json = conn.recv(1024).decode('ascii')
	# print for debug	
	print(request_json)

	#
	request = json.loads(request_json)
	ip = request["netid"]
	netmask = request["netmaskCIDR"]
	#print(ip)
	#print(netmask)

	#
	b=verifica_coerenza(ip, netmask)

	# control
	if not b:
		# file not found
		reply = {"status": "ERROR"}
		reply_json = json.dumps(reply)
		conn.sendall(reply_json.encode('ascii'))
	else:
		# file found
		#conn.sendall(f'OK: File {filename} found, sending information...\r\n'.encode('ascii'))

		# process request
		#filesize = os.stat(f'files/{filename}').st_size	# return size in Bytes

		indirizzo_min, indirizzo_max = calcola_indirizzi_sottorete(ip, netmask)

		reply = {"status": "OK", "IPmin": indirizzo_min, "IPmax": indirizzo_max}
		reply_json = json.dumps(reply)

		# send reply
		#time.sleep(0.5)
		conn.sendall(reply_json.encode('ascii'))
		#conn.sendall(f'\n<{filesize} bytes of file content>'.encode('ascii'))

		# opening file found and reading content
		#f = open(f'files/{filename}', "r")
		#content = f.read()
		#f.close()

		# send content to client
		#time.sleep(1)
		#conn.sendall(content.encode('ascii'))

		# sleep for 1 second to wait the client to close the socket
		#time.sleep(1)
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



