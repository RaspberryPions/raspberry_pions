#! /usr/bin/env python2.7

# peon boots and listens for the master (blocks on listen)
# if master connects, peon interpretes the command and executes it
# results of execution are sent back to master
# peon continues listening 

import socket 
import select 
# import example as example #TO BE CHANGED!!
import benchmarks as example 
import configs

from threading import Thread # currently not used, has to be used for reboot command from master 


BLOCK_SIZE = 1024
HOST = '127.0.0.1'    
MASTER = '127.0.0.1' # TODO: hardcode or get from overlay  
TASK_PORT = 50009             
COMM_PORT = 50011 

# TODO: support threading on peon for supporting rebooting purposes: use task port for communication back and forth, 
# create a different server in a thread that listens on COMM_PORT

def execute_task(processed_data):
    """ Execute task assigned by master. """

    report_pad_length = 38 # space to fit the rest of the message
    chunk_size = BLOCK_SIZE - report_pad_length

    function_name, id, args = processed_data
    user_func = getattr(example, function_name)
    job_report = {}
    try:
        result = user_func(*args) 
        print(result)
        job_report["status"] = "success"

        result_str = str(result)

        # split result in blocks
        data_blocks = [result_str[i: i + chunk_size] for i in range(0, len(result_str), chunk_size)]

        # send result blocks to master
        for i in range(len(data_blocks)):
            job_report["answer"] = data_blocks[i]
            report_to_master(job_report, id)

    except Exception as e:
        print(e)
        job_report["status"] = "error"
        report_to_master(job_report, id)

    # send end of job marker to master
    report_to_master({"status" : "exit"}, id)


def report_to_master(answer, id):
    """ Send result of task execution to master. """ 

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((MASTER, TASK_PORT))

    st = str((answer, id))
    st += " " * (BLOCK_SIZE - len(st))    

    conn.send(st)
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
    received_data = ""

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
                    print(data)
                    if data[0] == "0":  # master continues to send input
                        received_data += data[1:]  
                    else:  # end of input has been received, may execute task now
                        received_data = received_data.strip()
                        processed_data = eval(received_data)
                        execute_task(processed_data)
                        received_data = "" 
                else:
                    s.close()
                    read_list.remove(s)




if __name__ == "__main__":
    process_commands()

