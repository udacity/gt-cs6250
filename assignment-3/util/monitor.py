from time import sleep, time
from subprocess import *
import re

default_dir = '.'

def monitor_qlen(iface, interval_sec = 0.01, fname='%s/qlen.txt' % default_dir):
    pat_queued = re.compile(r'backlog\s[^\s]+\s([\d]+)p')
    cmd = "tc -s qdisc show dev %s" % (iface)
    ret = []
    open(fname, 'w').write('')
    while 1:
        p = Popen(cmd, shell=True, stdout=PIPE)
        output = p.stdout.read()
        # Not quite right, but will do for now
        matches = pat_queued.findall(output)
        if matches and len(matches) > 1:
            ret.append(matches[1])
            t = "%f" % time()
            open(fname, 'a').write(t + ',' + matches[1] + '\n')
        sleep(interval_sec)
    #open('qlen.txt', 'w').write('\n'.join(ret))
    return

def monitor_count(ipt_args="--src 10.0.0.0/8",
                  interval_sec=0.01, fname='%s/bytes_sent.txt'
                  % default_dir, chain="OUTPUT"):
    cmd = "iptables -I %(chain)s 1 %(filter)s -j RETURN" % {
        "filter": ipt_args,
        "chain": chain,
        }
    # We always erase the first rule; will fix this later
    Popen("iptables -D %s 1" % chain, shell=True).wait()
    # Add our rule
    Popen(cmd, shell=True).wait()
    open(fname, 'w').write('')
    cmd = "iptables -vnL %s 1 -Z" % (chain)
    while 1:
        p = Popen(cmd, shell=True, stdout=PIPE)
        output = p.stdout.read().strip()
        values = output.split(' ')
        if len(values) > 2:
            t = "%f" % time()
            pkts, bytes = values[0], values[1]
            open(fname, 'a').write(','.join([t, pkts, bytes]) + '\n')
        sleep(interval_sec)
    return

def monitor_devs(dev_pattern='^s', fname="%s/bytes_sent.txt" %
                 default_dir, interval_sec=0.01):

    """Aggregates (sums) all txed bytes and rate (in Mbps) from
       devices whose name matches @dev_pattern and writes to @fname"""
    pat = re.compile(dev_pattern)
    spaces = re.compile('\s+')
    open(fname, 'w').write('')
    prev_tx = {}
    while 1:
        lines = open('/proc/net/dev').read().split('\n')
        t = str(time())
        total = 0
        for line in lines:
            line = spaces.split(line.strip())
            iface = line[0]
            if pat.match(iface) and len(line) > 9:
                tx_bytes = int(line[9])
                total += tx_bytes - prev_tx.get(iface, tx_bytes)
                prev_tx[iface] = tx_bytes
        open(fname, 'a').write(','.join([t,
             str(total * 8 / interval_sec / 1e6), str(total)]) + "\n")
        sleep(interval_sec)
    return

def monitor_devs_ng(fname="%s/txrate.txt" % default_dir, interval_sec=0.01):
    """Uses bwm-ng tool to collect iface tx rate stats.  Very reliable."""
    cmd = ("sleep 1; bwm-ng -t %s -o csv "
           "-u bits -T rate -C ',' > %s" %
           (interval_sec * 1000, fname))
    Popen(cmd, shell=True).wait()

def monitor_cpu(fname="%s/cpu.txt" % default_dir):
    cmd = "(top -b -p 1 -d 1 | grep --line-buffered \"^Cpu\") > %s" % fname
    # BL: Disabling until we reinstantiate attachment using setns.
    #if container is not None:
    #    cmd = ("(top -b -p 1 -d 1 | "
    #           "grep --line-buffered \\\"^Cpu\\\") > %s" % fname)
    #    cmd = "lxc-execute -n %s -- bash -c \"%s\"" % (container, cmd)
    Popen(cmd, shell=True).wait()
