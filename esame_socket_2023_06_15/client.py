#!/usr/bin/env python3

import socket
import sys
import time
import json
import re

# Standard loopback interface address (localhost)
HOST = '127.0.0.1'
# Porta su cui contatatre il server (le porte non riservate sono > 1023)
PORT = 8080

# prima di cominciare prende la richiesta dell'utente per non aprire socket inutili
request = input('inserisci un prefisso di rete con netmask in formato CIDR: ')

# esegue un controllo tramite regular expression (regex)
m = re.match(r'^([0-9]+.[0-9]+.[0-9]+.[0-9]+)/([0-9]+)$', request)

# se non fa match da errore e chiude
if not m:
        print("-ERR")

# se non da errore prosegue aprendo la socket
else:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))

                # inserisce in due variabili le due parti che compongono l'imput
                ip=m.group(1)
                netmask=m.group(2)

                # le due variabili vengono inserite in un dizionario
                request = {"netid": ip,"netmaskCIDR":netmask}

                # il dizionario viene incapsulato in formato json
                request_json = json.dumps(request)

                # il messaggio in formato Json viene spedito al server
                s.sendall(request_json.encode('ascii'))

                # il client attende la risposta, ricevuta, la stampa e chiude
                reply_json = s.recv(1024).decode('ascii')
                print(reply_json)
                s.close()

