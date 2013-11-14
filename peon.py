#! /usr/bin/env python2.7

# peon boots and listens for the master (blocks on listen)
# if master connects, peon interpretes the command and executes it
# results of execution are sent back to master
# peon continues listening 

import socket 
import select 
import example as example #TO BE CHANGED!!

from threading import Thread # remove on peon


BLOCK_SIZE = 1024
HOST = '127.0.0.1'    
MASTER = '127.0.0.1' # TODO: hardcode or get from overlay  
TASK_PORT = 50009             
COMM_PORT = 50011 

# TODO: support threading on peon for supporting rebooting purposes. 


def execute_task():
    function_name = 'user_sum' # get this from master
    args = eval('[1,2,3,4]')
    user_func = getattr(example, function_name)
    res = user_func(args) # TODO: error handling
    return res


def report_to_master(result):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((MASTER, TASK_PORT))

    st = str(result)
    st += " " * (BLOCK_SIZE - len(st))
    conn.send(st)
    conn.send("exit")
    conn.close()


def process_commands():
    """ Peon is a server that keeps on waiting for instructions from the master. 
        Upon receiving the instruction (execute / reboot), it performs it. 
        If executing instruction resulted in an error, provides a feedback to master.  
    """

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, COMM_PORT))
    server_socket.listen(0)
    print ("Listening on port " + str(COMM_PORT)) 

    read_list = [server_socket]

    while True:
    
        readable, writable, errored = select.select(read_list, [], [])
        for s in readable:
            if s is server_socket:
                client_socket, address = server_socket.accept()
                read_list.append(client_socket)
                print ("Connection from", address)
            else:
                data = s.recv(1024)
                if data:
                    # TODO: interpret instruction
                    result = execute_task()
                    report_to_master(result)

                else:
                    s.close()
                    read_list.remove(s)


if __name__ == "__main__":
    process_commands()

