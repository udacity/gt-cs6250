#!/bin/bash

if [ $# -ne 1 ]
then
    echo "Usage: `basename $0` {experiment_name}"
exit
fi

exp=$1
IP=`curl http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null`
python plot_queue.py --maxy 20 --miny 0 -f ${exp}_sw0-qlen.txt -o ${exp}_queue.png >/dev/null
python plot_tcpprobe.py -f ${exp}_tcpprobe.txt -o ${exp}_tcp_cwnd_iperf.png -p 5001 >/dev/null
python plot_tcpprobe.py -f ${exp}_tcpprobe.txt -o ${exp}_tcp_cwnd_wget.png -p 80 --sport >/dev/null

echo "Use http://$IP:8888/ to see the figures on your browser"
echo "Figure Names"
echo "Queue : ${exp}_queue.png"
echo "IPERF CWND : ${exp}_tcp_cwnd_iperf.png"
echo "WGET CWND : ${exp}_tcp_cwnd_wget.png"

rm -f index.html
touch index.html
echo "<html><head><title>FIGURES</title></head>" > index.html
echo "<body><cetner><table border=\"1\">" >> index.html
echo "<tr><th>Switch Queue Occupancy</th></tr>" >> index.html
echo "<tr><td><a href=\"${exp}_queue.png\"><img src=\"${exp}_queue.png\"/></a></td></tr>" >> index.html
echo "<tr><th>TCP CWND for iperf</th></tr>" >> index.html
echo "<tr><td><a href=\"${exp}_tcp_cwnd_iperf.png\"><img src=\"${exp}_tcp_cwnd_iperf.png\"/></a></td></tr>" >> index.html
echo "<tr><th>TCP CWND for wget</th></tr>" >> index.html
echo "<tr><td><a href=\"${exp}_tcp_cwnd_wget.png\"><img src=\"${exp}_tcp_cwnd_wget.png\"/></a></td></tr>" >> index.html
echo "</table></center></body></html>" >> index.html

#sudo pkill -9 -f SimpleHTTPServer
python -m SimpleHTTPServer 8000
