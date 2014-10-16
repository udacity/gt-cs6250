#!/bin/bash

sysctl 'net.mptcp.mptcp_enabled=1'

./mptcp.sh topo_measure.py 05 512000 > 05.txt

sysctl 'net.mptcp.mptcp_enabled=0'

./mptcp.sh topo_wifi.py 05 512000 > 05_tcp_wifi.txt

./mptcp.sh topo_measure.py 05 512000 > 05_tcp_3g.txt

sysctl 'net.mptcp.mptcp_enabled=1'
