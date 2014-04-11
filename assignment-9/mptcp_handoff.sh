#!/bin/bash

sysctl 'net.mptcp.mptcp_enabled=1'

python topo_wireless_handoff.py -b 10 -n 10 -t 80

sysctl 'net.mptcp.mptcp_enabled=0'
