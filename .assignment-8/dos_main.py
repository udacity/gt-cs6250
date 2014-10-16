# Udacity
# Computer Networking
# Assignment 8: Applications of SDN
#
# Professor: Nick Feamster
# Teaching Assistant: Ben Jones
#
################################################################################
# Resonance Project                                                            #
# Resonance implemented with Pyretic platform                                  #
# author: Hyojoon Kim (joonk@gatech.edu)                                       #
# author: Nick Feamster (feamster@cc.gatech.edu)                               #
# author: Muhammad Shahbaz (muhammad.shahbaz@gatech.edu)                       #
################################################################################

# import pyretic stuff
from pyretic.lib.corelib import *
from pyretic.lib.std import *

# import pyresonance stuff
from ..drivers.sflow_event import *
from ..globals import *

# import other files from this assignment
from dos_fsm import DDoSFSM
from dos_policy import DDoSPolicy

HOST = 'localhost'
PORT = 8008

def main(queue):
    
    # Create FSM object
    fsm = DDoSFSM()
    
    # Create policy using state machine
    policy = DDoSPolicy(fsm)
    
    # Create an event source (i.e., SFlow)
    sflow_event = SFlowEvent_T(fsm.default_handler, HOST, PORT)
    
    sflow_event.set_max_events(10)
    sflow_event.set_timeout(60)
    
    groups = {'external':['0.0.0.0/0']}
    flows = {'keys':'ipsource,ipdestination','value':'frames'}
    threshold = {'metric':'ddos','value':10}
    message = {'event_type':'ddos', 'message_type':'state', 'message_value':'ddos-attacker', \
               'flow':{'dstip': None, 'protocol': None, 'srcmac': None, 'tos': None, 'vlan_pcp': None, 'dstmac': None, \
               'inport': None, 'ethtype': None, 'srcip': '10.0.0.1', 'dstport': None, 'srcport': None, 'vlan_id': None}}
    
    sflow_event.set_groups(groups)
    sflow_event.set_flows(flows)
    sflow_event.set_threshold(threshold)
    sflow_event.set_action(message)
    
    sflow_event.start(queue)
    
    return fsm, policy
