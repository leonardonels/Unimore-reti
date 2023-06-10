	[0] INTRODUZIONE A RETI E PROTOCOLLI
			Introduzione alle reti:
				Nodi: Host, Switch
				Link: Wired (cavi coassiali, fobra ottica, ...), Wireless		
			Circuit Switching: prenotazione di un canale di comunicazione riservato per processo
			Packet Switching: raggruppa i pacchetti e li instrada usando tutta la rete a disposizione
			Store-and-forward: unito al packet switching raggruppa i pacchetti in arrivo e li rispedisce sfruttando tutta la rete a disposizione
			Frame relay
			Asynchronous transfer Mode (ATM)
			Protocollo:
				Sintassi: insieme e struttura dei comandi e delle risposte, formato e messaggi
				Semantica: significato dei comandi, delle azioni, delle risposte da effettuare al momento della trasmissione e ricezione dei messaggi.
				Temporizzazione: specifica delle possibili sequenze temporali di emissione dei comandi e dei messaggi, nonché delle eventuali risposte
			PCI: Protocol Control Information (PCI) - header
			SDU: Service Data Unit - informazione
			PDU: Protocol Data Unit (PCI+SDU)
			
	[0] STANDARD	ISO/OSI:
				ISO: International Standard Organization
				OSI: Open System Interconnection
				si dividono in:
					Protocolli di comunicazione a livello di rete
					Protocolli di elaborazione a livello applicativo
				Livelli:
					Application: fornisce una interfaccia standard per i programmi applicativi che utilizzano la rete
					Presentation: risolve le differenze di fromato tra le diverse macchine
					Session: consente a utenti su macchine eterogenee di stabilire e coordinare sessioni
					Transport: controlla end-to-end della sessione di comunicazione e garantisce l'affidabilità del trasporto
					Network: fornisce i collegamenti e l'instradamento dei pacchetti nella rete (gestione degli indirizzi di ingresso e uscita)
					Data Link: gestisce i frame o i pacchetti trasformando la semplice trasmissione in una liena comunicativa priva di errori non rilevati
					Physical: gestisce i particolari meccanici ed elettrici della trasmissione fisica di un flusso di bit
			TCP/IP:
				Livelli:
					Application: usa i protocolli del livello trasporto per realizzare applicazioni di rete (http, smtp, telnet, ftp)
					Transport: estende i protocolli di livello ip tramite protocolli quali UDP e TCP
					IP: (network) protocollo per la consegna dei pacchetti, privo di connessione, non affidabile
					H2N: comprende il livello fisico e il livello data link del modello ISO/OSI
	
	[1-2] H2N	Esempi:
				LAN Wired
				LAN Wireless
				Mediante modem
			si divide in:
				livello 1 fisico
				livello 2 data link
					framing (incapsulamento del frame)
					accesso al link
					controllo di flusso
					ricerca di errori
					correzione di errori
					half duplex o full duplex
			simile a protocollo trasporto (cone tcp):
				h2n si opera a livello di singolo link
				trasporto opera a livello di host end-to-end
			il livello h2n comunica tramite FRAME
			collegamenti:
				broadcast: molti host connessi ad un unico canale di comunicazione (Wireless LAN)
				punto-punto: due host per mezzo di comunicazione
			Modalità di trasmissione:
				Unicast: uno a uno
				Multicast: uno a molti
				Anycast: uno ad ALMENO uno
				Breadcast: uno a tutti
			NIC: Network Interface Card (con connettore RJ45)
			MAC: Media Access Control
			FRAME:
				Preambolo: 8 byte primi 7 10101010, l'ultimo 10101011, serve sincronizzare i clock.
				Indirizzo di destinazione: 6 byte, contiene l'indirizzo MAC, quando un adattatore riceve un frame, lo scarta se l'indirizzo MAC di destinazione non corrisponde la proprio
				Indirizzo di sorgente: 6 byte, contiene l'indirizzo MAC
				Tipo: 2 byte, serve all'adattatore per sapere a quale dei protocolli dello strato di rete debba essere passato il campo dati di ciascun frame ricevuto 
				Dati: minimo di 46 byte, massimo di 1500 byte, contiene il datagramma IP contenete i dati reali, se superano i 1500byte devono essere frammentati o passati al jumbo frame con un massimale di 9000 byte, se sono meno di 46 byte, dimensione minima, il campo dati deve essere riempito (stuffing) con byte di riempimento che verranno rimossi in ricezione.
				CRC: 4 byte, controllo a ridondanza ciclica, permette all'adattatore che riceve i dati di rilevare la presenza di un errore nei bit del frame ricevuto, quando un host riceve il frame ricalcola il CRC e vede se corrisponde.
			ARP: ADDRESS RESOLUTION PROTOCOL
				gli indirizzi ip non sono riconosciuti in hardware, ARP si occupa di trasformare l'indirizzo IP di un host della stessa LAN nel corrispondente indirizzo MAC
				è incluso nella suite TCP/IP, richiede in broadcast, riceve la risposta in unicast, ciascun host effettua un caching temporaneo delle risoluzioni arp
			RARP: REVERSE ADDRESS RESOLUTION PROTOCOL
				operazione inversa ad arp, dato un indirizzo mac ricava l'indirizzo IP corrispondente
			Apparati di rete:
				Hub:
				Bridge:
				Switch:
				Switch di livello 3:
		
	
