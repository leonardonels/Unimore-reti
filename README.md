	# UNIMORE-reti
	
		#nano /etc/network/interfaces
		#vale per nodi statici o per il dhcp_server nel caso di reti dhcp
	auto eth0
	iface eth0 inet static
		address 192.168.1.1/24
		gateway 192.168.1.254
		post-up ip route add 192.168.2.0/24 via 192.168.1.254
		post-up ip route add 1.1.1.1/32 dev eth0
		post-up ip route add -host 1.1.1.1/32 dev eth0		#cavo cross router-router
			#Ext deve limitare il traffico in uscita (ad esempio file disponibili su Ext e scaricati da qualunque altra macchina) a una bandwidth massima di 10MBit/s.
		post-up tc qdisc add dev eth0 root tbf rate 10Mbit latency 50ms burst 1539		#traffic shaping


		#vale per nodi di una rete dhcp
	auto eth0
	iface eth0 inet dhcp
		hwaddress 02:04:06:11:22:33	#necessario solo se si vuole dedicare un indirizzo ip alla macchina con questo indirizzo MAC
		
	#nano /etc/dnsmasq.conf
		# don't look for other nameservers
	no-resolv
		# read /etc/ethers file
	read-ethers
		# network interface for DHCP
	interface=eth0
		# network domain name
	domain=reti.org
		#3 per default gateway; 6 per dns server
	dhcp-option=3,192.168.1.254
	dhcp-option=6,192.168.1.254
		# or...
		# dhcp-option=option:router,192.168.1.254
		# dhcp-option=option:dns-server,192.168.1.254
		#range di indirizzi da assegnare, l'ultimo parametro indica il lease time (tempo durante il quale il dhcp server riserva un indirizzo assegnato)
		#il range e' mevessario affinche' il parametro dhcp-host venga preso in consideazione
	dhcp-range=192.168.1.10,192.168.1.15,1h
		#per assegnare un range di indirizzi utilizzati solo dalle macchine specificate tramite dhcp-host
	dhcp-range=192.168.1.0,static
		#utile ad assegnare un indirizzo specifico ad un determinato host
	dhcp-host=02:04:06:11:22:33,client3,192.168.1.3,1h
		# override address (can also use /etc/hosts)
	address=/www.hackerz.com/192.168.1.1
	
	#usare solo hosts e ethers e' deletereo poiche' le macchine vengono vincolate ad indirizzi non riservati
	#nano /etc/hosts
	192.168.1.254 server server.reti.org
	192.168.1.3 client3 client3.reti.org
	
	#nano /etc/ethers
	02:04:06:11:22:33 192.168.1.3
	
		#per abilitare il dhcp server all'avvio
	systemctl enable dnsmasq
		#per avviare il dhcp server
	service dnsmasq start
		
		#nano /etc/sysctl.conf
		#uncomment la riga seguente
	sysctl net.ipv4.ip_forward
		
		#per applicare la modifica
	sysctl -p /etc/sysctl.conf		
	------------------------------------------------------------------
	
		#iptables
	iptables -t filter -P INPUT DROP
	iptables -t filter -P OUTPUT DROP
	iptables -t filter -P FORWARD DROP
	
		#DHCP
	iptables -t filter -A INPUT -i eth0.10 -p udp --dport 67 --sport 68 -j ACCEPT
	iptables -t filter -A OUTPUT -o eth0.10 -p udp --sport 67 --dport 68 -j ACCEPT
	
		#DNS LAN
	iptables -t filter -A INPUT -i eth0.10 -p udp --dport 53 -j ACCEPT
	iptables -t filter -A OUTPUT -o eth0.10 -p udp --sport 53 -j ACCEPT
	
		#DNS DMZ
	iptables -t filter -A INPUT -i eth0.20 -p udp --dport 53 -j ACCEPT
	iptables -t filter -A OUTPUT -o eth0.20 -p udp --sport 53 -j ACCEPT
	
		#SERVER WEB EXT (con due vlan: .10 e .20)
	iptables -t filter -A FORWARD -i eth0.10 -o eth1 -p tcp --dport www -s 10.0.1.0/25 -d {IP internet} -m state --state NEW,ESTABLISHED -j ACCEPT
	iptables -t filter -A FORWARD -o eth0.10 -i eth1 -p tcp --sport www -d 10.0.1.0/25 -s {IP internet} -m state --state ESTABLISHED -j ACCEPT
	
	iptables -t filter -A FORWARD -i eth0.20 -o eth1 -p tcp --dport www -s 10.0.1.128/25 -d {IP internet} -m state --state NEW,ESTABLISHED -j ACCEPT
	iptables -t filter -A FORWARD -o eth0.20 -i eth1 -p tcp --sport www -d 10.0.1.128/25 -s {IP internet} -m state --state ESTABLISHED -j ACCEPT
	
		#EXT POSSA CONTATTARE SRV (internet possa conattare il server della DMZ)
	iptables -t filter -A FORWARD -i eth1 -o eth0.20 -p tcp --dport www -s {IP internet} -d {IP Srv - nella dmz} -m state --state NEW,ESTABLISHED -j ACCEPT
	iptables -t filter -A FORWARD -o eth1 -i eth0.20 -p tcp --sport www -d {IP internet} -s {IP Srv - nella dmz} -m state --state ESTABLISHED -j ACCEPT
	
		#SSH H1
	iptables -t filter -A INPUT -i eth0.10 -p tcp --dport ssh -s {IP H1} -m state --state NEW,ESTABLISHED -j ACCEPT
	iptables -t filter -A OUTPUT -i eth0.10 -p tcp --sport ssh -d {IP H1} -m state --state ESTABLISHED -j ACCEPT

	------------------------------------------------------------------
	
		#REGOLE DI NAT [10.0.1.129 corrisponde al server nella dmz]
	iptables -t nat -A POSTROUTING -p tcp --dport www -s 10.0.1.0/24 -o eth1 -j MASQUERADE
	iptables -t nat -A PREROUTING -i eth1 -p tcp --dport www -j DNAT --to-destination 10.0.1.129

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
