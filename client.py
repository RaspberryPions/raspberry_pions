#! /usr/bin/env python2.7
import socket 

HOST = '127.0.0.1'    # The remote host
PORT = 50008             # The same port as used by the server


def establish_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    return s

def perform_tasks():
    s = establish_connection()
    while 1:
        data = s.recv(1024)
        print 'Received', repr(data)
        s.send('Hello, world')

        if data == "end":
            break
    s.close()







if __name__ == "__main__":
    perform_tasks()
