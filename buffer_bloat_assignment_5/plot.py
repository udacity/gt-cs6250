#!/usr/bin/python

'CS244 Assignment 3: TCP Fast Open -- Plots'

from argparse import ArgumentParser
from collections import namedtuple
import sys
import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np


parser = ArgumentParser(description='TCP Fast Open Plot Generator')
parser.add_argument('--clientdir', help='Client Results Directory', 
                    type=str, default='./client')
parser.add_argument('--outputdir', help='Directory to put Figures',
                    type=str, default='./output-figures')
args = parser.parse_args()

Transaction = namedtuple('Transaction', ['start', 'end', 'length', 'url'])

def autolabel(rects):
  # attach some text labels
  for rect in rects:
    width = rect.get_width()
    plt.text(rect.get_y()+rect.get_height()/2., 1.05*width, '%d'%int(width),
             ha='center', va='bottom')


if __name__ == '__main__':
  directories = os.listdir(args.clientdir)
  results = {}
  print directories
  pages = []
  latencies = []
  for directory in directories:
    run_info = directory.split('-')
    run_info.remove('tfo')
    [latency, run_index, tfo] = [int(x) for x in run_info]
    result_files = os.listdir(args.clientdir+'/'+directory)
    results[(latency, run_index, tfo)] = {}
    if latency not in latencies:
      latencies.append(latency)
    for result_file in result_files:
      results[(latency, run_index, tfo)][result_file] = []
      if not result_file in pages:
        pages.append(result_file)
      with open(args.clientdir+'/'+directory+'/'+result_file) as f:
        data = f.read()
        start_tag = '<transactions>'
        end_tag = '</transactions>'
        start_index = data.find(start_tag)+len(start_tag)
        end_index = data.find(end_tag)
        if start_index == -1 or end_index == -1:
          print 'Error parsing file: ', result_file
        else:
          transactions = data[start_index:end_index]
          for transaction in transactions.split('\n')[2:-1]:
            start, end, length, url = [x.strip() for x in transaction.split('|')][0:4]
            results[(latency, run_index, tfo)][result_file].append(
                Transaction(float(start), float(end), float(length), url))

  print "Generating basic table (like in TFO paper)"
  print "Page\tRTT(ms)\tPLT: no TFO (s)\tPLT: TFO (s)\tImprov."


  for page in pages:
    print page
    
    for latency in latencies:
 
      result_no_tfo = results[(latency, 0, 0)]
      result_tfo = results[(latency, 1, 1)]
      if result_no_tfo and result_tfo:
        if (page in result_no_tfo and len(result_no_tfo[page]) and
            page in result_tfo and len(result_tfo[page])):
          sec_no_tfo = result_no_tfo[page][-1].end
          sec_tfo = result_tfo[page][-1].end
          tfo_len = np.array([result_tfo[page][i].end-result_tfo[page][i].start for i in range(len(result_tfo[page]))])
          tfo_start = np.array([result_tfo[page][i].start for i in range(len(result_tfo[page]))])
          no_tfo_len = np.array([result_no_tfo[page][i].end-result_no_tfo[page][i].start for i in range(len(result_no_tfo[page]))])
          no_tfo_start = np.array([result_no_tfo[page][i].start for i in range(len(result_no_tfo[page]))])
        

          ind = np.arange(min(len(tfo_len), len(no_tfo_len)))  # the x locations for the groups
          height = 1.0       # the width of the bars

          plt.figure()
          plt.subplot(111)
          rects2 = plt.barh(np.arange(len(no_tfo_len)), no_tfo_len, height,
              color='g',
              left=no_tfo_start,
              )

          rects1 = plt.barh(np.arange(len(tfo_len)), tfo_len, height,
              color='r',
              left=tfo_start,
              #align="center"
              )


          # add some
          plt.xlabel('Time (ms)')
          plt.ylabel('Request Index')
          plt.title('TFO Timing Breakdown: %s at %i ms RTT' % (page[4:], latency*2))
          plt.legend( (rects1[0], rects2[0]), ('TFO Enabled', 'TFO Disabled') , loc=4)

          #fig = plt.figure()
          #plt.plot(np.array([result_no_tfo[page][i].end for i in range(len(result_no_tfo[page]))]), 'ro')
          #plt.plot(np.array([result_tfo[page][i].end for i in range(len(result_tfo[page]))]), 'go')
          plt.savefig(args.outputdir + ("/timing-%s-%i.png" % (page[4:], latency*2)))
          print '\t', latency*2,'\t', sec_no_tfo, '\t', sec_tfo,'\t', 100.0*abs(sec_tfo-sec_no_tfo)/sec_no_tfo
  """for (latency, run_index, tfo), site in results.iteritems():
    for url, transactions in site.iteritems():
      if transactions:
        print url, transactions[-1].end
  """
