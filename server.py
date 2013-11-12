#! /usr/bin/env python2.7

import socket

BLOCK_SIZE = 1024
PORT = 50007
HOST = '127.0.0.1'


NUM_PEONS = 2


# in the beginning:
    # get available peons from overlay


class Task(object):

    def __init__(self, completed_callback=None):
        self._listen()

    def peon_task(self, user_function, id, args=[]):
        pass

    def _listen(self):

        solutions = []

        s = socket.socket()
        s.bind((HOST, PORT))

        for i in range(NUM_PEONS):
            s.listen(0)
            c, addr = s.accept()
            print("Connection from", addr)

            while 1:
                c.send("Send the solution Peon")
                peon_message = c.recv(BLOCK_SIZE)
                print("Peon sends the solution ", peon_message)

                if peon_message.strip() == "exit":
                    print("closing connection", str(i))
                    break
                else:
                    solutions.append(peon_message.strip())

            c.close()

        self._completed(solutions)

    def _completed(self, solutions):
        print(solutions)



if __name__ == "__main__":
    t = Task()

# TODO: 
# reboot peon
# reboot all
# retry subtask
# non-blocking IO: select 