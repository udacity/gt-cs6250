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

rootdir=buffersizing-$exptid
plotpath=util
iperf=~/iperf-patched/src/iperf

# TODO: change the interface for which queue size is adjusted
# should be <switch-name>-eth3
iface=s1-eth3

for run in 1; do
for flows_per_host in 1 2 5 10 50 100 200 300 400; do
	dir=$rootdir/nf$flows_per_host-r$run

	python buffersizing.py --bw-host 1000 \
		--bw-net 62.5 \
		--delay 43.5 \
		--dir $dir \
		--nflows $flows_per_host \
		--iperf $iperf \
		--iface $iface

	python $plotpath/plot_queue.py -f $dir/qlen_$iface.txt -o $dir/q.png
	python $plotpath/plot_tcpprobe.py -f $dir/tcp_probe.txt -o $dir/cwnd.png --histogram
done
done

cat $rootdir/*/result.txt | sort -n -k 1
cat $rootdir/*/result.txt | sort -n -k 1 > $rootdir/buffer-size-result.txt
python plot-results.py --dir $rootdir -o $rootdir/result.png
echo "Started at" $start
echo "Ended at" `date`
