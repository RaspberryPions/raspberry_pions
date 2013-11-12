#! /usr/bin/env python2.7

import socket

BLOCK_SIZE = 1024
PORT = 50008
HOST = '127.0.0.1'

s = socket.socket()
s.bind((HOST, PORT))

s.listen(0)
c, addr = s.accept()
print("Connection from", addr)

while 1:

    c.send("blah")
    peon_message = c.recv(BLOCK_SIZE)
    print(peon_message)

c.close()