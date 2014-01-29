#!/bin/bash
echo "start cs144 buffer bloat experiment"
sudo sysctl -w net.ipv4.tcp_congestion_control=reno
python bufferbloat.py --bw-host 1000 \
                --bw-net 1.5 \
                --delay 10 \
                --dir ./ \
                --nflows 1 \
                --maxq 20 \
                -n 2 \

echo "cleaning up..."
killall -9 iperf ping
mn -c > /dev/null 2>&1
echo "end"
