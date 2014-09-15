#!/bin/bash

# Exit on any failure
set -e

# Check for uninitialized variables
set -o nounset

ctrlc() {
	killall -9 python
	mn -c
	exit
}

trap ctrlc SIGINT

start=`date`
exptid=`date +%b%d-%H:%M`
rootdir=topology-$exptid

# Note: you need to make sure you report the results
# for the correct port!
# In this example, we are assuming that each
# client is connected to port 2 on its switch.

for n in 1; do
    dir=$rootdir
    python measure.py \
        --dir $dir 
    python util/plot_rate.py \
        --xlabel 'Time (s)' \
        --ylabel 'Rate (Mbps)' \
        -i 's.*-eth1' \
        -f $dir/bwm.txt \
        -o $dir/rate.png
    python util/plot_tcpprobe.py \
        -f $dir/tcp_probe.txt \
        -o $dir/cwnd.png
done

echo "Started at" $start
echo "Ended at" `date`
echo "Output saved to $rootdir"
