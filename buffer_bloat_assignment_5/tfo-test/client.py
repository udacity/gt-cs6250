import socket
import sys
import array
BUFFER_SIZE = 1024
MSG_FASTOPEN = 0x20000000
TCP_FASTOPEN = 23
tfo = False

if len(sys.argv) < 3:
  sys.exit(0)
elif len(sys.argv) >= 4: 
  if(sys.argv[3] == '1'):
    tfo = True

ip = sys.argv[1]
port = int(sys.argv[2])
message = "GET / HTTP/1.0\n\n"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if tfo == False:
  s.connect((ip, port))
  s.send(message)
else:
  s.sendto(message, MSG_FASTOPEN, (ip, port))

sock_file = s.makefile('r', 0)
lines = sock_file.readlines()
for line in lines:
  print line

s.close()
