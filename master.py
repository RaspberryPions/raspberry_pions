#! /usr/bin/env python2.7

# master gets invoked when Task is created
# master gets ips from overlay and creates a list of connections to the peons
# during creating each connection, master assigns a task to the peon
# master listens (non-blocking select) for solutions
# after all tasks are completed (or some were completed and there were some errors), master invokes completed callback if it exists


import socket
import select
from threading import Thread

BLOCK_SIZE = 1024
TASK_PORT = 50009 # port used to assign tasks 
COMM_PORT = 50011 # used for testing on same machine, need to keep for reboot signaling
HOST = '127.0.0.1'


NUM_PEONS = 2



class Task(object):

    # added num_tasks since it makes sense for Task to know total number of jobs (to get out of listen loop)
    def __init__(self, num_tasks, completed_callback=None): 
        self._solutions = [] 
        self.num_tasks = num_tasks
        self.completed_callback = completed_callback
        self.peon_ip_list = ['127.0.0.1'] # get IPs from overlay
        Thread(target=self._listen).start() # listen gets thread so Task can issue jobs to peons. 


    def get_free_peon(self):
        return self.peon_ip_list[0] # free list representation



    def peon_task(self, user_function, id, args=[]):
        free_peon = self.get_free_peon() # get free peon from free list
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((HOST, COMM_PORT))
        conn.send("Hello " + str(id)) # send job to peon
        # print("sent\n")
        conn.close() # we don't need this connection anymore


    def _listen(self):

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, TASK_PORT))
        server_socket.listen(NUM_PEONS)
        print "Listening on port " + str(TASK_PORT)

        read_list = [server_socket]
        
        while self.num_tasks != 0:
            readable, writable, errored = select.select(read_list, [], [])
            for s in readable:
                if s is server_socket:
                    client_socket, address = server_socket.accept()
                    read_list.append(client_socket)
                    print "Connection from", address
                else:
                    data = s.recv(BLOCK_SIZE)
                    if data:
                        peon_message = data.strip()
                        print("Peon sends the solution ", peon_message)

                        if peon_message == "exit":
                            self.num_tasks -= 1

                        # TODO: support returned by peon error handling
                        # TODO: support timeout error handling

                        else: # TODO: modify to support longer chunk of response
                            self._solutions.append(peon_message)

                    else:
                        s.close()
                        read_list.remove(s)
        
        server_socket.close()
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