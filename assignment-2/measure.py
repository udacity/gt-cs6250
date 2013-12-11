#!/usr/bin/python

"Networking Assignment 2"

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import lg, output
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange, custom, quietRun, dumpNetConnections
from mininet.cli import CLI

from time import sleep, time
from multiprocessing import Process
from subprocess import Popen
import argparse

import sys
import os
from util.monitor import monitor_devs_ng

from mntopo import MNTopo

parser = argparse.ArgumentParser(description="Topology bandwith and TCP tests")

parser.add_argument('--dir', '-d',
                    help="Directory to store outputs",
                    default="results")

parser.add_argument('--cli', '-c',
                    action='store_true',
                    help='Run CLI for topology debugging purposes')

parser.add_argument('--time', '-t',
                    dest="time",
                    type=int,
                    help="Duration of the experiment.",
                    default=60)

parser.add_argument('--buffer', '-s',
                    dest="size",
                    type=int,
                    help="Size of buffer.")

# Expt parameters
args = parser.parse_args()

if not os.path.exists(args.dir):
    os.makedirs(args.dir)

lg.setLogLevel('info')

def waitListening(client, server, port):
    "Wait until server is listening on port"
    if not 'telnet' in client.cmd('which telnet'):
        raise Exception('Could not find telnet')
    cmd = ('sh -c "echo A | telnet -e A %s %s"' %
           (server.IP(), port))
    while 'Connected' not in client.cmd(cmd):
        output('waiting for', server,
               'to listen on port', port, '\n')
        sleep(.5)

def progress(t):
       # Begin: Template code
    while t > 0:
        print '  %3d seconds left  \r' % (t)
        t -= 1
        sys.stdout.flush()
        sleep(1)

def start_tcpprobe():
    os.system("rmmod tcp_probe 1>/dev/null 2>&1; modprobe tcp_probe")
    Popen("cat /proc/net/tcpprobe > %s/tcp_probe.txt" % args.dir, shell=True)

def stop_tcpprobe():
    os.system("killall -9 cat; rmmod tcp_probe")

def get_txbytes(iface):
    f = open('/proc/net/dev', 'r')
    lines = f.readlines()
    for line in lines:
        if iface in line:
            break
    f.close()
    if not line:
        raise Exception("could not find iface %s in /proc/net/dev:%s" %
                        (iface, lines))
    return float(line.split()[9])

def get_rates(iface, nsamples=1, period=30,
              wait=10):
    """Returns rate in Mbps"""
    # Returning nsamples requires one extra to start the timer.                                                                                                                 
    nsamples += 1
    last_time = 0
    last_txbytes1 = 0
    last_txbytes2 = 0
    ret = []
    sleep(wait)
    iface1 = 's1-eth1'
    iface2 = 's2-eth1'
    while nsamples:
        nsamples -= 1

        txbytes1 = get_txbytes(iface1)
        txbytes2 = get_txbytes(iface2)
    
        now = time()
        elapsed = now - last_time
 
        last_time = now

        rate1 = (txbytes1 - last_txbytes1) * 8.0 / 1e6 / elapsed
        rate2 = (txbytes2 - last_txbytes2) * 8.0 / 1e6 / elapsed
        if last_txbytes1 != 0:
            ret.append(rate1)
            ret.append(rate2)
            ret.append(rate1+rate2)
        last_txbytes1 = txbytes1
        last_txbytes2 = txbytes2
        sys.stdout.flush()
        sleep(period)
    return ret

def run_topology_experiment(net):
    "Run experiement"

    seconds = args.time

    # Start the bandwidth and cwnd monitors in the background
    monitor = Process(target=monitor_devs_ng, 
            args=('%s/bwm.txt' % args.dir, 1.0))
    monitor.start()
    start_tcpprobe()

    # Get receiver and clients
    recvr = net.getNodeByName('receiver')
    sender = net.getNodeByName('sender')

    s1 = net.getNodeByName('s1')

    # Start the receiver
    port = 5001
    recvr.cmd('iperf -s -p', port,
              '> %s/iperf_server.txt' % args.dir, '&')

    waitListening(sender, recvr, port)

    sender.sendCmd('iperf -c %s -p %s -t %d -i 1 -yc > %s/iperf_%s.txt' %
	    (recvr.IP(), 5001, seconds, args.dir, recvr))

    # Turn off and turn on links
    rates = get_rates(iface='s1-eth1')
    print rates

    sender.waitOutput()

    recvr.cmd('kill %iperf')

    # Shut down monitors
    monitor.terminate()
    stop_tcpprobe()

def check_prereqs():
    "Check for necessary programs"
    prereqs = ['telnet', 'bwm-ng', 'iperf', 'ping']
    for p in prereqs:
        if not quietRun('which ' + p):
            raise Exception((
                'Could not find %s - make sure that it is '
                'installed and in your $PATH') % p)

def main():
    "Create and run experiment"
    start = time()

    topo = MNTopo()

    host = custom(CPULimitedHost, cpu=.15)  # 15% of system bandwidth
    link = custom(TCLink, max_queue_size=200)

    net = Mininet(topo=topo, host=host, link=link)

    net.start()

    print "*** Dumping network connections:"
    dumpNetConnections(net)

    print "*** Testing connectivity"

    net.pingAll()

    if args.cli:
        # Run CLI instead of experiment
        CLI(net)
    else:
        print "*** Running experiment"
        run_topology_experiment(net)

    net.stop()
    end = time()
    os.system("killall -9 bwm-ng")
    print "Experiment took %.3f seconds" % (end - start)

if __name__ == '__main__':
    check_prereqs()
    main()

