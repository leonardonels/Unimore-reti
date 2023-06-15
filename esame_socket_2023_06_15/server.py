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
# Porta su cui ascoltare (le porte non riservate sono > 1023)
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
	# riceve la richiesta dal client
	request_json = conn.recv(1024).decode('ascii')
	# stampa per debug	
	print(request_json)

        # isola le due variabiloi dalla richiesta in formato Json
	request = json.loads(request_json)
	ip = request["netid"]
	netmask = request["netmaskCIDR"]

        #verifica che le due variabili siano coerenti tra loro
	b=verifica_coerenza(ip, netmask)

	# logica
	if not b:
		# non coerente
		reply = {"status": "ERROR"}
		reply_json = json.dumps(reply)
		conn.sendall(reply_json.encode('ascii'))
	else:
		# coerente
		
		# trova gli indirizzi minimi e massimi
		indirizzo_min, indirizzo_max = calcola_indirizzi_sottorete(ip, netmask)

                # prepara la risposta
		reply = {"status": "OK", "IPmin": indirizzo_min, "IPmax": indirizzo_max}
		reply_json = json.dumps(reply)

		# spedisce la risposta
		conn.sendall(reply_json.encode('ascii'))

                #chiude la connessione
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
		# fork, genera il figlio
		pid = os.fork()
		# padre con pid > 0
		if pid > 0:
			"""
			print("I am parent process:")
			print("Process ID:", os.getpid())
			print("Child's process ID:", pid)
			"""
			# chiude la socked dal lato del padre
			conn.close()

		# figlio con pid = 0
		else:
			"""
			print("\nI am child process:")
			print("Process ID:", os.getpid())
			print("Parent's process ID:", os.getppid())
			"""

			# serve la richiesta del client
			serve_request(conn)
			# chiude il processo figlio
			# il padre continua ad andare in attesa di altre richieste
			sys.exit()



