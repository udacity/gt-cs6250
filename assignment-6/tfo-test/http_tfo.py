#!/usr/bin/python

# TFO-enabled server that serves scraped web pages

import socket
import SimpleHTTPServer
import SocketServer
import os
import sys
import time
import posixpath
import hashlib
from argparse import ArgumentParser

parser = ArgumentParser(description="TFO Server")
parser.add_argument('--port', help="Port number",
                    type=int, default=80)
parser.add_argument('--delay', help="Delay (s)",
                    type=float, default="0.0")
parser.add_argument('--fetchlogs', help="Directory with fetch logs",
                    type=str, default="../../Paper.fetchlog")
args = parser.parse_args()

TCP_FASTOPEN = 23
request_dict = {}

fetchlogs = os.listdir(args.fetchlogs)
for fetchlog in fetchlogs:
  with open(args.fetchlogs+'/'+fetchlog) as f:
    data = f.read()
    start_tag = '<responses>'
    end_tag = '</responses>'
    start_index = data.find(start_tag)+len(start_tag)
    end_index = data.find(end_tag)
    if start_index == -1 or end_index == -1:
      print 'Error parsing file: ', fetchlog
    else:
      transactions = data[start_index:end_index]
      for transaction in transactions.split('\n')[2:-1]:
        status, mime, charset, url = [x.strip() for x in transaction.split('|')][0:4]
        url = url.split(' ')[0]
        url = url.replace('http://','')
        #print url
        #print [mime, charset]
        request_dict[url] = [mime, charset]


class TFOServer(SocketServer.TCPServer):
  allow_reuse_address = 1
  def server_bind(self):
    """Override server_bind to set the TFO socket opt."""
    SocketServer.TCPServer.server_bind(self)
    self.socket.setsockopt(socket.SOL_TCP, TCP_FASTOPEN, 5)
  def process_request(self, request, client_address):
    """Override process_request to add delay."""
    time.sleep(args.delay)
    return SocketServer.TCPServer.process_request(self, request, client_address)

class CustomHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
  def send_head(self):
    """Common code for GET and HEAD commands.

    This sends the response code and MIME headers.

    Return value is either a file object (which has to be copied
    to the outputfile by the caller unless the command was HEAD,
    and must be closed by the caller under all circumstances), or
    None, in which case the caller has nothing further to do.

    """
    print self.request
    path = self.translate_path(self.path)
    f = None
    print path
    isdir = False
    if os.path.isdir(path):
      isdir = True
      """for index in "index.html", "index.htm":
        index = os.path.join(path, index)
        if os.path.exists(index):
          path = index
          break
      else:
        return self.list_directory(path)
      """
    ctype = self.guess_type(path)
    if ctype.startswith('text/'):
      mode = 'r'
    else:
      mode = 'rb'
    if isdir:
      dirpath = self.path
      if len(path) and dirpath[-1] == '/':
        dirpath = dirpath[:-1]
      print  os.getcwd() + '/index.html' + dirpath

      path = '/index.html' + dirpath
    else:
      path = self.path
      print path
    do_hash = False
    try:
      f = open(os.getcwd() + path, mode)
    except IOError:
      do_hash = True
   
    # URL was too long, so we may have hashed it?
    if do_hash:
      try:
        if len(path) and (path[-1] == '?' or path[-1] == '#'):
          path = path[:-1]
        print path
        hashed_path = hashlib.md5(path).hexdigest()
        print "trying hash:", hashed_path
        f = open(os.getcwd() + '/' + hashed_path, mode)
      except IOError:
        self.send_error(404, "file not found")
     
    self.send_response(200)
    self.send_header("Content-type", ctype)
    self.end_headers()
    return f
   
  def guess_type(self, path):
    base, ext = posixpath.splitext(path)
    domain = os.getcwd().split('/')[-1]
    key = domain+self.path
    if key not in request_dict:
      return 'text/html'
    else:
      print 'found page in dictionary'
      [mime, encoding] = request_dict[key] 
      
      print "mime:", mime
      print "encoding: ",encoding
      return mime+'; charset='+encoding

handler = CustomHTTPRequestHandler

httpd = TFOServer(("", args.port), handler)
print "HTTP Running :", args.port, " from ", os.getcwd(), " with delay ", args.delay, "s"
sys.stdout.flush()
httpd.serve_forever()
