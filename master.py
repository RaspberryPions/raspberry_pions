#! /usr/bin/env python2.7

import socket

BLOCK_SIZE = 1024
PORT = 50009
HOST = '127.0.0.1'


NUM_PEONS = 2
NUM_TASKS = 4



class Task(object):

    def __init__(self, completed_callback=None):
        self._solutions = [] 
        # get ips from overlay
        self.completed_callback = completed_callback
        self._listen()

    def peon_task(self, user_function, id, args=[]):
        pass

    def _listen(self):
        self._solutions = []

        s = socket.socket()
        s.bind((HOST, PORT))

        for i in range(NUM_TASKS):
            s.listen(0)
            c, addr = s.accept()
            print("Connection from", addr)

            while 1:
                c.send("Send the solution Peon")
                peon_message = c.recv(BLOCK_SIZE).strip()
                print("Peon sends the solution ", peon_message)

                if peon_message == "exit":
                    print("closing connection", str(i))
                    break
                else:
                    self._solutions.append(peon_message)

            c.close()

        self._completed()

    def _completed(self):
        self.completed_callback(self)

    def get_solutions(self):
        return self._solutions



if __name__ == "__main__":
    t = Task()

# TODO: 
# reboot peon
# reboot all
# retry subtask
# non-blocking IO: select 
# upload on PIs