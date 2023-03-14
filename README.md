	# UNIMORE-reti
	
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
	
	auto eth0
	iface eth0 inet static
		address 192.168.1.1

 	$ ln -s ~/.marionnet/kernels/linux-4.10-mod linux
 	$ ln -s ~/.marionnet/filesystems/machine-rootfs.ext4 rootfs.ext4
	
	$ ip addr add dev eth0 192.168.1.1
	$ ip addr show dev eth0
	$ ip link set dev eth0 up [down]
	$ ip link show

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
