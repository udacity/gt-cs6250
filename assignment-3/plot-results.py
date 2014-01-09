#!/usr/bin/env python
from util.helper import *
import glob
import sys
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--out',
                    help="Save plot to output file, e.g.: --out plot.png",
                    dest="out",
                    default=None)

parser.add_argument('--dir',
                    dest="dir",
                    help="Directory from which outputs of the sweep are read.",
                    required=True)

args = parser.parse_args()
data = defaultdict(list)
nedata = defaultdict(list)
RTT = 85.0 # ms
BW = 62.5 # Mbps
nruns = 10 # Number of runs for your experiment
nflows = 800
nfiles = 0

def first(lst):
    return map(lambda e: e[0], lst)

def second(lst):
    return map(lambda e: e[1], lst)

def avg(lst):
    return sum(lst)/len(lst)

def median(lst):
    l = len(lst)
    lst.sort()
    return lst[l/2]

def parse_data(filename):
    lines = open(filename).read().split("\n")
    for l in lines:
        if l.strip() == "":
            continue
        x, pkt, byte = map(float, l.split(' '))
        data[int(x)].append(byte/1024.0)
    return

def parse_nedata2(filename):
    lines = open(filename).read().split("\n")
    for l in lines:
        if l.strip() == "":
            continue
        values = map(int, l.split(' '))
        x, y = values[0], values[1]
        nedata[x].append(y / 1024.0)
    return

for f in glob.glob("%s/*/result.txt" % args.dir):
    print "Parsing %s" % f
    parse_data(f)
    nfiles += 1

if nfiles == 0:
    print "Result files not found.   Did you pass the directory correctly?"
    sys.exit(0)

plot_quido = []
plot_bdp = []
plot_data = []
for n in sorted(data.keys()):
    bdp = (RTT * 1000 * BW / 8.0 / 1024.0)
    quido =  bdp / math.sqrt(n)
    plot_quido.append((n, quido))
    plot_bdp.append((n, bdp))

plt.plot(first(plot_quido), second(plot_quido), lw=2, label="RTT*C/$\sqrt{n}$")

# Should you want the BDP plot
plt.plot(first(plot_bdp), second(plot_bdp), lw=2, label="RTT*C")

# Plot results from Neda's experiment
parse_nedata2('nedata2.txt')
median_yneda = []
keys = list(sorted(nedata.keys()))
for k in keys:
    median_yneda.append(median(nedata[k]))
plt.plot(keys, median_yneda, lw=2, label="Hardware-Median",
         color="black", ls='--', marker='d', markersize=10)


keys = list(sorted(data.keys()))

for i in xrange(nruns):
    try:
        values = [mndata[k][i] for k in keys]
    except:
        break

    if i == 0:
        label = "Mininet"
    else:
        label = ''
    plt.plot(keys, values,
             lw=1, label=label, color="red")

avg_mn = []
for k in keys:
    avg_mn.append(avg(data[k]))

plt.plot(keys, avg_mn, lw=2, label="Mininet", color="red", marker='s', markersize=10)

#plt.xscale('log')
#plt.yscale('log')

plt.xlim((0, nflows))
plt.legend()
plt.ylabel("Queue size (KB)")
plt.xlabel("Total #flows")

if args.out:
    print "Saving to %s" % args.out
    plt.savefig(args.out)
else:
    plt.show()
