#! /usr/bin/env python2.7

# master gets invoked when Task is created
# master gets ips from overlay and creates a list of connections to the peons
# during creating each connection, master assigns a task to the peon
# master listens (non-blocking select) for solutions
# after all tasks are completed (or some were completed and there were some errors), master invokes completed callback if it exists


import socket
import select
import configs
from threading import Thread

BLOCK_SIZE = 1024
TASK_PORT = 50009 # port used to assign tasks 
COMM_PORT = 50011 # used for testing on same machine, need to keep for reboot signaling
HOST = '127.0.0.1'


NUM_PEONS = 2 # get this from overlay 



class Task(object):

    # added num_tasks since it makes sense for Task to know total number of jobs (to get out of listen loop)
    def __init__(self, num_tasks, completed_callback=None): 
        self._solutions = ["" for i in range(num_tasks)] 
        self.num_tasks = num_tasks
        self.completed_callback = completed_callback
        self.free_peons = ['127.0.0.1', '127.0.0.1'] # get IPs from overlay
        Thread(target=self._listen).start() # listen gets thread so Task can issue jobs to peons. 


    def get_free_peon(self): # free list imitation
        free_peon = self.free_peons.pop(0)
        return free_peon


    def peon_task(self, user_function, id, args=[]):
        free_peon = self.get_free_peon() # get available peon from free list

        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((HOST, COMM_PORT))
        data = str((user_function, id, args))

        # split long task into buffer-size parts
        data_blocks = [data[i: i + BLOCK_SIZE - 1] for i in range(0, len(data), BLOCK_SIZE - 1)]

        for i in range(len(data_blocks)):
            print("0" + data_blocks[i])
            st = "0" + data_blocks[i]
            st += " " * (BLOCK_SIZE - len(st))  
            conn.send(st)
        
        conn.close() 

        # mark end of input from master 
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((HOST, COMM_PORT))
        conn.send("1")
        conn.close()



    def _listen(self):
        """ Master listens to get back completed work from peons. """

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
                        received_message = data.strip()
                        job_report, id = eval(received_message)

                        print("Peon sends the solution ", job_report)

                        try: 
                            if job_report["status"] == "exit": # peon has successfully completed the task
                                addr = s.getsockname()
                                self.num_tasks -= 1 
                                ip = addr[0]
                                self.free_peons.append(ip) # add peon to the free list

                            # TODO: support returned by peon error handling: free list required
                            # TODO: support timeout error handling: free list required

                            else: 
                                self._solutions[id] += job_report["answer"]
                        except Exception as e: # something got broken on peon side, possibly need to reboot peon
                            pass # TODO: change this 

                    else:
                        s.close()
                        read_list.remove(s)
        
        server_socket.close()
        self._completed()


    def _completed(self):
        if self.completed_callback is not None: 
            self.completed_callback(self)


    def get_solutions(self):
        return self._solutions




if __name__ == "__main__":
    t = Task()




# TODO: 
# reboot peon
# reboot all
# retry subtask
# upload on PIs
# status
# multiple tasks (complicated)