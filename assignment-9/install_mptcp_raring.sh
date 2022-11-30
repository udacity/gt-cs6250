#!/bin/bash
# Script to install MPTCP kernel from the MPTCP apt-get repo
# Instructions from http://mptcp.info.ucl.ac.be/pmwiki.php?n=Users.AptRepository

# Get key
wget -q -O - http://multipath-tcp.org/mptcp.gpg.key | sudo apt-key add - 
# Add repo
sudo sh -c 'echo "deb http://multipath-tcp.org/repos/apt/debian raring main" > /etc/apt/sources.list.d/mptcp.list'

# Update:
sudo apt-get update

# Install appropriate kernel version; -virtual for EC2.
linux_kernel=linux-mptcp

echo "installing linux kernel: $linux_kernel"
sudo apt-get install $linux_kernel

echo "If *-mptcp is not the first entry, change the default param in /boot/grub/menu.lst to match it (probably 2 or 4, but not odd - those are rescue kernels)."
grep ^default /boot/grub/menu.lst
echo ""

echo "Check to make sure the following entry is in: /boot/grub/menu.lst"
echo "If it is not there, add it to the list and verify 'default'"
echo ""

#title		Ubuntu 12.10, kernel 3.5.0-21-mptcp
echo "title		Ubuntu 13.04, kernel `ls /boot/ | grep -o -m 1 3.5.*mptcp`"
echo "root		(hd0)"
#kernel		`ls /boot/vmlinux*mptcp`/boot/vmlinuz-3.5.0-24-mptcp root=LABEL=cloudimg-rootfs ro console=hvc0 
echo "kernel		`ls /boot/vmlinuz*mptcp` root=LABEL=cloudimg-rootfs ro console=hvc0"
#initrd		/boot/initrd.img-3.5.0-24-mptcp
echo "initrd		`ls /boot/initrd*mptcp`"
echo ""

echo "Then, reboot to enjoy a fresh MPTCP kernel, with 'sudo reboot'."
echo "Once rebooted, verify the kernel version with 'uname -a'."
echo "Enjoy!"
#sudo reboot
