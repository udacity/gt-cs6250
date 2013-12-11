from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import custom

# Topology to be instantiated in Mininet
class MNTopo(Topo):
    "Topo1 Topology"

    def __init__(self, cpu=.1, bw=10, delay=None,
                 max_queue_size=None, **params):

        # Initialize topo
        Topo.__init__(self, **params)

        # Host and link configuration
        hconfig = {'cpu': cpu}
        lconfig_eth = {'bw': 10, 'delay': '1ms', 'loss': 0,
                   'max_queue_size': max_queue_size }
       
	# Hosts and switches
        s1 = self.addSwitch('s1')
	sender = self.addHost('sender', **hconfig)
	receiver = self.addHost('receiver', **hconfig)

	# Wire receiver
        self.addLink(receiver, s1, **lconfig_eth)

	# Wire sender
	self.addLink(sender, s1, **lconfig_eth)


