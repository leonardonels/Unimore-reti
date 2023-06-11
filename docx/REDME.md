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
			consegna non affidabile dei pacchetti:
				consegna priva di connessioni
					ogni pacchetto è trattato in modo indipendente da tutti gli altri
				consegna con impegno (best efford):
					tentativo di consegnare ogni pacchetto (possibili inaffidabilità)
				consegna non garantita, i pacchetti possono essere persi, duplicati, ritardati, o conseganti senza ordine
			layout del datagram ip
				header del datagram:
					VERS: 4 bit, bersione del protocollo IP
					HLEN: 4 bit, lunghezza dell'header del datagram in parole da 32 bit, generalmente 5
					SERVICE TYPE: 8 bit , specifica come si richiede che sia trattato il datagram (D - basso ritardo; T - alto throughput; R - alta affidabilità; DS - DiffServ, definisce per-hop behavior, usa class selector per la priorità di traffico come best effort, priority o immediate; ECN - explicit congestion notification)
					TOTAL LENGHT: 16 bit, lunghezza del datagram IP in byte (64 kbyte)
					IDENTIFICATION: 16 bit, intero che indentifica il datagram
					FLAGS: 4 bit, controllo della frammentazione (0 - reserved; DF - don't fragment; MF - more fragments)
					FRAGMENT OFFSET: 12 bit, la posizione del frammento nel datagram originale
					TIME TO LIVE: 8 bit, decremento da ciascun router che gestisce il datagram, se uguale a 0 il datagram viene eiliminato
					PROTOCOL: 8 bit, indica quale protocollo di livello superiore può utilizzare i dati contenuti nel datagram
					HEADER CHECKSUM: 16 bit, serve per controllare l'integrità dei dati trsportati nell'header
					SOURCE IP ADDRESS: 32 bit
					DESTINATION IP ADDRESS: 32 bit
					IP OPTIONS: 0-32 bit, campo opzionale di lunghezza variabile, server per testing e debugghing della rete
					PADDING: campo opzionale, serve a far allineare l'header ai 32 bit, presente solo se ip options presenta una lunghezza variabile
				payload
			indirizzo ip è diviso in:
				netid: prefisso di rete, identifica la rete
					calssi di net id:
						classe a: 1 byte netid e 3 byte host id, primo byte 0xxx, da 0.1.0.0 a 127.255.255.255
						classe b: 2 byte netid e 2 byte host id, primo byte 10xx, da 128.0.0.0 a 191.255.255.255
						classe c: 3 byte netid e 1 byte host id, primo byte 110x, da 192.0.0.0 a 223.255.255.255
						classe d: indirizzi di multicast, primo byte 1110, da 224.0.0.0 a 239.255.255.255
						classe e: indirizzi riservati per esperimenti, primo byte 1111, da 240.0.0.0 a 255.255.255.254
				hostid: identifica l'host all'interno della rete
			un host conosce il proprio indirizzo ip tramite:
				configurazione manuale: configurazione da parte dell'amministratore del sistema
				DHCP: Dynamic Host Configuration Protocol, allocazione dinamica effettuata da un server speciale
			limited broadcast address: tutti i bit uguali a 1 255.255.255.255
			this host in thi network: tutti i bit a 0 0.0.0.0
			network address: ip address con hostid a 0
			ip broadcast address: ip address con host id a 1
			netmask: indica i bit di netid mediante and logico con il netid, es: 11111111.11111111.11111111.00000000
			subnetting e supernetting:
				opportunità:
					sottoclassi di indirizzi ip (subnet), per otganizzazioni
					sopraclassi di indirizzi ip (supernet), per ISP
				vantaggi: 
					maggiore flessibilità nella ripartizione degli indirizzi all'interno di una organizzazione
					si facilitano le operazioni di routing idetificando insiemi di indirizzi
			l'architettura della rete è lascamente gerarchica
				host terminali -> isp locali -> isp regionali -> isp globali
			i router sono aggregati in regioni chiamte Autonomus System (AS)
				Autonumus System: 
					un insieme di reti IP (network prefix) e di router sotto il controllo di una organizzazione (o consorzio di) nell'ambito del quale si utilizza una politica di interior routing. Gli AS sono le unità delle politiche di exterior routing, come nel caso del BGP
					gli AS dall'esterno vengono visti come un'unica entità
					ciascun AS è caratterizzato da un numero identificativo su 2 byte (1-64511, 64512-65536 sono riservati) e uno o più network id o network prefix
				gli ISP regionali (nazionali) e internazionali sono collegati tra di loro al più alto livello dalla gerarchia, mediante peering point (privati) oppure mediante Internet Exchange Point (una volta chiamati network access point)
					peering point: interconnessione stabilita tra peer, in questo caso AS, con lo scopo di scambiarsi il traffico dei relativi utenti
					internet exchange point: tipicamente consorzi indipendenti senza scopo di lucro, talvolta creati fra AS, talvolta supoortati da finanziamenti pubblici, offorno servizi tra gli associati, ma anche ad altri
						permettono agli AS di scambiarsi traffico mediante protocollo BGP
			dal punto di vista delle applicazioni di rete, internet è una unità trasparente, nella maggior parte dei casi
			IP Forwarding (inoltro): 
				meccanismo con cui un router trasferisce i pacchetti da una interfaccia d'ingresso a quella di uscita
				viene effettuato da ogni router
				il next hop router appartiene ad una rete alla quale il router è collegato direttamente
				ogni host e ogni router ha una tabella di routing in cui ciascuna riga fornisce il next-hop router per ogni possibile destinazione (le tabelle possono arrivare a 50k righe)
				tramite tecniche di aggregazione ogni riga può fornire informazioni per molte destinazioni
				le tabelle seguono la regola del LONGEST PREFIX MATCHING che le vogliono ordinate con prima le maschere più lunghe (es. /25) e poi le più corte (es. /20)
				si può utilizzare anche il router di default comune a più indirizzi di destinazione oppure il router geografico
			caratteristiche delle tabelle di routing:
				routing statico:
					la tabella non è modificata dal router, da usare nel caso di reti piccole con pochi cambiamenti, sconveniente nel caso di cambiamenti topologici
				routing dinamico:
					la tabella di routing è modificabile dal router al variare delle condizioni sulla rete, lo scambio delle informazioni tra router avviene tramite protocolli quali RIP, OSPF o BGP
			algoritmi di routing:
				obiettivo: determinatre il percorso ottimale, costo minimo, uso di grafico pesato
				fattori statici: topologia della rete
				fattori dinamici: traffico della rete, guasti
				anche le politiche di routing dei vari router influenzano il routing
				principali algoritmi:
					routing distribuito: nessun nodo ha una informzione completa del costo di tutti i link della rete, es. distance vector protocol
						distance vector protocol: viene scambiato un vettore di distanze rispetto alle varie destinazioni (algoritmo di Bellman-Ford)
							data l'estensione della rete non si può salvare la distanza da ogni nodo, inoltre per evitare cicli si rende necessario inviare anche il percorso, ciò permette al router di verificare di non essere presente nel percorso tra lui e la destinazione, diventa un problema la quantità di dati trasmessi, proporzionale all distanza tra i nodi
					routing centralizzato: ogni nodo possiede un'informazione globale della rete, es link state protocol
						link state protocol:
							ogni nodo calcola lo stato dei link ad esso connessi, poi, periodicamente, trasmette identità e costi dei link connessi, ciascun nodo calcola i cammini di costo minimo verso tutti gli altri nodi della rete mediante l'algoritmo di Dijkstra
					periodicamente vengono inviati in broadcast su tutti i link del nodo dei pacchetti LSP con le seguenti infromazioni:
						node ID
						lista di vicini e costo dei rispettivi link
						informazioni aggiuntive:
							numero di sequenza per accorgersi di errori in caso di delivery out-of-order delle informazioni
							TTL per evitare di usare informazioni vecchie e quindi non affidabili
					la propagazione delle informazioni avviene attraverso flooding (inondazione):
						quando un nodo riceve un LSP, se è più recente viene salvato nel database e una copia viene inoltrata su tutti i link connessi al nodo, altrimenti viene scartato
					link state vs distance vector
						LS usa messaggi più piccoli
						LS propaga un numero di messaggi decisamente molto più grande [O(n) n nodi del grafo]
						DV comunica solo ai vicini = meno messaggi
						LS molto veloce
						DV veloce solo tramite aggiornamenti molto frequenti, così rischiando pero instabilità
						LS ha un requisito di memorizzazione molto alto
						DV mantiene salvate solo lo stato dei vicini
						LS calcola i percorsi in maniera indipendente da ogni nodo
						DV calcola i percorsi in base agli alti nodi
					link state viene usato solitamente negli AS
					distance vector viene solitamente usato tra AS
			per il routing all'interno di un AS (intra-AS) i router utilizzano qualche interior gateway protocol dove i router di un AS possono possedere un'informazione completa du tutti gli altri router dell'AS
			per il routing verso altroi AS (inter-AS) viene utilizzato qualche Exterior Gateway Protocol (prima EGP, ora BGP, Border Gateway Protocol) ciascun AS può usare metriche multiple per il routing interno, ma appare come un unico AS ad altri AS
			in base agli accordi commerciali tra AS, questi possono essere impostati come:
				stub: AS 2 è connesso al mondo solo tramite AS1
				multi-homed: gli AS sono connessi tra di loro, ma non permettono il traffico di cui non sono origine o destinazione
				transit: AS che permette il forwarding di traffico di cuo non è ne origine ne destinazione
			intra-AS: si usa prevalentemente OSPF (open shortest path first, basato su link state), successore di RIP (routing information protocol, basato su distance vector)
			inter-AS: BGP ha sostituito EGP che presupponeva una struttura ad albero senza cicli, entrata in crisi con la introduzione delle dorsali; BGP sfrutta un algoritmo di distance vector
				BGP fa uso di connessioni TCP semi-permanenti, due peer BGP che si scambiano messaggi sulla connessione TCP formano una sessione BGP
					sessioni che possono essere difinite:
						E-BGP: sessioni etserne tra router di AS diversi
						I-BGP: sessioni interne tra router dello stesso AS
					Border Router: gestisce sessioni E-BGP
					Transit Router: gestisce sessioni I-BGP
				OSPF open source, basato su link state protocol
					rispetto a RIP, OSPF
						aumenta la sicurezza tramite crittografia dei messaggi 
						permette di usare più percorsi per instradare il traffico (rip solo uno)
						integra supporto unicast e multicast
						permette di strutturare grandi domini di instradamento in gerarchie AS
					OSPF è strutturato:
						header (comune):
							numero di versione
							tipo:
								1 HELLO: scoperta di router, scambio di parametri sul funzionamento OSPF adiacenti
								2 DB description: contenuto del DB
								3 link state req: richiesta di informazioni relative a una porzione del link state DB
								4 link state update : infromazioni relative a link mandato in risposta a request, usato per propagare periodicamente gli update nella struttura della rete
								5 link state ACK: acknowledgement della ricezione di un messaggio di update
							checksum
							tipo e informazioni per autenticazione
						corpo (che dipende dal tipo)
					consente una suddivisione di grandi AS in aree così da avere una gerarchia interna a due livelli:
						aree locali (1-x)
						area backbone
							instrada il traffico tra le aree del AS
							contiene tutti i router di confine (boarder router) (gateway router)
								router di confine che instradano il traffico verso altri AS
							router di backbone instrada il traffico all'interno dell'area di backbone
							router di confine area comunicano i percorsi verso altre aree locali dell'AS ai router di quell'area
					si usa link state per ogni area
			Protocolli:
				che offrono servizi:
					portano "dati utente"
					le loro DPU vengono imbustate in accordo alla pila iso-osi
					es.: tcp
				di supporto:
					portano "dati di controllo" e non offrono direttamente servizi
					LA LORO POSIZIONE NELLO STACK È INDIPENDENTE DA COME VENGONO IMBUSTATE LE PDU
					es.: ICMP(lvl3), ARP/RARP(lvl2), protocolli di routing(lvl2)
						potocollo ICMP (Internet Control Message Protocol):
							notifica situazioni di errore o animalie
							supporta debugging interattivo della rete
							funziona a IP e viaggia in pacchetti IP
							porta informazioni di controllo e di notifica errori
							NON porta dati
							interviene quando c'è una anomalia nel processo di instradamento e una condizione di errore deve essere notificata al mittente del pacchetto
							utile a testare la taggiungibilità del livello IP di un host remoto con un dato indirizzo
							se il pacchetto viene frammentato solo il primo frammento puo generare un messaggio di errore ICMP
							broadcast e multicast non generano ICMP
							DESTINETION_UNREACHABLE:
								un gateway vede la rete di destinazione a disnatnza infinita
								l'host non risponde ad una chiamata ARP
								l'host destinazione non conosce il protocollo del pacchetto
								il pacchetto non può essere frammentato (è richiesta la frammentazione e DF è impostato a 1)
			IPV6:
				uso di numeri in notazione esadecimale
				8 blocchi di 16 bit (4 cifre ciascuno)
				regola: gruppi di 4 cifre di valore 0 posso essere semplificati ad una unica cifra 0 oppure omessi
				il prefisso ::/96 di 96 zeri trasforma un udirizzo IPV4 in IPV6
				header ipv6 (40 bit) è composto:
					version: 4 bit, vale 6 per ipv6
					traffic class: 8 bit, analogo al campo tipe of service di ipv4, indica la priorità del datagramma
					flow label: 20 bit: ipostato da una sorgente per indicare pi	u datagrammi come apparteneti ad un unico flusso di traffico, i router possono usare questo campo per istradare allo stesso modo tutti i datagrammi di uno stesso flusso, se non usato ha valore nullo
					payload lenght: 16 bit
					next header: tipo di protocollo usato per il payload
					hop limit: come il TTL per ipv4
					sorce address
					destination address
				ipv6 parte dal presupposto che frammentare è male
				la frammentazione non è gestita a livello di singoli router intermedi
				solo la sorgente può frammentare
					in caso di messaggio troppo grande per il livello 2
						viene scartato il messaggio
						si genera il messaggio di errore ICMP
				la corruzione dell header è estremamente rara, la generazione del checksum al variare del TTl è onerosa a livello dei router, ipv6 decide di non gestire questa operazione
				è possibile avere opzioni come nel payload del datagram IP
				NDS Neighbor Discovery Protocol:
					protocollo ipv6 per:
						apprendimento di parametri come MTU e hop limit
						configurazionr automatica di indirizzi
						address resolution (come RARP)
						neighbor unreachability detection: identificare quando un vicino non è più raggiungibile
						duplicate address detection
						neighbor discovery: 5 tipi di pacchetto ICMPv6
							router solicitation: inviato quando una interfaccia viene attivata, chiede ai router di mandare messaggi di tipo router advertisement immediatamente
							router advertisement: i router inviano periodicamente un messaggio che informa la rete della loro presenza, anche in risposta di un ruouter solicitation
								contenuto del messaggio:
									lista di prefissi usati per decidere il routing
									flag che indicano usi specifici di alcuni prefissi
									parametri come MTU o numero di hop che sono associati ad una destinazione
							neighbor solicitation: mandato da un nodo per ottenere un indirizzo mac di un vicino, usato anche per determinare se un vicino è ancora raggiungibile (arping)
							neighbor advertisement: risposta a messaggio di tipo neighbor solicitation
							redirect: informare un router di una destinazione migliore per raggiungere una destinazione
						link-layer address change: un nodo che sa di aver cambiato indirizzo MAC può mandare un messaggio di tipo neighbor advertisement agli altri nodi per aggiornare la loro cache
						inbound load balancing: i router possono non cmunicare i loro MAC address per consentire una risposta selettiva qaundo più ruoter possono gestire lo stesso percorso (es.: round robin policy)
				per aiutare la diffusione di ipv6 sono stati itrodotti i tunnel ip:
					per connettre isole, aree, in cui è stato implemnato ipv6 al 100% si inseriscono i d iatagramma ipv6 nel payload di un datagramma ipv4
	[4] TRASPORTO:	il livello trasporto estende il servizio di consegna con impegno proprio del protocollo IP tra due host terminali ad un servizio di consegna a due processi applicativi in esecuzione sugli host
		il livello trasporto aggiunge:
			multiplazione e demultiplazione messaggi tra processi
				il protocollo IP non consegna dati tra processi applicativi in esecuzione sui nodi terminali (compito del protocollo trasporto)
				ogni segmento dello strato di trasporto possiede un campo contenete l'informazione usata per determinare a quale processo deve essere conseganto il segmento.
				la demultiplazione avviene dal lato del dedtinatario
				multiplazione: creazione dei segmenti provenienti dal mesaggi di diversi processi applicativi, avviene dal lato del mittente
			rilevamento dell'errore mediante checksum (non corregge)
		udp e tcp attuano la multiplazione/demultiplazione includendo due campi speciali nell'header del segmento:
			numero di porta del mittente: numero di 16 bit compreso tra 0 65535, numeri di porta tra 0 e 1023 sono noti e riservati per protocolli applicativi come http(80), telnet(23), smtp(25), dns(53), porte tra 1024 e 49151 sono porte registrate, NON DEVONO ESSERE USATE SENZA UNA PRECEDENTE AUTORIZZAZIONE
			numero di porta del destinatario
		UDP - User Datagram Protocol
			è un protocollo di trasporto leggero, ovvero dotato delle funzionalità minime di trasporto
			multiplazione e demultiplazione: aggiunta di porta al messaggio
			controllo dell'errore: include nell'header un campo cheksum
				serve la conoscenza dell'indirizzo IP del mittente e del destinatario
				il processo mittente a livello UDP non può acquisire l'indirizzo IP del destinatario dall'applicazione di livello superiore
				il processo mittente a livello UDP chiede al livello IP di costruire lo pseudo-header, calcolare il checksum UDP ed eiliminare lo psudo-header
			servizio di consegna non garantito: best effort
			servizio senza connessione: no handshaking, ogni segmento UDP è trattato in modo indipendente
		affidabilità:
			serve notificare al mittente la presenza di errori e la richeista di una ritrasmissione
				messaggi di ACK e NAK
			aggiunta dell'id del messaggio per evitare duplicati o ritrasmissioni non volute
			aggiunta di timeout nel caso non arrivi il messaggio di ACK
		TCP - Transmission Control Protocol: offre servizi aggiuntivi rispetto a UDP
				trasferimento affidabile dei dati (controllo di flusso, acknowledgment e timer)
				controllo di gestione
			orientato alla connessione: comprende le fasi di instaurazione, utilizzo e chiusura delle connessioni
				viene creata una connessione tra i due host prima del trasferimento di qualunque dato tra le applicazioni e chiusa dopo il completamento del strasferimento dati
				fasi:
					instaurazione
					utilizzo
					chiusura
				il processo applicativo viene avvisato solo se:
					non si riesce a stabilire la connessione
					la connessione viene interrotta
			orientato al flusso di dati (byte stream): considera il flusso di dati dall'host mittente fino al destinatario
				la connessione viene trattata come un flusso continuo di byte
					il processo applicativo mittente scrive byte
					il livello TCP, per inviarli, accorpa i byte in un segmento TCP
					il livello IP incapsula ogni segmento TCP in un datagram IP
					il processo applicativo destinatario legge byte
				l'unita di trasmissione è il byte
			rispetto a UDP:
				trasferimento con buffer: i dati sono inseriti in un buffer e popi inseriti in un pacchetto quando il buffer è pieno
				connessioni full duplex
					TCp puè effettuare trasferimenti contemporaneamente in entrambe le direzioni della connessione, nell'ambito della stessa sessione
					ai processi applicativi questi appaiono come duie data stream non correlati
					TCP consente di sovrapporre (piggybacking) comunicazioni di dati e comunicazioni di controllo, con l'invio di informazioni di controllo (es.: ACK) insieme ai dati utente
			cosa TCP NON garantisce:
				comunicazione in tempo reale
					possibilità di ritardi molto lunghi nella rete
						 è possibile che giungano pacchetti molto molto vecchi
				garanzia di disponibilità banda tra mittente e destinatario
				multicast affidabile
			offre un livello di trasporto affidabile e orientato alla connessione su di un canale inaffidabile
				ACK+timeout+(ritrasmissione)
			permette la comunicazione tra host eterogenei
				tempi di trasmissione eterogenei
				possibilità di avere differenti capacità tra host e destinatario
				possibilità di avere congestioni nelle reti intermedie
					per queste ragioni TCP fa uso di BUFFER
						nuove problematiche:
							congestion control
								gestione del tasso di trasmissione in base allo stato di congestione della rete
							flow control
								l'host mittente non deve sovraccaricare l'host destinatario
			SEGMENTO TCP:
				payload: dati del byte stream
				header: informazioni di controllo per identificare i byte dati
					source port: 16 bit
					destination port: 16 bit
					sequence number: 32 bit, numero di sequenza frelativo al flusso di byte che si sta trasmettendo
					acknowledgement number: 32 bit, ACK relativo ad un numero di sequenza del flusso di byte che si sta ricevendo (poiché il flusso è bidirezionale vi è la possibilità di piggybacking)
					header lenght: 4 bit, lunghezza dell'header TCP in multipli di 32 bit
					reserved: 6 bit, per usi futuri
					code bits: 6 bit, scopo e contenuto del segmento
						URG: urgenti
						ACK: valore del campo acknowledgement è valido
						PSH: il destinatario deve passare i dati all'applicazione immediatamente
						SYN (synchronize), FIN, RST (reset): usati per instaurare, chiudere e interropere la connessione
					windows size: 16 bit, dimensione della finestra di ricezione (indica il numero di byte che si è disposti ad accettare in ricezione)
					checksum: 16 bit, controllo integrtià dei dati trasportati nel segmento TCP (del tutto analogo a quello del protocollo UDP)
					urgent pointer: 16 bit, puntatore al termine dei dati urgenti (es.: ˆC)
					TCP options: campo opzionale di lunghezza variabile (serve a negoziare la dimensione del segmento massimo scambiato)
						MSS: 	troppo piccolo -> overhead eccessivo dovuto agli header
							troppo grande -> elevati rischi di frammentazione nell'aatraversamento dei livelli dello stack sottostanti
							deafult -> 536 byte minimi, spesso usati 1450
						l'ACK viene mandato a livello del segmento originale, quindi se un frammento viene perso, tutto il segmento deve essere riinviato
					zero padding: per header con lunghezza multipla di 32 bit (se opzioni)
			instaurare e chiudere una connessione TCP
				una connessione deve essere instaurata prima di poter trasmettere dati
				modello client server
					client inizia una connessione
					server deve essere già attivo in attesa
				inizializzazione delle variabili TCP
					numeri di sequenza dei segmenti
					informazioni necessarie per la gestione del buffer di trasmissione e ricezione
				quando un client richiede una connessione, invia un segmento TCP speciale SYN segment al server
					il segmento SYN del client include:
						initial sequence number del client (ISN)
							nell'intestazione del segmento è riportato solo il numero di sequnenza del primo byte dei dati contenuto nel segmento
						ACK
						maximum receive window (MRW) del client
						maximum segment size (MSS)
						NON HA PAYLOAD, solo TCP header
					il client deve conoscere a chi spedire la richiesta, per cui nell'header del segmento deve specificare la porta del server
				per accettare la connessione, il server deve essere già in attesa di ricevere connessioni
				three-way handshaking:
					client -> server SYN=1 seq=client_isn
					server -> client SYN=1 seq=server_isn ACK=client_isn+1
					client -> server SYN=0 seq=client_isn+1 ACK=server_isn+1
				chiusura (polite) della conessione:
					client -> server FIN, seq=x
					server -> client ACK, seq=x+1
					server -> client FIN, seq=y
					client -> server ACK, seq=y+1
					il client TCP attende per un tempo TIME_WAIT (es.: 30 secondi) prima di chiudere definitivamente la connesione per gestire situazioni anomale ed errori
				chiusura (reset) della connessione:
					{server -> client, client -> server} RST=1
					l'altro chiude immediatamente la connessione
			trasferimento di dati:
				avviene in 3 fasi:
					handshaking
					trasmissione
					chiusura della connessione
			affidabilità del protocollo TCP
				ACK, timeout, (ritrasmissione)
				princpi:
					ogni trasmissione andata a buon fine viene notificata dall'host ricevente
					se l'host mittente non riceve ACK entro il timeout ritrasmette i dati
				come stabilire il tempo di time out:
					troppo breve e si effettuano troppe ritrasmissioni
					troppo lungo e ha una reazione troppo lenta alla perdita di segmenti
					deve essere MAGGIORE del RTT (round trip time)
					inizialmente si sceglieva timeout = bet*RTTmedio ove beta=2
					ora:
						sampleRTT:
							misura del tempo strascorso dalla trasmissione del segmento alla ricezione di ACK
							ignora ritrasmissioni o ACK cumulativi
							media pesata
						estimatedRTT:
							media pesata
							l'influenza dei campioni passati diminuisce esponenzialmente
						timeout(t)=estimatedRTT(t)+4*Dev(t)
						dove il margine di errore Dev(t)=(1-x)*Dev(t-1)+x*abs[sampleRTT(t)-estimatedRTT(t)]
				
						
				
				
			
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
