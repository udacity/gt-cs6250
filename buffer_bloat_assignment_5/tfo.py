#!/usr/bin/python

"CS244 Assignment 3: TCP Fast Open -- Experiments"

from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import lg
from mininet.util import dumpNodeConnections
from mininet.cli import CLI

import subprocess
from subprocess import Popen, PIPE
from multiprocessing import Process
import termcolor as T
from argparse import ArgumentParser

import sys
import os
import time
import signal
import string

def cprint(s, color, cr=True):
    if cr:
        print T.colored(s, color)
    else:
        print T.colored(s, color),

def kill_proc(proc):
  Popen(("ps -ef | grep %s | grep '^root' | grep -v python | "
         + "sed -s 's/  */ /g' | "
         + "cut -f2 -d' ' | xargs kill -9 2> /dev/null") % proc,
        shell=True).wait()


parser = ArgumentParser(description="TCP Fast Open")
parser.add_argument('--bwhome', help="Home network bandwidth (Mb/s)",
                    type=float, default=1000)
parser.add_argument('--delayhome', help="Home network delay (ms)",
                    type=int, default=1)
parser.add_argument('--bwnet', help="Internet bandwidth (Mb/s)",
                    type=float, default=4) # Experiment is 4Mbps/256Kbps.
parser.add_argument('--delaynet', help="Internet delays to test (ms)",
                    type=int, default=10)
parser.add_argument('--name',
                    help=("Name for the Webpages/ directory, " +
                          "and the associated Webpages.pages and " +
                          "Webpages.fetchlog files."),
                    type=str)
parser.add_argument('--port', help="Default server port.",
                    type=int, default=8000)
parser.add_argument('--tfo', help="Enable TFO.",
                    type=int, default=0)
parser.add_argument('--testruns', help="Number of test runs.",
                    type=int, default=2)
args = parser.parse_args()

lg.setLogLevel('info')

 
def sanitize_file(file):
  "Turn a URL into a valid filename."
  valid = "-_.() %s%s" % (string.ascii_letters, string.digits)
  return ''.join(c for c in file if c in valid)


class StarTopo(Topo):
  "Star topology for TCP Fast Open experiment"

  def __init__(self):
    super(StarTopo, self ).__init__()

  def create_topology(self):
    user = self.addHost('user')
    directories = os.listdir(args.name)
    servers = []
    index = 0
    for directory in directories:
      server = self.addHost('server' + str(index))
      servers.append([directory, server])
      index += 1
    home_switch = self.addSwitch('s0')
    self.addLink(user, home_switch,
                   bw=args.bwhome,
                   delay=str(args.delayhome) + 'ms', use_htb=True)
    # Assumes args.name directory _only_ has directories in it.
    for name, server in servers:
      self.addLink(server, home_switch,
                   bw=args.bwnet,
                   delay=str(args.delaynet) + 'ms', use_htb=True)
    return servers

def start_servers(net, servers):
  time.sleep(2) # Give Mininet some time to start everything.
  hack_dns = []
  cwd = os.getcwd()
  cprint("Starting " + str(len(servers)) + " servers...",
         "green")
  for hostname, server_name in servers:
    server = net.getNodeByName(server_name)
    outdir = (cwd + "/serverlogs/" +
              str(args.delaynet) + "-" +
              "tfo-" + str(args.tfo) + "/")
    if not os.path.exists(outdir):
      os.makedirs(outdir)
    outfile = open(outdir + sanitize_file(hostname), "w+")
    dir = cwd + '/' + args.name + '/' + hostname
    server.popen('cd ' + dir, shell=True).wait()
    # Run Python without buffering.
    server.popen('python -u ' + cwd + '/tfo-test/http_tfo.py ' +
                 '--port=' + str(args.port),
                 shell=True,
                 stderr=subprocess.STDOUT,
                 cwd=dir,
                 stdout=outfile)
    hack_dns.append(hostname + " " + server.IP() +
                    " " + str(args.port))

  # Write out the hack DNS file that the Chrome shell (the client)
  # will use to remap its requests to the servers we started above.
  # Format is: 'hostname' space 'ip' space 'port' newline.
  with open("hack_dns", "w+") as f:
    for line in hack_dns:
      f.write(line + "\n")

def run(topo, net, page, testrun, delay):
  cwd = os.getcwd()
  dir = (cwd + "/client/" +
         str(args.delaynet) + "-" + str(testrun) +
         "-tfo-" + str(args.tfo) + "/")
  if not os.path.exists(dir):
    os.makedirs(dir)
  outfile = open(dir + sanitize_file(page), "w+")
  command_tfo = ""
  if args.tfo:
    command_tfo = "--enable-tcp-fastopen=1"
  command = (cwd + "/test_shell "
             " --stats --savefiles " +
             command_tfo +
             " --hack_dns=" + cwd + "/hack_dns " +
             page)
  client = net.getNodeByName("user")
  # This is an informative measurement but includes the shell's
  # start time, so it shouldn't be used as the actual benchmark.
  # The Chrome shell outputs more accurate results in its log file.
  # Python's timer also isn't quite accurate on some platforms.
  start = time.time()
  client.popen(
      command,
      stderr=subprocess.STDOUT,
      stdout=outfile,
      shell=True, cwd=dir).wait()
  end = time.time()
  cprint((("  Fetching %s took %6.3fs.") %
          (page, end - start)), "green")

if __name__ == '__main__':
  net = None
  try:
    start = time.time()
    topo = StarTopo()
    servers = topo.create_topology()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    dumpNodeConnections(net.hosts)

    start_servers(net, servers)
    time.sleep(2) # Let the servers start properly.
    #CLI(net)
    pages = []
    with open(args.name + '.pages', 'r') as namefile:
        pages = namefile.readlines()
    pages = [p.strip() for p in pages if len(p.strip()) != 0]

    for testrun in range(args.testruns):
      for page in pages:
        cprint(("Experiment %s %s @ %sms delay" %
                (testrun, page, args.delaynet)), "blue")
        # Make sure the Chrome shell doesn't server from cache.
        with open('/dev/null', 'w+') as null:
          Popen("rm -r ./cache",
                shell=True, stdout=null, stderr=null).wait()
          run(topo, net, page, testrun, args.delaynet)
          Popen("rm -r ./cache",
                shell=True, stdout=null, stderr=null).wait()

    cprint("Experiment done", "green")
  finally:
    cprint("Cleaning up", "red")
    sys.stdout.flush()
    if net: net.stop()
    [kill_proc(proc) for proc in ["ping", "bwm-ng", "tcpprobe",
                                  "simhost", "wget", "test_shell"]]
  cprint("Done", "green")
