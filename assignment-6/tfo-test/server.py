import socket
import sys

BUFFER_SIZE = 1024
MSG_FASTOPEN = 0x20000000
TCP_FASTOPEN = 23
tfo = False
message = "GET REQUEST STAND-IN"

if len(sys.argv) < 4:
  sys.exit(0)
elif len(sys.argv) >= 5: 
  if(sys.argv[4] == '1'):
    tfo = True

ip = sys.argv[1]
port = int(sys.argv[2])
served_data = ""
with open(sys.argv[3]) as f:
  served_data = f.read()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip, port))
if tfo:
  s.setsockopt(socket.SOL_TCP, TCP_FASTOPEN, 5)

while 1:
  s.listen(1)
  conn, addr = s.accept()
  print 'Connected To: ', addr
  print conn.recv(len(message))
  conn.send(served_data)
  conn.close()
