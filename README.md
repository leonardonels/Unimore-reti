	# Bibbia UNIMORE-reti
	
	#nano /etc/network/interfaces
	#vale per nodi statici o per il dhcp_server nel caso di reti dhcp
		auto eth0
		iface eth0 inet static
			address 192.168.1.1/24
			gateway 192.168.1.254	
			post-up ip route add 1.1.1.1/32 dev eth0
			post-up ip route add 192.168.2.0/24 via 1.1.1.1
		
			


	#vale per nodi di una rete dhcp
		auto eth0
		iface eth0 inet dhcp
			hwaddress 02:04:06:11:22:33	#necessario solo se si vuole dedicare un indirizzo ip alla macchina con questo indirizzo MAC
	
	------------------------------------------------------------------
	
	#nano /etc/ethers
		02:04:06:11:22:33 192.168.1.3
	
	------------------------------------------------------------------
	
	#nano /etc/hosts
		192.168.1.254 server server.reti.org
		192.168.1.3 client3 client3.reti.org
		
	------------------------------------------------------------------
	
	#nano /etc/dnsmasq.conf
	
		no-resolv	#don't look for other nameservers
		
		read-ethers	# read /etc/ethers file
		
		interface=eth0	# network interface for DHCP
		
		domain=reti.org	# network domain name
		
		dhcp-option=3,192.168.1.254	#3 per default gateway
	
		dhcp-option=6,192.168.1.254	#6 per dns server
			# or...
			# dhcp-option=option:router,192.168.1.254
			# dhcp-option=option:dns-server,192.168.1.254
		
		dhcp-range=192.168.1.10,192.168.1.15,1h		#range di indirizzi da assegnare, l'ultimo parametro indica il lease time (tempo durante il quale il dhcp server riserva un indirizzo assegnato)
							#il range e' mecessario affinche' il parametro dhcp-host venga preso in consideazione
		
		dhcp-range=192.168.1.0,static	#per assegnare un range di indirizzi utilizzati solo dalle macchine specificate tramite dhcp-host
		
		dhcp-host=02:04:06:11:22:33,client3,192.168.1.3,1h	#utile ad assegnare un indirizzo specifico ad un determinato host
		
		address=/www.hackerz.com/192.168.1.1	# override address (can also use /etc/hosts)
						#usare solo hosts e ethers e' deletereo poiche' le macchine vengono vincolate ad indirizzi non riservati
						
	------------------------------------------------------------------		
						
		systemctl enable dnsmasq	#per abilitare il dhcp server all'avvio

		service dnsmasq start	#per avviare il dhcp server

	------------------------------------------------------------------
		
	#nano /etc/sysctl.conf	per abilitare il forwarding dei pacchetti
	#rimuovi il commento alla riga seguente
		net.ipv4.ip_forward
		
	#per applicare la modifica
		sysctl -p /etc/sysctl.conf	
		
	------------------------------------------------------------------
	#eliminare la regola di tc corrente
		tc qdisc del root dev eth0
	
	#Ext deve limitare il traffico in uscita (ad esempio file disponibili su Ext e scaricati da qualunque altra macchina) a una bandwidth massima di 10MBit/s.
		post-up tc qdisc add dev eth0 root tbf rate 10Mbit latency 50ms burst 1539		#traffic shaping stateless
		
		tc qdisc add dev eth0 root handle 1: htb default 20					#traffic shaping statefull
		tc class add dev eth0 parent 1: classid 1:1 htb rate 100Mbit burst 15k
		tc class add dev eth0 parent 1:1 classid 1:10 htb rate 1Mbit burst 15k
		tc class add dev eth0 parent 1:1 classid 1:20 htb rate 20Mbit ceil 50Mbit burst 15k
		tc qdisc add dev eth0 parent 1:10 handle 10: pfifo limit 50
		tc qdisc add dev eth0 parent 1:20 handle 20: pfifo limit 50
		tc filter add dev eth0 protocol ip parent 1:0 prio 1 u32 match ip dst 10.0.1.129{ip da rallentare} flowid 1:10
	
	#strumento di test
		dd if=/dev/zero bs=10M count=1 | nc <netcat server> <netcat port>
		
	------------------------------------------------------------------
	
	#iptables
	#elenco di regole
		iptables -t filter -L -n -v
	
	#blocco di tutto il traffico
		iptables -t filter -P INPUT DROP
		iptables -t filter -P OUTPUT DROP
		iptables -t filter -P FORWARD DROP
		
	#PING - ICMP
		#ping bidirezionale
		iptables -t filter -A FORWARD -p icmp -i eth0(interfacia A del ping) -o eth0(interfacia B del ping) -j ACCEPT
		iptables -t filter -A FORWARD -p icmp -o eth0(interfacia A del ping) -i eth0(interfacia B del ping) -j ACCEPT
		
		#ping monodirezionale
		iptables -t filter -A FORWARD -p icmp -i eth0(interfacia di richiesta del ping) -o eth0(interfaccia di risposta del ping) -j ACCEPT					#da testare
		iptables -t filter -A FORWARD -p icmp -o eth0(interfaccia di richesta del ping) -i eth0(interfaccia di risposta del ping) -state --state RELATED,ESTABLISHED -j ACCEPT	#da testare
	
	#DHCP
		iptables -t filter -A INPUT -i eth0(interfaccia ingresso verso il client) -p udp --dport 67 --sport 68 -j ACCEPT
		iptables -t filter -A OUTPUT -o eth0(interfaccia ingresso verso il client) -p udp --sport 67 --dport 68 -j ACCEPT
		
		#se firewall fa da dhcp relay e non dhcp server, dhcp server in un'altra lan
		iptables -t filter -A OUTPUT -o eth1(interfaccia verso il dhcp server) -p udp -s 155.185.1.6(indirizzo firewall-dhcp relay) --sport 67 -d 192.168.1.253(indirizzo dhcp server) --dport 67 -m state --state NEW,ESTABLISHED -j ACCEPT
		iptables -t filter -A INPUT -i eth1(interfaccia verso il dhcp server) -p udp -s 192.168.1.253(indirizzo dhcp server) --sport 67 -d 155.185.1.6(indirizzo firewall-dhcp relay) --dport 67 -m state --state ESTABLISHED -j ACCEPT
	
	#DNS LAN
		iptables -t filter -A INPUT -i eth0(interfaccia ingresso verso il client) -p udp --dport 53 -j ACCEPT
		iptables -t filter -A OUTPUT -o eth0(interfaccia ingresso verso il client) -p udp --sport 53 -j ACCEPT
	
	#DNS DMZ
		iptables -t filter -A INPUT -i eth0(interfaccia ingresso verso DMZ) -p udp --dport 53 -j ACCEPT
		iptables -t filter -A OUTPUT -o eth0(interfaccia ingresso verso DMZ) -p udp --sport 53 -j ACCEPT
	
	#PERMETTERE AL SERVER WEB TRAFFICO SULLA PORTA 80 WWW HTTP
		iptables -t filter -A FORWARD -p tcp --dport http -i eth0(interfaccia ingresso verso il client) -o eth0(interfaccia in uscita verso il web server) -d 192.168.200.1 -m state --state NEW,ESTABLISHED -j ACCEPT
		iptables -t filter -A FORWARD -p tcp --sport http -o eth0(interfaccia ingresso verso il client) -i eth0(interfaccia in uscita verso il web server) -s 192.168.200.1 -m state --state ESTABLISHED -j ACCEPT
	
	#PERMETTERE AL SERVER MAIL TRAFFICO SULLA PORTA SMTP
		iptables -t filter -A FORWARD -p tcp --dport smtp -i eth0(interfaccia ingresso verso il client) -o eth0(interfaccia in uscita verso il mail server) -d 192.168.200.1 -m state --state NEW,ESTABLISHED -j ACCEPT
		iptables -t filter -A FORWARD -p tcp --sport smtp -0 eth0(interfaccia ingresso verso il client) -i eth0(interfaccia in uscita verso il mail server) -s 192.168.200.1 -m state --state ESTABLISHED -j ACCEPT
	
	#PERMETTERE IL PING DAL CLIENT AL SERVER
		iptables -t filter -A FORWARD -i eth0(interfaccia ingresso verso il client) -o eth0(interfaccia in uscita verso il server) -j ACCEPT
		iptables -t filter -A FORWARD -o eth0(interfaccia ingresso verso il client) -i eth0(interfaccia in uscita verso il server) -m state --state RELATED,ESTABLISHED -j ACCEPT
	
	#SSH
		iptables -t filter -A INPUT -i eth0.10 -p tcp --dport ssh -s {IP H1} -m state --state NEW,ESTABLISHED -j ACCEPT
		iptables -t filter -A OUTPUT -o eth0.10 -p tcp --sport ssh -d {IP H1} -m state --state ESTABLISHED -j ACCEPT

	------------------------------------------------------------------
	
	#REGOLE DI NAT [10.0.1.129 corrisponde al server nella dmz]
		iptables -t nat -A POSTROUTING -p tcp --dport www -s (netid da mascherare) -o eth1 -j MASQUERADE
		iptables -t nat -A PREROUTING -i eth1 -p tcp --dport www -d (IP del firewall in ingresso) -j DNAT --to-destination (IP del server dopo l'uscita del firewall)
		#per testare dnat server fare netcat al server al posto che al server di destinazione come port forwarding

	------------------------------------------------------------------
		
	$ ip addr add dev eth0 192.168.1.1
	$ ip addr show dev eth0
	$ ip link set dev eth0 up [down]
	$ ip link show
	
	------------------------------------------------------------------
	
	#come istallare marionnet su windows/linux
	#requisiti per windows: abilitare la virtualizzazione da bios e hyperV da "attiva o disattiva funzionalità di windows"
	|	powewrshell $ wsl --install -d Ubuntu-20.04
	|	Ubuntu-20.04 $ sudo apt update
	|	Ubuntu-20.04 $ sudo apt upgrade
	|	Ubuntu-20.04 $ sudo dpg --add-architecture i386
	|	Ubuntu-20.04 $ sudo apt update
	|	Ubuntu-20.04 $ sudo apt install marionnet
	|	
	#work in progress
	#
	
	------------------------------------------------------------------

 	$ ln -s ~/.marionnet/kernels/linux-4.10-mod linux
 	$ ln -s ~/.marionnet/filesystems/machine-rootfs.ext4 rootfs.ext4

	# creare un nodo con due dischi virtuali
 	$ dd if=/dev/zero of=myfs.ext4 bs=1 count=1 seek=300M
 	$ ./linux ubd0=root1.cow,rootfs.ext4 ubd1=usr1.cow,myfs.ext4
 	$ lsblk
 	$ blkid
  
	# collegare in rete due nodi h1 e h2 tramite switch s1
 	(s1) $ vde_switch -s s1 -M `pwd`/s1_term -d
 	(s1) $ vdeterm s1_term
 	
 	(h1) $ ./linux ubd0=h1.cow,rootfs.ext4 eth0=vde,s1		[./linux ubd0=h1.cow,rootfs.ext4 eth0=vde,s1,indirizzo mac,numero di porta]
 	
 	(h2) $ ./linux ubd0=h2.cow,rootfs.ext4 eth0=vde,s1
		
 	(s1-vde) $ vde[s1_term]: port/print
 	
 	(h1-uml) # ifconfig eth0 up
 	(h1-uml) # arping -0Bi eth0
 	(h2-uml) # ifconfig eth0 up
 	(h2-uml) # tcpdump -ni eth0
	
	------------------------------------------------------------------
	
	traffic shaping:
	in sede di esame è richiesta la conoscenza di: TBF, HTB e FIFO_FAST.
	[fifo_fast prevede code di priorità che vengono svuotate una alla volta]
	
	note: RANDOM_EARLY_DETECTION riduce la crescita delle code marcando alcuni datagram e simulando una perdita di pacchetti prima che avvenga.
