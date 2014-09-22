#!/usr/bin/python

"Assignment 4 - This is the controller code that students will have to \
    implement sections of. It is Pyretic based, but this is somewhat\
    unimportant at the moment, as we only care about the learning\
    behaviors."

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import packets



# These helper functions are simply macros to simplify your introduction
# to Pyretic.
def get_src_mac(pkt):
    """ Returns the source MAC address of the packet. """
    return pkt['srcmac']

def get_dst_mac(pkt):
    """ Returns the destination MAC address of the packet. """
    return pkt['dstmac']

def get_switch(pkt):
    """ Returns the switch of the packet. """
    return pkt['switch']

def get_inport(pkt):
    """ Returns the port the packet came in on. """
    return pkt['inport']

def get_outport(pkt):
    """ Returns the port the packet came in on. """
    return pkt['outport']


class LearningSwitch(DynamicPolicy):
    def __init__(self):
        """ Initialization of the Learning Switch. The important piece
            is the definition of the switch mapping. This is a nested
            dictionary. """

        # Initialize the parent class
        super(LearningSwitch, self).__init__()

        # initialize the forwarding table to empty.
        # This may need to be updated if a different topology is used.
        self.fwd_table = {}
        self.fwd_table['1'] = {}
        self.fwd_table['2'] = {}
        self.fwd_table['3'] = {}
        self.fwd_table['4'] = {}
        self.fwd_table['5'] = {}

        # only use one flood instance - this is the default policy
        self.flood = flood()

        # get the first packet from each new MAC address on a switch
        new_pkts = packets(1, ['srcmac', 'switch'])
        new_pkts.register_callback(self.learn_route)
        self.query = new_pkts

        # Initialize the policy
        self.push_rules() 


    def print_switch_tables(self):
        for entry in self.fwd_table.keys():
            print "Switch " + str(entry)
            for fwd_rule in self.fwd_table[entry].keys():
                print "   %s : %s" % (str(fwd_rule), 
                                      str(self.fwd_table[entry][fwd_rule]))
        print "----------------"

	# **** Adding the following lines for ease of grading *****

	f = open("output.txt", "w")
	for entry in self.fwd_table.keys():
	    f.write("Switch " + str(entry)+ "\n")
	    for fwd_rule in self.fwd_table[entry].keys():
	         f.write(" %s : %s \n" % (str(fwd_rule),
	                                  str(self.fwd_table[entry][fwd_rule])))
	f.write("---------------- \n")
	f.close()

	# **********************************************

    def learn_route(self, pkt):
        """  This function adds new routes into the fowarding table. """

        # TODO - create a new entry in the fowarding table.
        # Adding a new route should be
        #    self.fwd_table['s1'][mac_addr] = port
        # You must extract the correct pieces from the packet to populate
        # the forwarding table. 


        # print out the switch tables:
        self.print_switch_tables()

        # Call push_rules to update the fowarding tables of the switches.
        self.push_rules()
        pass




    def push_rules(self):
        new_policy = None
        not_flood_pkts = None
        
        for entry in self.fwd_table.keys():
            for fwd_rule in self.fwd_table[entry].keys():
                if new_policy == None:
                    new_policy = (match(switch=int(entry), dstmac=fwd_rule) >> 
                                  fwd(self.fwd_table[entry][fwd_rule]))
                else:
                    new_policy += (match(switch=int(entry), dstmac=fwd_rule) >> 
                                   fwd(self.fwd_table[entry][fwd_rule]))
                
                if not_flood_pkts == None:
                    not_flood_pkts = (match(switch=int(entry), dstmac=fwd_rule))
                else:
                    not_flood_pkts |= (match(switch=int(entry), dstmac=fwd_rule))


        if new_policy == None:
            self.policy = self.flood + self.query
        else:
            self.policy = if_(not_flood_pkts, new_policy, self.flood) + self.query
        
        # The following line can be uncommented to see your policy being
        # built up, say during a flood period. When submitting your completed
        # code, be sure to comment it out!
#        print self.policy


def main():
    return LearningSwitch()
