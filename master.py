#! /usr/bin/env python2.7

import socket
import select
from threading import Thread

BLOCK_SIZE = 1024
TASK_PORT = 50009 # port used to assign tasks 
COMM_PORT = 50011 # used for testing on same machine
HOST = '127.0.0.1'

NUM_PEONS = 2
NUM_TASKS = 4

class Task(object):

    # added num_tasks since it makes sense for Task to know total number of jobs (to get out of listen loop)
    def __init__(self, num_tasks, completed_callback=None): 
        self._solutions = [] 
        self.num_tasks = num_tasks
        self.completed_callback = completed_callback
        self.peon_ip_list = ['127.0.0.1'] # get IPs from overlay
        # listen gets it's own thread so Task can issue jobs to peons. 
        Thread(target=self._listen2).start() 

    def get_free_peon(self):
        return self.peon_ip_list[0] # free list representation

    def peon_task(self, user_function, id, args=[]):
        free_peon = self.get_free_peon() # get free peon from free list
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((HOST, COMM_PORT))
        conn.send("Hello " + str(id)) # send job to peon
        print("sent\n")
        conn.close() # we don't need this connection anymore

    def _listen2(self):
        # proof of concept for select
        # TODO: update to support previous functionality

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, TASK_PORT))
        server_socket.listen(5)
        print "Listening on port " + str(TASK_PORT)

        read_list = [server_socket]
        while True: # while self.num_tasks != 0:
            readable, writable, errored = select.select(read_list, [], [])
            for s in readable:
                if s is server_socket:
                    client_socket, address = server_socket.accept()
                    read_list.append(client_socket)
                    print "Connection from", address
                else:
                    data = s.recv(1024)
                    if data:
                        s.send(data)
                    else:
                        s.close()
                        read_list.remove(s)


    def _listen(self): # disabled, kept for reference purposes 
        s = socket.socket()
        s.bind((HOST, TASK_PORT))

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

# master gets invoked when Task is created
# master gets ips from overlay and creates a list of connections to the peons
# during creating each connection, master assigns a task to the peon
# master listens (non-blocking select) for solutions
# after all tasks are completed (or some were completed and there were some errors), master invokes completed callback if it exists
