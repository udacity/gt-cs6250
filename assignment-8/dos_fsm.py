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

from pyretic.lib.corelib import *
from pyretic.lib.std import *

from ..FSMs.base_fsm import *
from ..drivers.sflow_event import *

from ..globals import *

HOST = 'localhost'
PORT = 8008

class DDoSFSM(BaseFSM):
    
    def default_handler(self, message, queue):
        print message
        return_value = 'ok'
        
        if DEBUG == True:
            print "DDoS handler: ", message['flow']
            
        if message['event_type'] == EVENT_TYPES['ddos']:
            if message['message_type'] == MESSAGE_TYPES['state']:
                self.state_transition(message['message_value'], message['flow'], queue)
            elif message['message_type'] == MESSAGE_TYPES['info']:
                pass
            else: 
                return_value = self.debug_handler(message, queue)
        else:
            print "DDoS: ignoring message type."
            
        return return_value
