#!/usr/bin/python

"Networking Assignment 2 Latency Script"

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

from mntopo import MNTopo

def latencyTest():
    "Create network and run latency test"
    topo = MNTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    #print "Testing network latency"

    # Get hosts
    sender = net.get('sender')
    receiver = net.get('receiver') 

    result = sender.cmd('ping -c 5 ', receiver.IP())

    print result

    #net.pingAll()
    net.stop()

if __name__ == '__main__':
    setLogLevel('output')
    latencyTest()
