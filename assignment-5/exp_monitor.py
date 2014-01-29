from monitor import monitor_qlen

from subprocess import Popen, PIPE
from time import sleep, time
from multiprocessing import Process
from argparse import ArgumentParser

import sys
import os

parser = ArgumentParser(description="CWND/Queue Monitor")
parser.add_argument('--exp', '-e', 
                    dest="exp",
                    action="store",
                    help="Name of the Experiment",
                    required=True)
# Expt parameters
args = parser.parse_args()

def start_tcpprobe():
    "Install tcp_pobe module and dump to file"
    os.system("(rmmod tcp_probe >/dev/null 2>&1); modprobe tcp_probe full=1;")
    print "Monitoring TCP CWND ... will save it to ./%s_tcpprobe.txt " % args.exp
    Popen("cat /proc/net/tcpprobe > ./%s_tcpprobe.txt" %
          args.exp, shell=True)

def qmon():
    monitor = Process(target=monitor_qlen,args=('s0-eth2', 0.01, '%s_sw0-qlen.txt' % args.exp ))
    monitor.start()
    print "Monitoring Queue Occupancy ... will save it to %s_sw0-qlen.txt " % args.exp
    raw_input('Press Enter key to stop the monitor--> ')
    monitor.terminate()

if __name__ == '__main__':
    start_tcpprobe()
    qmon()
    Popen("killall -9 cat", shell=True).wait()

