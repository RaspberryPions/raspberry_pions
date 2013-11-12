#! /usr/bin/env python2.7
import socket 
import example as example #TO BE CHANGED!!

HOST = '127.0.0.1'    # The remote host
PORT = 50009             # The same port as used by the server


def establish_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    return s

def execute_task():
    function_name = 'user_sum'
    args = eval('[1,2,3,4]')
    #Assume we're given function_name, and (args)
    user_func = getattr(example, function_name)
    report_to_master(user_func(args))

def report_to_master(result):
    s = establish_connection()

    data = s.recv(1024)
    print 'Received', data.strip()
    st = str(result)
    st += " " * (1024 - len(st))
    s.send(st)
    s.send("exit")
    
    s.close()


# while we did not reach end of output:
#   keep sending stuff + "\n\r"
# if there is remainder: pad the remainder


if __name__ == "__main__":
    execute_task()
