#!/usr/bin/python

"Assignment 4 - Creates the topology used for the learning switch \
    assignment. This file needs no changes in order to complete the \
    assignment, however the student may want to change it to test new \
    topologies."

from mininet.topo import Topo
from mininet.net  import Mininet
from mininet.node import CPULimitedHost, RemoteController
from mininet.util import custom
from mininet.link import TCLink
from mininet.cli  import CLI


class LSTopo(Topo):

    def __init__(self, cpu=.1, bw=10, delay=None, **params):
        """ Creates the topology described in assignment 4
            with 5 switches and 7 hosts.
            cpu: system fraction for each host
            bw: link bandwidth in Mb/s
            delay: link delay (e.g. 10ms)"""

        # Initialize topo
        super(LSTopo, self).__init__()

        # Host in link configuration
        hconfig = {'cpu': cpu}
        lconfig = {'bw': bw, 'delay': delay}
        
        # Create all the switches
        sA = self.addSwitch('s1')
        sB = self.addSwitch('s2')
        sC = self.addSwitch('s3')
        sD = self.addSwitch('s4')
        sE = self.addSwitch('s5')

        # Create all the hosts
        h1 = self.addHost('h1', **hconfig)
        h2 = self.addHost('h2', **hconfig)
        h3 = self.addHost('h3', **hconfig)
        h4 = self.addHost('h4', **hconfig)
        h5 = self.addHost('h5', **hconfig)
        h6 = self.addHost('h6', **hconfig)
        h7 = self.addHost('h7', **hconfig)

        # Add links between switches
        self.addLink(sA, sB, port1=1, port2=1, **lconfig)
        self.addLink(sB, sC, port1=3, port2=1, **lconfig)
        self.addLink(sC, sD, port1=2, port2=2, **lconfig)
        self.addLink(sB, sE, port1=2, port2=2, **lconfig)

        # Add links between hosts and switches
        self.addLink(sA, h1, port1=0, port2=0, **lconfig)
        self.addLink(sB, h2, port1=0, port2=0, **lconfig)
        self.addLink(sC, h3, port1=0, port2=0, **lconfig)
        self.addLink(sD, h4, port1=0, port2=0, **lconfig)
        self.addLink(sD, h5, port1=1, port2=0, **lconfig)
        self.addLink(sE, h6, port1=1, port2=0, **lconfig)
        self.addLink(sE, h7, port1=0, port2=0, **lconfig)

def main():
    print "Starting topology"
    topo = LSTopo()
    net = Mininet(topo=topo, link=TCLink, controller=RemoteController, autoSetMacs=True)
    net.start()
    CLI(net)

if __name__ == '__main__':
    main()
