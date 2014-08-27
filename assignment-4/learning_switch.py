#!/usr/bin/python

"Assignment 4 - This is the controller code that students will have to \
    implement sections of. It is Pyretic based, but this is somewhat\
    unimportant at the moment, as we only care about the learning\
    behaviors."

from pyretic.lib.corelib import *
from pyretic.lib.std import *



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
        
        # initialize the forwarding table to empty
        self.fwd_table['s1'] = {}
        self.fwd_table['s2'] = {}
        self.fwd_table['s3'] = {}
        self.fwd_table['s4'] = {}
        self.fwd_table['s5'] = {}

        # only use one flood instance - this is the default policy
        self.flood = flood()

        # get the first packet from each new MAC address on a switch
        new_pkts = packets(1, ['srcmac', 'switch'])
        self.query = new_pkts

        # Initialize the policy
        self.push_rules() 


    def print_switch_tables(self):
        for entry in fwd_table.keys():
            print "Switch " + str(entry)
            for fwd_rule in fwd_table[entry].keys():
                print "   %s : %s" % (str(fwd_rule), 
                                      str(fwd_table[entry][fwd_rule]))


    def learn_route(self, pkt):
        """  This function adds new routes into the fowarding table. """

        # TODO - create a new entry in the fowarding table.
        # Adding a new route should be
        #    self.fwd_table['s1'][mac_addr] = port
        # You must extract the correct pieces from the packet to populate
        # the forwarding table. 



        # Call push_rules to update the fowarding tables of the switches.
        self.push_rules
        pass




    def push_rules(self):
        new_policy = None
        
        for entry in fwd_table.keys():
            for fwd_rule in fwd_table[entry].keys():
                if new_policy = None:
                    new_policy = (match(switch=entry, srcport=fwd_rule) >> 
                                  fwd(fwd_table[entry][fwd_rule]))
                else:
                    new_policy += (match(switch=entry, srcport=fwd_rule) >> 
                                   fwd(fwd_table[entry][fwd_rule]))
        if new_policy = None:
            self.policy = self.flood + self.query
        else:
            self.policy = new_policy >> self.flood + self.query
        

        pass


