#!/bin/bash 
#qsize=$1
iperf -c 10.0.0.2 -p 5001 -t 3600 -i 1 -w 16m -Z reno > iperf.txt &
echo started iperf

