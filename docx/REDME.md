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
				Hub: semplici ed economici, ripetitore a livello dei singoli bit in ingresso su di una interfaccia su di tutte le interfaccie, gli hub non isolano il DOMINIO DELLE COLLISIONI
				Bridge: (software) dispositivo di livello 2 (link layer), opera a livello di frame esaminando l'header dei frame ed inoltrandoli selettivmente, esegue un filtraggio sul MAC, isola i dominii di collisione, trsaparente per gli host, mantengono delle tabelle di filtraggio costruite automaticamente senza bisogno dell'intervento di amministratori di rete, il bridge impara la localizzazione del mittente dalla ricezione, nelle tabelle di filtraggio usa un parmetro TTL, generalmente di 60 minuti
				Switch:	sono praticamente bridge ad alte prestazioni con molte interfacce
					switch store-and-forward: attende l'arrivo dell'intero frame prima di inoltrarlo
					switch cut-through: attende l'arrivo della parte del frame contente l'indirizzo di destinazione per iniziare a instradare il pacchetto che ta ancora arrivando, non verifica il byte di controllo
			VLAN: Virtual LAN
				lo standard 802.1Q del 2003 definisce le specifiche che permettono di definire più reti locali virtuali (VLAN) distinte, utilizzando una stessa infrastruttura fisica
				ogni vlan si comporta come se fosse una rete locale separata dalle altre
					i pacchetti broadcast sono confinato all'interno della vlan
					la comunicazione di livello 2 è confinata all'interno della vlan
					la connettività tra diverse vlan può essere realizzata solo a livello 3 attraverso routing
				vlan permettono un risparmio, aumento di prestazioni, aumento della sicurezza e una maggiore flessibilità
				la connettività tra diverse vlan può essere realizzata solo a livello 3 attraverso routing
				le vlan possono essere:
					port based: assegnazione statica port-vlan (partizionamento di un bridge fisico i più bridge logici), non richede l'osservanza dello standard 802.1Q, ma solo che il bridge sappia configurarla secondo lo standard
					tagged: viene usato lo standard 802.1Q per condividere lo stesso link fisico tra vlan differenti, LO STANDARD DEFINISCE UNA MODIFICA DEL FORMATO DEL FRAME ETHERNET AGGIUNGENDO 4 BYTE CHE TRASPORTANO LE INFORMAZIONI SULLA VLAN, il tag deve essere comune nella vlan
					
				per saper gestire reti virtuali i bridge devono saper svolgere funzioni di:
					ingress: comprendere la vlan sorgente
					forwarding: invio corretto
					egress: comunicazione corretta della vlan sorgente
				gli ISP usano un secodno standard 802.1AD che divide la rete in due vlan, una prima S-tag gestita solo dall'isp ed una seconda C-tag per l'utente
	[3]	IP	
