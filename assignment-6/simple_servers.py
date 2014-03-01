#!/usr/bin/python

import subprocess
from subprocess import Popen, PIPE
from time import sleep, time
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

parser = ArgumentParser(description="TCP Fast Open -- simple servers")
parser.add_argument('--delays', help="List of delay to servers (s)",
                    type=list, default=[0.000, 0.050, 0.100, 0.500])
parser.add_argument('--data', help="Directory containing web pages",
                    type=str, default='./Internet')
parser.add_argument("--start_port", help="Port to start serving from",
                    type=int, default=50000)
parser.add_argument("--pages", help="List of pages to fetch.",
                    type=list,
                    default=["http://www.google.com",
                             "http://www.amazon.com",
                             "http://www.nytimes.com",
                             "http://www.wsj.com",
                             "http://en.wikipedia.org/wiki/Tranmission_Control_Protocol"])
args = parser.parse_args()

def sanitize_file(file):
  valid = "-_.() %s%s" % (string.ascii_letters, string.digits)
  return ''.join(c for c in file if c in valid)

def start_servers(delay, port):
  servers = []
  hack_dns = []
  cwd = os.getcwd()
  dirs = os.listdir(args.data)
  cprint("  Starting " + str(len(dirs)) +
         " servers at port " + str(port), "green")
  for directory, idx in zip(dirs, range(len(dirs))):
    hack_dns.append(directory + " 127.0.0.1 " + str(port))
    outdir = "./serverlogs/" + str(delay) + "/"
    if not os.path.exists(outdir):
      os.makedirs(outdir)
    outfile = open(outdir + sanitize_file(directory), "w+")
    dir = cwd + '/Internet/' + directory
    # Run Python without buffering.
    servers.append(
        subprocess.Popen('python -u ' +
                         cwd + '/tfo-test/http_tfo.py' +
                         ' --host=localhost' +
                         ' --port=' + str(port) +
                         ' --delay=' + str(delay),
                         shell=True,
                         cwd=dir,
                         stderr=subprocess.STDOUT,
                         stdout=outfile,
                         # Create process group because of shell.
                         preexec_fn=os.setsid))
    port = port + 1

  with open("hack_dns", "w+") as f:
    for line in hack_dns:
      f.write(line + "\n")
      
  return servers

def fetch(delay, page):
  dir = "./client/" + str(delay) + "/"
  if not os.path.exists(dir):
    os.makedirs(dir)
  outfile = open(dir + sanitize_file(page), "w+")
  command = ("DISPLAY=:1 " +
             os.getcwd() + "/test_shell "
             "--stats " +
             "--hack_dns=" + os.getcwd() + "/hack_dns " +
             page)
  start = time.time()
  proc = subprocess.Popen(
      command,
      stderr=subprocess.STDOUT,
      stdout=outfile,
      shell=True, cwd=dir)
  proc.wait()
  end = time.time()
  #assert(proc.returncode == 0)
  return end - start

if __name__ == '__main__':
  start_port = args.start_port
  for delay in args.delays:
    cprint("Simulating with " + str(delay) + "s of delay.", "green")
    servers = []
    try:
      servers = start_servers(delay, start_port)
      cprint("Started " + str(len(servers)) + " servers.", "green")
      for page in args.pages:
        t = fetch(delay, page)
        cprint("  Fetching " + page + " took " + str(t) + "s.",
               "blue")
    finally:
      # Kill all the process groups (shell and subprocesses).
      [os.killpg(server.pid, signal.SIGTERM) for server in servers]
