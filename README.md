 # UNIMORE-reti

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
  
  (h1) $ ./linux ubd0=h1.cow,rootfs.ext4 eth0=vde,s1
  
  (h2) $ ./linux ubd0=h2.cow,rootfs.ext4 eth0=vde,s1

  (s1-vde) $ vde[s1_term]: port/print
  
  (h1-uml) # ifconfig eth0 up
  (h1-uml) # arping -0Bi eth0
  (h2-uml) # ifconfig eth0 up
  (h2-uml) # tcpdump -ni eth0
