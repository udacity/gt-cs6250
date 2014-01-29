#!/bin/bash 
IP=`curl http://169.254.169.254/latest/meta-data/public-ipv4`
echo "Use http://$IP:8888/queue.png to see the figure on your browser"
python -m SimpleHTTPServer 8888
