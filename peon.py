#! /usr/bin/env python2.7
import socket 
import select 
import example as example #TO BE CHANGED!!

from threading import Thread # remove on peon


BLOCK_SIZE = 1024
HOST = '127.0.0.1'    
MASTER = '127.0.0.1'    
TASK_PORT = 50009             
COMM_PORT = 50011

def establish_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, TASK_PORT))
    return s

def execute_task():
    function_name = 'user_sum'
    args = eval('[1,2,3,4]')
    #Assume we're given function_name, and (args)
    user_func = getattr(example, function_name)
    report_to_master(user_func(args))

def report_to_master(result):
    s = establish_connection()

    data = s.recv(BLOCK_SIZE)
    print 'Received on Peon', data.strip()
    st = str(result)
    st += " " * (BLOCK_SIZE - len(st))
    print(st)
    s.send(st)
    s.send("exit")
    
    s.close()


def process_commands():
    # proof of concept for select 
    # TODO: implement previous functionality

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, COMM_PORT))
    server_socket.listen(5)
    print "Listening on port " + str(COMM_PORT)

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
                    # s.send(data)
                    print(data)
                    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    conn.connect((MASTER, TASK_PORT))
                    conn.send(data)
                    conn.close()

                else:
                    s.close()
                    read_list.remove(s)


    # peon boots and listens for the master (blocks on listen)
    # if master connects, peon interpretes the command and executes it
    # results of execution are sent back to master
    # peon continues listening 


if __name__ == "__main__":
    process_commands()

