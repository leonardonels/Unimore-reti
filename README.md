	# UNIMORE-reti
	
		#nano /etc/network/interfaces
		#vale per nodi statici o per il dhcp_server nel caso di reti dhcp
	auto eth0
	iface eth0 inet static
		address 192.168.1.1/24
		gateway 192.168.1.254
		post-up ip route add 192.168.2.0/24 via 192.168.1.254
		post-up ip route add 1.1.1.1/32 dev eth0
		
		#vale per nodi di una rete dhcp
	auto eth0
	iface eth0 inet dhcp
		hwaddress ethers 02:04:06:11:22:33	#necessario solo se si vuole dedicare un indirizzo ip alla macchina con questo indirizzo MAC
		
	#nano /etc/dnsmaq.conf
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
