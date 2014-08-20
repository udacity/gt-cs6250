'''
Udacity: ud436/sdn-firewall
Professor: Nick Feamster
'''

################################################################################
# The Pyretic Project                                                          #
# frenetic-lang.org/pyretic                                                    #
# author: Joshua Reich (jreich@cs.princeton.edu)                               #
################################################################################
# Licensed to the Pyretic Project by one or more contributors. See the         #
# NOTICES file distributed with this work for additional information           #
# regarding copyright and ownership. The Pyretic Project licenses this         #
# file to you under the following license.                                     #
#                                                                              #
# Redistribution and use in source and binary forms, with or without           #
# modification, are permitted provided the following conditions are met:       #
# - Redistributions of source code must retain the above copyright             #
#   notice, this list of conditions and the following disclaimer.              #
# - Redistributions in binary form must reproduce the above copyright          #
#   notice, this list of conditions and the following disclaimer in            #
#   the documentation or other materials provided with the distribution.       #
# - The names of the copyright holds and contributors may not be used to       #
#   endorse or promote products derived from this work without specific        #
#   prior written permission.                                                  #
#                                                                              #
# Unless required by applicable law or agreed to in writing, software          #
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT    #
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the     #
# LICENSE file distributed with this work for specific language governing      #
# permissions and limitations under the License.                               #
################################################################################

from pyretic.lib.corelib import *
from pyretic.lib.std import *

# insert the name of the module and policy you want to import
from pyretic.examples.pyretic_switch import ActLikeSwitch
from csv import DictReader
from collections import namedtuple
import os

policy_file = "%s/pyretic/pyretic/examples/firewall-policies.csv" % os.environ[ 'HOME' ]
Policy = namedtuple('Policy', ('mac_0', 'mac_1'))

def main():
    # Read in the policies from the firewall-policies.csv file
    def read_policies (file):
        with open(file, 'r') as f:
            reader = DictReader(f, delimiter = ",")
            policies = {}
            for row in reader:
                policies[row['id']] = Policy(MAC(row['mac_0']), MAC(row['mac_1']))
        return policies

    policies = read_policies(policy_file)

    # start with a policy that doesn't match any packets
    not_allowed = none

    # TODO and add traffic that isn't allowed
    # Note: this uses the same policy named tuple from the POX
    # firewall code. Please refer there for further info. HINT - You could use '|' in place of  '+' as well.
    for policy in policies.itervalues():
        not_allowed = not_allowed + ( <traffic going in one direction> ) + ( <traffic going in the other direction> )

    # TODO express allowed traffic in terms of not_allowed - hint use '~'
    allowed = <...>

    # and only send allowed traffic to the mac learning (act_like_switch) logic
    return allowed >> ActLikeSwitch()



